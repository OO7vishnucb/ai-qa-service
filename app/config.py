# config.py
# Loads settings from the .env file so we never hardcode secrets in code.

from dotenv import load_dotenv
import os

load_dotenv()  # reads the .env file and puts values into environment variables

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Quick safety check — crash early with a clear message if keys are missing
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Add it to your .env file.")
