---
layout: page
title: 東京の美術館一覧
permalink: /museums/
---

| 美術館 | エリア | 最寄り駅 |
|---------|--------|-----------|
{% for m in site.data.museums %}
| [{{ m.name }}]({{ m.url }}) | {{ m.area }} | {{ m.nearest }} |
{% endfor %}