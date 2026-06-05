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

def why_important(title, summary):
    text = (title + " " + summary).lower()

    if "openai" in text or "chatgpt" in text:
        return "生成AI業界最大手の動向であり、市場全体への影響が大きいため"

    if "anthropic" in text or "claude" in text:
        return "ChatGPTの有力競合であり、企業向けAI活用への影響が大きいため"

    if "google" in text or "gemini" in text or "deepmind" in text:
        return "GoogleのAI戦略や検索事業への影響が注目されるため"

    if "xai" in text or "grok" in text:
        return "xAIの新機能や戦略は生成AI市場の競争に影響するため"

    if "agent" in text:
        return "AIエージェントは次世代の主要トレンドとして注目されているため"

    if "llm" in text:
        return "大規模言語モデルの進化は生成AI全体の性能向上につながるため"

    return "生成AI業界の最新動向として注目度が高いため"

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

    message += f"なぜ重要？\n{why_important(title, summary)}\n\n"

    message += f"URL：\n{entry.link}\n\n"
    message += "────────────\n\n"

response = requests.post(
    WEBHOOK_URL,
    json={"content": message}
)

print(response.status_code)
