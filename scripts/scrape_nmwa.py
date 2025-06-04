"""
国立西洋美術館 企画展情報取得スクリプト（開始日と終了日を front matter に含める版）
"""
from __future__ import annotations
import requests, re, os, pathlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from slugify import slugify

BASE = "https://www.nmwa.go.jp"
PAGES = {
    "開催中": f"{BASE}/jp/exhibitions/current.html",
    "今後":   f"{BASE}/jp/exhibitions/upcoming.html",
}

# 日付パターン：YYYY年M月D日 など
DATE_RX  = r"(?:\d{4}年)?\d{1,2}月\d{1,2}日(?:\[[^]]+\])?"
DASHES   = r"[‐-–―－ー-]"   # 省略線などの複数バリエーション
RANGE_RX = re.compile(rf"({DATE_RX})\s*{DASHES}\s*({DATE_RX})")

POST_DIR = "_posts"
os.makedirs(POST_DIR, exist_ok=True)

def normalize_range(start: str, end: str) -> tuple[str,str]:
    """
    start: "2025年3月11日"
    end:   "3月 8日" または "2025年6月8日" など
    → 両方に年を付与して戻す
    """
    if "年" not in end and "年" in start:
        year = re.match(r"(\d{4})年", start).group(1)
        end = f"{year}年{end}"
    if "年" not in start and "年" in end:
        year = re.match(r"(\d{4})年", end).group(1)
        start = f"{year}年{start}"
    return start, end

def scrape_one(page_url: str) -> list[dict]:
    """
    指定したページ（current.html または upcoming.html）から
    各企画展のタイトル・会期・リンクを取得し、辞書リストで返す。
    """
    res = requests.get(page_url, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    exhibitions: list[dict] = []
    for heading in soup.find_all(["h2", "h3", "h4"], string=re.compile(r"企画展")):
        for elem in heading.find_all_next():
            # 次の「h2/h3/h4」にぶつかったら内側ループを抜ける
            if elem.name in ["h2", "h3", "h4"] and elem is not heading:
                break
            # li, article, div の中を探す
            if elem.name in ["li", "article", "div"]:
                title_tag = elem.find(["h3", "h4", "a"])
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)

                text  = elem.get_text(" ", strip=True)
                m = RANGE_RX.search(text)
                if m:
                    raw_start, raw_end = m.groups()
                    start_norm, end_norm = normalize_range(raw_start, raw_end)
                else:
                    start_norm, end_norm = "", ""

                link  = urljoin(page_url, title_tag.get("href", ""))
                exhibitions.append({
                    "title": title,
                    "dates_raw": f"{start_norm}－{end_norm}" if m else "会期情報なし",
                    "start_raw": start_norm,
                    "end_raw": end_norm,
                    "url": link
                })
        # heading ごとに break しない → 開催中/今後のブロックすべてを取得
    return exhibitions

def main() -> None:
    for label, url in PAGES.items():
        # PAGES のキー（開催中 / 今後）はログ用。出力には関係なし。
        for ex in scrape_one(url):
            # raw 文字列から「YYYY年M月D日」を抽出して ISO 形式に直す
            if not ex["start_raw"] or not ex["end_raw"]:
                # 日付情報が取れなかったらスキップ
                continue

            # 例: "2025年3月11日" を数字に分解
            m1 = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", ex["start_raw"])
            m2 = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", ex["end_raw"])
            if not (m1 and m2):
                continue
            y1, mo1, d1 = map(int, m1.groups())
            y2, mo2, d2 = map(int, m2.groups())

            iso_start = f"{y1:04d}-{mo1:02d}-{d1:02d}"
            iso_end   = f"{y2:04d}-{mo2:02d}-{d2:02d}"
            slug = slugify(ex["title"])[:50]
            fname = f"{POST_DIR}/{iso_start}-{slug}.md"
            if pathlib.Path(fname).exists():
                # 既存ファイルがあれば上書きせずスキップ
                continue

            # Markdown ファイルを生成
            with open(fname, "w", encoding="utf-8") as f:
                f.write(f"---\n")
                f.write(f"title: \"{ex['title']}\"\n")
                f.write(f"date: {iso_start}\n")
                f.write(f"end_date: {iso_end}\n")
                f.write(f"museum: nmwa\n")
                f.write(f"layout: single\n")
                f.write(f"link: \"{ex['url']}\"\n")
                f.write(f"---\n\n")
                # 表示用に元の会期テキストを本文に残す
                f.write(f"**{ex['dates_raw']}**\n")
    # 処理が終わったら終了

if __name__ == "__main__":
    main()
