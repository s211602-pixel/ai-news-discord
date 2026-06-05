import feedparser
import requests
import os

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

rss_url = (
    "https://news.google.com/rss/search?"
    "q=generative+AI+OR+OpenAI+OR+Anthropic+OR+Google+AI"
    "&hl=ja&gl=JP&ceid=JP:ja"
)

feed = feedparser.parse(rss_url)

message = "【本日の生成AIニュース】\n\n"

for i, entry in enumerate(feed.entries[:3], start=1):
    message += f"{i}. {entry.title}\n"
    message += f"{entry.link}\n\n"

requests.post(
    WEBHOOK_URL,
    json={"content": message}
)
