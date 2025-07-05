import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("DISCORD_APPLICATION_ID")

url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"

json_data = {
    "name": "hello",
    "type": 1,
    "description": "Say hello!"
}

response = requests.post(url, json=json_data)

print("Status:", response.status_code)
print("Response:", response.text)
