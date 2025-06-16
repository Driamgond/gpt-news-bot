import os
import requests
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAILERLITE_API_KEY = os.getenv("MAILERLITE_API_KEY")
MAILERLITE_GROUP_ID = os.getenv("MAILERLITE_GROUP_ID")

# Initialize OpenAI
client = OpenAI()
client.api_key = OPENAI_API_KEY

# Dummy news (나중에 RSS로 대체 가능)
NEWS = [
    "AI dominates global investment trends in 2025...",
    "OpenAI expands API capabilities for automation...",
]

# Summarize news
summaries = [client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"Summarize this: {n}"}]
).choices[0].message.content for n in NEWS]

# Save to markdown file
md_content = "\n".join([f"### {datetime.today().date()} Summary", ""] + summaries)
with open("today.md", "w") as f:
    f.write(md_content)

# Format HTML content for email
content_html = "<h2>🧠 AI News Summary</h2><ul>" + "".join(
    [f"<li>{s}</li>" for s in summaries]
) + "</ul><hr><p>💰 Sponsored: <a href='https://your-affiliate-link.com'>Try the AI tool we use → Click here</a></p>"

# Prepare MailerLite campaign payload
campaign_url = "https://api.mailerlite.com/api/v2/campaigns"
headers = {
    "Content-Type": "application/json",
    "X-MailerLite-ApiKey": MAILERLITE_API_KEY
}
payload = {
    "subject": f"🧠 AI News Summary - {datetime.today().date()}",
    "groups": [MAILERLITE_GROUP_ID],
    "type": "regular",
    "from": {
        "name": "AI Brief",
        "email": "driamgond@gmail.com"
    },
    "content": {
        "html": content_html
    }
}

# Send request to MailerLite
response = requests.post(campaign_url, headers=headers, json=payload)
print(f"[MailerLite 응답 코드] {response.status_code}")
print(f"[MailerLite 응답 내용] {response.text}")
