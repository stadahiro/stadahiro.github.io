"""
国立西洋美術館 企画展情報取得スクリプト（年省略 & 複数ブロック対応版）
"""
from __future__ import annotations
import requests, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.nmwa.go.jp"
PAGES = {
    "開催中": f"{BASE}/jp/exhibitions/current.html",
    "今後":   f"{BASE}/jp/exhibitions/upcoming.html",
}

DATE_RX  = r"(?:\d{4}年)?\d{1,2}月\d{1,2}日(?:\[[^]]+\])?"
DASHES   = r"[‐-–―－ー-]"
RANGE_RX = re.compile(rf"({DATE_RX})\s*{DASHES}\s*({DATE_RX})")

def normalize_range(start: str, end: str) -> str:
    if "年" not in end and "年" in start:
        year = re.match(r"(\d{4})年", start).group(1)
        end = f"{year}年{end}"
    if "年" not in start and "年" in end:
        year = re.match(r"(\d{4})年", end).group(1)
        start = f"{year}年{start}"
    return f"{start}－{end}"

def scrape_one(page_url: str) -> list[dict]:
    res = requests.get(page_url, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    exhibitions: list[dict] = []

    for heading in soup.find_all(["h2", "h3", "h4"], string=re.compile(r"企画展")):
        for elem in heading.find_all_next():
            if elem.name in ["h2", "h3", "h4"] and elem is not heading:
                break                                    # ← 内側ループだけ抜ける

            if elem.name in ["li", "article", "div"]:
                title_tag = elem.find(["h3", "h4", "a"])
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)

                text  = elem.get_text(" ", strip=True)
                m = RANGE_RX.search(text)
                dates = normalize_range(*m.groups()) if m else "会期情報なし"
                link  = urljoin(page_url, title_tag.get("href", ""))
                exhibitions.append({"title": title, "dates": dates, "url": link})

        # ここで break しない  ←★★★

    return exhibitions

def main() -> None:
    for label, url in PAGES.items():
        print(f"\n■ {label}の企画展（{url}）")
        for ex in scrape_one(url):
            print(f"- {ex['title']}  [{ex['dates']}]")
            print(f"  {ex['url']}")

if __name__ == "__main__":
    main()
