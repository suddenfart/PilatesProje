from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")  # 👈 bunu EKLE

DATABASE_URL = os.getenv("DATABASE_URL")

print("DEBUG:", DATABASE_URL)