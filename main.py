from openaq import OpenAQ

import pandas as pd
import dataclasses
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from langchain_community.llms import Replicate
import os

# API keys (Colab userdata)
openaq_api_key =  os.getenv('OPENAQ_API_KEY')
replicate_api_token = os.getenv('REPLICATE_API_TOKEN')
os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

api = OpenAQ(api_key=openaq_api_key)
model_id = "ibm-granite/granite-3.2-8b-instruct"
granite = Replicate(model=model_id, replicate_api_token=replicate_api_token)

def extract_local_date_from_period(period):
    if not period:
        return None
    # period bisa berisi kunci berbeda: 'datetime_from', 'date', 'datetime'
    for key in ("datetime_from", "date", "datetime"):
        if key in period and period[key]:
            # beberapa struktur: period[key] bisa dict {'local': '...'} atau string
            try:
                if isinstance(period[key], dict) and 'local' in period[key]:
                    return period[key]['local']
                # kadang period[key] sendiri sudah string (jarang)
                if isinstance(period[key], str):
                    return period[key]
            except Exception:
                continue
    # ada juga kemungkinan kunci 'date' di level lain
    try:
        # fallback: jika period punya 'date' yang berisi dict
        if 'date' in period and isinstance(period['date'], dict) and 'local' in period['date']:
            return period['date']['local']
    except Exception:
        pass
    return None

try:  
  #nyari negara indo
    countries = api.countries.list(limit=300)
    df_countries = pd.DataFrame([dataclasses.asdict(c) for c in countries.results])
    indonesia_row = df_countries[df_countries['code'] == 'ID']
    if indonesia_row.empty:
        raise Exception("Indonesia tidak ditemukan di daftar negara OpenAQ.")
    indonesia_id = int(indonesia_row.iloc[0]['id'])
    #buat nyari lokasi jakarta
    locs = api.locations.list(countries_id=indonesia_id, limit=1000)
    df_locations = pd.DataFrame([dataclasses.asdict(l) for l in locs.results])
    df_jakarta = df_locations[df_locations['name'].str.contains("Jakarta", case=False, na=False)]
    if df_jakarta.empty:
        raise Exception("Tidak ada lokasi Jakarta di data OpenAQ.")

    pm25_sensors = []
    for loc_id in df_jakarta['id']:
        loc_detail = api.locations.get(locations_id=int(loc_id))
        detail_list = [dataclasses.asdict(m) for m in loc_detail.results]
        if not detail_list:
            continue
        sensors_list = detail_list[0].get('sensors', []) or []
        for s in sensors_list:
            try:
                if 'pm25' in (s.get('name') or '').lower() or (s.get('parameter') and s['parameter'].get('name') == 'pm25'):
                    pm25_sensors.append(int(s['id']))
            except Exception:
                continue

    pm25_sensors = list(dict.fromkeys(pm25_sensors)) 
    if not pm25_sensors:
        raise Exception("Tidak ditemukan sensor PM2.5 di lokasi jakarta.")

    #30 hari.
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    all_measurements = []

    for sensor_id in pm25_sensors:
        meas = api.measurements.list(
            sensors_id=sensor_id,
            datetime_from=start_date.isoformat() + "Z",
            datetime_to=end_date.isoformat() + "Z",
            limit=1000
        )

        chunk = [dataclasses.asdict(m) for m in meas.results] if getattr(meas, "results", None) else []
        if chunk:
            all_measurements.extend(chunk)

    if not all_measurements:
        raise Exception("Tidak ada data PM2.5 untuk 30 hari terakhir dari semua sensor di Jakarta.")

  
    df_meas = pd.DataFrame(all_measurements)

    df_meas['date_local_raw'] = df_meas['period'].apply(lambda p: extract_local_date_from_period(p))
    df_meas['date_local'] = pd.to_datetime(df_meas['date_local_raw'], errors='coerce')

    def safe_param_name(p):
        try:
            if isinstance(p, dict):
                return p.get('name') or p.get('display_name') or None
        except:
            pass
        return None

    def safe_param_unit(p):
        try:
            if isinstance(p, dict):
                
                return p.get('units') or p.get('unit') or None
        except:
            pass
        return None

    df_meas['parameter_name'] = df_meas['parameter'].apply(safe_param_name)
    df_meas['unit'] = df_meas['parameter'].apply(safe_param_unit)

  
    df_clean = df_meas.dropna(subset=['date_local', 'value']).copy()

    df_clean = df_clean.sort_values('date_local').reset_index(drop=True)

    df_final = df_clean[['date_local', 'value', 'parameter_name', 'unit']].copy()

    print(f"Mengambil {len(df_final)} baris data PM2.5 dari {len(pm25_sensors)} sensor (gabungan).")
    display(df_final.head())

    #disini visual
    plt.figure(figsize=(12,5))
    plt.plot(df_final['date_local'], df_final['value'], marker='o', linestyle='-', alpha=0.6)
    plt.title('Tren PM2.5 di Jakarta (30 Hari Terakhir) — Gabungan Sensor')
    plt.xlabel('Tanggal')
    plt.ylabel(f"PM2.5 ({df_final['unit'].dropna().unique().tolist()[:3]})")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

  
    summary_stats = df_final['value'].describe().to_dict()
    prompt = f"""
    Anda adalah analis lingkungan.
    Data PM2.5 Jakarta (30 hari, gabungan sensor). Statistik ringkas: {summary_stats}

    1) Jelaskan kondisi kualitas udara secara umum.
    2) Sebutkan pola/tren yang terlihat.
    3) Kenapa PM2.5 Berbahaya dan jelaskan secara detail dari hasil yang kamu peroleh secara detail dengan anda menjelaskan ke orang yang awam
    4) Berikan rekomendasi singkat untuk pemerintah dan masyarakat.
    """

    try:
        insight = granite(prompt)
        print("=== Insight & Rekomendasi AI ===")
        print(insight)
    except Exception as e:
        print("Insight AI gabisa dijalankan:", e)

except Exception as e:
    print("Terjadi error:", e)