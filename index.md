---
title: 東京アートまとめ
layout: default    # ※「home」ではなく「default」を指定し、Recent Posts 部分を出さないようにする
author_profile: false
---

![hero](/assets/images/hero.jpg)

{: .notice--primary}
**本サイトは東京の美術館・展覧会情報を毎日自動更新しています。**

{% comment %}
  今日の日付を "YYYY-MM-DD" 形式の文字列で取得する
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
        {%- comment -%} 開催期間を「YYYY年M月D日―YYYY年M月D日」の形式で表示したい場合は、post.content を使うか別途フィールドを追加してください {%- endcomment -%}
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
    <div class="card" style="margin: 1rem;">
      <div class="card__header">
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
