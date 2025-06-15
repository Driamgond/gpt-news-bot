import os
import requests
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # optional if testing locally

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MAILERLITE_API_KEY = os.environ.get("MAILERLITE_API_KEY")
MAILERLITE_GROUP_ID = os.environ.get("MAILERLITE_GROUP_ID")

# Dummy news
NEWS = [
    "AI dominates global investment trends in 2025...",
    "OpenAI expands API capabilities for automation...",
]

# OpenAI summary
client = OpenAI(api_key=OPENAI_API_KEY)
summaries = [
    client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize this: {n}"}]
    ).choices[0].message.content
    for n in NEWS
]

# Save markdown
md_content = "\n".join([f"### {datetime.today().date()} Summary", ""] + summaries)
with open("today.md", "w") as f:
    f.write(md_content)

# Send email via MailerLite API
headers = {
    "Authorization": f"Bearer {MAILERLITE_API_KEY}",
    "Content-Type": "application/json"
}

campaign_payload = {
    "type": "regular",
    "settings": {
        "subject": f"🧠 AI News Summary - {datetime.today().date()}",
        "from": "noreply@example.com",
        "reply_to": "noreply@example.com",
        "name": "GPT News Bot"
    }
}

# 1. Create campaign
campaign_response = requests.post(
    "https://connect.mailerlite.com/api/campaigns",
    headers=headers,
    json=campaign_payload
)

if campaign_response.status_code != 201:
    print("❌ Failed to create campaign")
    print(campaign_response.text)
    exit(1)

campaign_id = campaign_response.json()["id"]

# 2. Set content
content_payload = {
    "html": "<br>".join(summaries)
}
requests.put(
    f"https://connect.mailerlite.com/api/campaigns/{campaign_id}/content",
    headers=headers,
    json=content_payload
)

# 3. Send campaign
requests.post(
    f"https://connect.mailerlite.com/api/campaigns/{campaign_id}/actions/send",
    headers=headers
)
