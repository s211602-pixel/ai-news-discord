import feedparser
import requests
import os
import re

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

rss_url = (
    "https://news.google.com/rss/search?"
    "q=OpenAI+OR+Anthropic+OR+Google+DeepMind+OR+xAI+OR+AI+Agent"
    "&hl=ja&gl=JP&ceid=JP:ja"
)

feed = feedparser.parse(rss_url)

message = "🤖【本日の生成AIニュース】\n\n"

medals = ["🥇", "🥈", "🥉"]

priority_keywords = [
    "OpenAI",
    "Anthropic",
    "Google",
    "DeepMind",
    "Gemini",
    "ChatGPT",
    "Claude",
    "xAI",
    "Grok",
    "AI Agent",
    "LLM"
]

def score(entry):
    text = (entry.title + " " + getattr(entry, "summary", "")).lower()

    s = 0

    for keyword in priority_keywords:
        if keyword.lower() in text:
            s += 10

    return s

entries = sorted(feed.entries, key=score, reverse=True)

for i, entry in enumerate(entries[:3], start=1):

    title = entry.title

    summary = ""
    if hasattr(entry, "summary"):
        summary = re.sub("<.*?>", "", entry.summary)
        summary = summary.replace("続きを読む", "")
        summary = summary.strip()

    if len(summary) > 180:
        summary = summary[:180] + "..."

message += f"{medals[i-1]} {i}位\n"
message += f"{title}\n\n"

if summary:
    message += f"概要：\n{summary}\n\n"

message += f"URL：\n{entry.link}\n\n"

message += "────────────\n\n"

requests.post(
    WEBHOOK_URL,
    json={"content": message}
)
