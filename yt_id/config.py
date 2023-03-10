"""Module consists of necessary configurations."""
import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")
DATADIR = os.getenv("DATADIR", "data")
