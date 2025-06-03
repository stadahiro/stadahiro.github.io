import feedparser, os, datetime
from markdownify import markdownify as md
from slugify import slugify

RSS_URLS = [
    "https://www.city.takasaki.gunma.jp/rss/10/soshiki-2-11.xml",
    # 追加 RSS をここに
]

POST_DIR = "_posts"
os.makedirs(POST_DIR, exist_ok=True)

for url in RSS_URLS:
    feed = feedparser.parse(url)
    print(f"{len(feed.entries)} entries from {url}")
    for e in feed.entries:
        # --- 日付を安全に取得 ---
        if hasattr(e, "published_parsed"):
            dt = datetime.datetime(*e.published_parsed[:6])
        elif hasattr(e, "updated_parsed"):
            dt = datetime.datetime(*e.updated_parsed[:6])
        else:
            dt = datetime.datetime.today()
        date = dt.date()

        # --- slug & ファイル名 ---
        title = e.get("title", "No title")
        slug = slugify(title)[:50]
        fname = f"{POST_DIR}/{date}-{slug}.md"
        if os.path.exists(fname):
            continue

        # --- 本文 ---
        summary = md(e.get("summary", ""))[:300]
        link = e.get("link", "")

        with open(fname, "w", encoding="utf-8") as f:
            f.write(
f"""---
title: "{title}"
date: {date}
layout: single
link: {link}
---
{summary}
""")

            


            