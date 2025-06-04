---
layout: default
author_profile: false
---

![hero](/assets/images/hero.jpg)

{: .notice--primary}
**本サイトは東京の美術館・展覧会情報を毎日自動更新しています。**

{% assign now = site.time | date: "%Y-%m-%d" %}

---

## 開催中の企画展

{% assign any_ongoing = false %}
<div class="grid">
{% for post in site.posts %}
  {%- assign post_start = post.date | date: "%Y-%m-%d" -%}
  {%- assign post_end   = post.end_date | date: "%Y-%m-%d" -%}
  {% if post_start <= now and post_end >= now %}
    {% assign any_ongoing = true %}

    {%- comment -%}
      “museum” フィールド (例: nmwa, momat, mori) から
      `_data/museums.yml` を参照して “館名” を取得する
    {%- endcomment -%}
    {% assign museum_obj = site.data.museums | where: "id", post.museum | first %}
    {% assign museum_name = museum_obj.name %}

    <div class="card" style="margin: 1rem;">
      <div class="card__header">
        {%- comment -%}
          カード上部に小さく「館名」を表示する例
        {%- endcomment -%}
        <p class="museum-tag" style="font-size: 0.9rem; color: #555;">
          {{ museum_name }}
        </p>
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
      </div>
      <div class="card__body">
        {%- comment -%}
          本文部分には Front Matter で出力されている “会期テキスト” を表示
          （scripts/scrape_nmwa.py が本文に **YYYY年MM月DD日－YYYY年MM月DD日** を書き込んでいるため）
        {%- endcomment -%}
        {%- assign dates_raw = post.content | strip_html | strip_newlines -%}
        <p>{{ dates_raw }}</p>
        <p><a href="{{ post.link }}" target="_blank" rel="noopener">公式サイトを見る →</a></p>
      </div>
    </div>
  {% endif %}
{% endfor %}
</div>

{% unless any_ongoing %}
  <p>現在、開催中の企画展はありません。</p>
{% endunless %}

---

## 今後の企画展

{% assign any_upcoming = false %}
<div class="grid">
{% for post in site.posts %}
  {%- assign post_start = post.date | date: "%Y-%m-%d" -%}
  {% if post_start > now %}
    {% assign any_upcoming = true %}

    {% assign museum_obj = site.data.museums | where: "id", post.museum | first %}
    {% assign museum_name = museum_obj.name %}

    <div class="card" style="margin: 1rem;">
      <div class="card__header">
        <p class="museum-tag" style="font-size: 0.9rem; color: #555;">
          {{ museum_name }}
        </p>
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
      </div>
      <div class="card__body">
        {%- assign dates_raw = post.content | strip_html | strip_newlines -%}
        <p>{{ dates_raw }}</p>
        <p><a href="{{ post.link }}" target="_blank" rel="noopener">公式サイトを見る →</a></p>
      </div>
    </div>
  {% endif %}
{% endfor %}
</div>

{% unless any_upcoming %}
  <p>今後予定されている企画展はありません。</p>
{% endunless %}
