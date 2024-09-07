import os
from dotenv import load_dotenv

load_dotenv()

APP_PORT = 3001

# Get environment variables
if os.getenv('APP_PORT'):
    APP_PORT = int(os.getenv('APP_PORT'))