
import os
import requests
from datetime import datetime
from openai import OpenAI
from mailerlite import MailerLiteClient

# Load env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAILERLITE_API_KEY = os.getenv("MAILERLITE_API_KEY")
MAILERLITE_GROUP_ID = os.getenv("MAILERLITE_GROUP_ID")

# Dummy news source
NEWS = [
    "AI dominates global investment trends in 2025...",
    "OpenAI expands API capabilities for automation...",
]

# Summarize news
client = OpenAI(api_key=OPENAI_API_KEY)
summaries = [client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"Summarize this: {n}"}]
).choices[0].message.content for n in NEWS]

# Save to markdown
md_content = "\n".join([f"### {datetime.today().date()} Summary", ""] + summaries)
with open("today.md", "w") as f:
    f.write(md_content)

# Send email
mailer = MailerLiteClient(api_key=MAILERLITE_API_KEY)
mailer.campaigns.create_and_send(
    subject=f"🧠 AI News Summary - {datetime.today().date()}",
    group_id=MAILERLITE_GROUP_ID,
    html="<br>".join(summaries)
)
