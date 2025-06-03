#!/usr/bin/env python3
"""Google アラート RSS → Jekyll ポスト"""
import feedparser, os, datetime, hashlib
from markdownify import markdownify as md
from slugify import slugify

RSS_URLS = [
    "https://www.nact.jp/exhibition/rss.xml",  # 例
]
POST_DIR = "_posts"

os.makedirs(POST_DIR, exist_ok=True)
print(f'Write to: {filename}')

for url in RSS_URLS:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        date = datetime.datetime(*entry.published_parsed[:6]).date()
        slug = slugify(title)[:50]
        filename = f"{POST_DIR}/{date}-{slug}.md"
        if os.path.exists(filename):
            continue  # 重複スキップ
        summary = md(entry.summary)[:200]
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"---\n")
            f.write(f"title: \"{title}\"\n")
            f.write(f"date: {date}\n")
            f.write(f"layout: single\n")
            f.write(f"link: {link}\n")
            f.write(f"---\n\n{summary}\n")