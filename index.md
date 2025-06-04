---
layout: home
author_profile: false
paginate: false
---
![hero](/assets/images/hero.jpg)

{: .notice--primary}
**本サイトは東京の美術館・展覧会情報を毎日自動更新しています。**

{% comment %}
  今日の日付（文字列 "YYYY-MM-DD"）を取得
{% endcomment %}
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
    <div class="card" style="margin: 1rem;">
      <div class="card__header">
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
      </div>
      <div class="card__body">
        <p>{{ post.dates }}</p>
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
    <div class="card" style="margin: 1rem;">
      <div class="card__header">
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
      </div>
      <div class="card__body">
        <p>{{ post.dates }}</p>
        <p><a href="{{ post.link }}" target="_blank" rel="noopener">公式サイトを見る →</a></p>
      </div>
    </div>
  {% endif %}
{% endfor %}
</div>

{% unless any_upcoming %}
  <p>今後予定されている企画展はありません。</p>
{% endunless %}
