import json
import feedparser
import requests
from openai import OpenAI

WEBHOOK_URL = __import__("os").environ["DISCORD_WEBHOOK_URL"]
OPENAI_API_KEY = __import__("os").environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

rss_url = "https://news.google.com/rss/search?q=generative+AI+OR+OpenAI+OR+Anthropic+OR+Google+AI&hl=en-US&gl=US&ceid=US:en"

feed = feedparser.parse(rss_url)

articles = []

for entry in feed.entries[:20]:
    articles.append(
        f"Title: {entry.title}\n"
        f"Link: {entry.link}"
    )

prompt = f"""
以下のニュース候補から、
重要度が高い順に3件選び、

- タイトル
- 要約（150文字以内）
- なぜ重要か

を日本語で出力してください。

ニュース候補:

{chr(10).join(articles)}
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

summary = response.choices[0].message.content

requests.post(
    WEBHOOK_URL,
    json={
        "content":
        f"## 本日の生成AIトレンド\n\n{summary}"
    }
)
