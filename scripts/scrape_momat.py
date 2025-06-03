# scripts/scrape_momat.py
import requests, bs4, datetime, os, pathlib
from slugify import slugify

URL = "https://www.momat.go.jp/exhibition/"
POST_DIR = "_posts"
os.makedirs(POST_DIR, exist_ok=True)

html = requests.get(URL, timeout=20).text
soup = bs4.BeautifulSoup(html, "html.parser")

for item in soup.select(".exhibition__item"):
    title = item.select_one(".title").get_text(strip=True)
    link = item.select_one("a")["href"]
    # 会期テキストを日付に変換（例: 2025.7.10 – 10.12）
    dates = item.select_one(".date").get_text()
    start = dates.split("–")[0].strip().replace(".", "-")
    date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    slug = slugify(title)[:50]
    fname = f"{POST_DIR}/{date}-{slug}.md"
    if pathlib.Path(fname).exists():
        continue
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"""---
title: "{title}"
date: {date}
museum: momat
layout: single
link: {link}
---
({dates}) の会期で開催予定。
""")
