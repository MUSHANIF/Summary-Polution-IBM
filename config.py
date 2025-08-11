import os
from dotenv import load_dotenv

load_dotenv()  # Baca file .env

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
