# scripts/ics2md.py
import icalendar, requests, datetime, os
POST_DIR = "_posts"
ICS_URL = "https://www.nact.jp/calendar/events.ics"

cal = icalendar.Calendar.from_ical(requests.get(ICS_URL).content)
for comp in cal.walk("vevent"):
    title = str(comp.get("summary"))
    dt = comp.decoded("dtstart").date()
    slug = slugify(title)[:50]
    fname = f"{POST_DIR}/{dt}-{slug}.md"
    if os.path.exists(fname):
        continue
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"""---
title: "{title}"
date: {dt}
museum: nact
layout: single
---
※公式 iCal 情報から自動取得
""")
