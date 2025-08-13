# Jakarta PM2.5 Air Quality Analysis with AI Support By Mus

## 📌 Project Overview

Proyek ini bertujuan untuk menganalisis kualitas udara di Jakarta selama 30 hari terakhir, khususnya fokus pada parameter **PM2.5** yang diambil dari API publik **OpenAQ**. Data diperoleh dari berbagai sensor di Jakarta, kemudian diproses untuk mendapatkan tren, pola, dan insight yang bermanfaat bagi masyarakat maupun pemerintah.

Analisis ini dibantu oleh **IBM Granite AI Model** melalui layanan **Replicate**, yang digunakan untuk memberikan interpretasi dan rekomendasi berbasis data.

---

## 📂 Raw Dataset Link

- Sumber data: [OpenAQ API](https://docs.openaq.org/)
- Endpoint yang digunakan:
  - `/measurements` → mengambil data pengukuran PM2.5
- Data diambil khusus untuk Indonesia (lokasi Jakarta) dan periode 30 hari terakhir.
- Pengambilan dan pembersihan data dilakukan menggunakan Python.

---

## 📊 Insight & Findings

Berdasarkan data PM2.5 dari seluruh sensor di Jakarta selama 30 hari terakhir:

- **Statistik ringkas** (contoh):
  - Mean: _sekitar XX μg/m³_
  - Min: _sekitar XX μg/m³_
  - Max: _sekitar XX μg/m³_
  - Std dev: _sekitar XX μg/m³_
- **Pola umum**:
  - Terjadi fluktuasi PM2.5 harian, dengan beberapa puncak konsentrasi yang signifikan.
  - Tren cenderung stabil di kisaran _X–Y μg/m³_, namun dengan beberapa hari di atas batas aman WHO (25 μg/m³ untuk rata-rata 24 jam).
- **Potensi risiko**:
  - Konsentrasi tinggi PM2.5 berbahaya karena dapat menembus saluran pernapasan hingga alveoli paru-paru dan masuk ke aliran darah.

---

## 🤖 AI Support Explanation

Proses analisis ini memanfaatkan **IBM Granite 3.2 8B Instruct** melalui **Replicate API** untuk:

1. Menginterpretasikan hasil statistik PM2.5.
2. Menjelaskan dampak PM2.5 terhadap kesehatan dengan bahasa yang mudah dimengerti masyarakat awam.
3. Memberikan rekomendasi singkat bagi:
   - **Pemerintah**: misalnya meningkatkan pemantauan dan kebijakan pengendalian emisi.
   - **Masyarakat**: misalnya menggunakan masker di luar ruangan saat kualitas udara buruk.

Catatan:

- **AI tidak digunakan untuk mengambil atau memproses data mentah**. Semua pengambilan dan pembersihan data dilakukan secara manual dengan Python.
- AI hanya digunakan untuk **mendukung analisis dan penyusunan insight**.

---

## 📈 Visualisasi

Script ini menghasilkan grafik tren PM2.5 selama 30 hari terakhir di Jakarta:

![Tren PM2.5](docs/pm25_trend.png)
