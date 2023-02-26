"""Module consists of necessary configurations."""
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

API_KEY = os.getenv("API_KEY", "AIzaSyCYFvoCfs6D4OJe7eJfec_0192f234JPzg")
URL = os.getenv("URL", "https://youtube.googleapis.com/youtube/v3/videos")
DATADIR = os.getenv("DATADIR", "data")