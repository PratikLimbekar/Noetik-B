import os
from dotenv import load_dotenv

load_dotenv()

#initially just to have env files outside

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
SESSION_SECRET = os.getenv("SESSION_SECRET")