import feedparser
import requests
import os
import re

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

rss_url = (
    "https://news.google.com/rss/search?"
    "q=generative+AI+OR+OpenAI+OR+Anthropic+OR+Google+AI"
    "&hl=ja&gl=JP&ceid=JP:ja"
)

feed = feedparser.parse(rss_url)

message = "🤖【本日の生成AIニュース】\n\n"

for i, entry in enumerate(feed.entries[:3], start=1):

    title = entry.title

    summary = ""
    if hasattr(entry, "summary"):
        summary = re.sub("<.*?>", "", entry.summary)
        summary = summary.replace("続きを読む", "")
        summary = summary.strip()

    if len(summary) > 180:
        summary = summary[:180] + "..."

    message += f"■ {i}. {title}\n"

    if summary:
        message += f"概要：{summary}\n"

    message += f"URL：{entry.link}\n\n"

requests.post(
    WEBHOOK_URL,
    json={"content": message}
)
