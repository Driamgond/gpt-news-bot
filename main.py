import os
import requests
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAILERLITE_API_KEY = os.getenv("MAILERLITE_API_KEY")
MAILERLITE_GROUP_ID = os.getenv("MAILERLITE_GROUP_ID")

# Dummy news source (replace with real fetch later)
NEWS = [
    "AI dominates global investment trends in 2025...",
    "OpenAI expands API capabilities for automation...",
]

# Summarize news using OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
summaries = []

for article in NEWS:
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize this: {article}"}]
    )
    summaries.append(res.choices[0].message.content)

# Save to markdown
md_content = "\n".join([f"### {datetime.today().date()} Summary", ""] + summaries)
with open("today.md", "w") as f:
    f.write(md_content)

# Send email via MailerLite API (no SDK needed)
def send_mailerlite_campaign(api_key, group_id, subject, html):
    base_url = "https://connect.mailerlite.com/api"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Step 1: Create campaign
    campaign_data = {
        "type": "regular",
        "name": subject,
        "subject": subject,
        "from": {
            "email": "noreply@driamgond.com",
            "name": "GPT Digest"
        },
        "groups": [group_id],
        "content": {
            "html": html
        }
    }

    r = requests.post(f"{base_url}/campaigns", headers=headers, json=campaign_data)
    r.raise_for_status()
    campaign_id = r.json()["id"]

    # Step 2: Send campaign
    send_resp = requests.post(f"{base_url}/campaigns/{campaign_id}/actions/send", headers=headers)
    send_resp.raise_for_status()

# Fire off the campaign
send_mailerlite_campaign(
    api_key=MAILERLITE_API_KEY,
    group_id=MAILERLITE_GROUP_ID,
    subject=f"🧠 AI News Summary - {datetime.today().date()}",
    html="<br>".join(summaries)
)
