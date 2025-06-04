---
layout: home
author_profile: false
paginate: false
---
![hero](/assets/images/hero.jpg)

{: .notice--primary}
**本サイトは東京の美術館・展覧会情報を毎日自動更新しています。**

---

## 開催中の企画展

{% assign now = site.time | date: "%Y-%m-%d" %}

{%- comment -%}
  post.date を文字列化してから比較する（Liquid は文字列同士の比較なら OK）
{%- endcomment -%}
{% assign tmp = site.posts | where_exp: "post", "post.date | date: '%Y-%m-%d' <= now" %}
{% assign ongoing = tmp | where_exp: "post", "post.end_date >= now" %}

{% if ongoing.size > 0 %}
  <div class="grid">
  {% for post in ongoing %}
    <div class="card" style="margin: 1rem;">
      <div class="card__header">
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
      </div>
      <div class="card__body">
        <p>{{ post.dates }}</p>
        <p><a href="{{ post.link }}" target="_blank" rel="noopener">公式サイトを見る →</a></p>
      </div>
    </div>
  {% endfor %}
  </div>
{% else %}
  <p>現在、開催中の企画展はありません。</p>
{% endif %}

---

## 今後の企画展

{%- comment -%}
  こちらも同様に post.date を文字列化して比較
{%- endcomment -%}
{% assign upcoming = site.posts | where_exp: "post", "post.date | date: '%Y-%m-%d' > now" | sort: "date" %}

{% if upcoming.size > 0 %}
  <div class="grid">
  {% for post in upcoming %}
    <div class="card" style="margin: 1rem;">
      <div class="card__header">
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
      </div>
      <div class="card__body">
        <p>{{ post.dates }}</p>
        <p><a href="{{ post.link }}" target="_blank" rel="noopener">公式サイトを見る →</a></p>
      </div>
    </div>
  {% endfor %}
  </div>
{% else %}
  <p>今後予定されている企画展はありません。</p>
{% endif %}

---

## 今後の企画展

{% assign upcoming = site.posts | where_exp: "post", "post.date > now" | sort: "date" %}
{% if upcoming.size > 0 %}
  <div class="grid">
  {% for post in upcoming %}
    <div class="card" style="margin: 1rem;">
      <div class="card__header">
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
      </div>
      <div class="card__body">
        <p>{{ post.dates }}</p>
        <p><a href="{{ post.link }}" target="_blank" rel="noopener">公式サイトを見る →</a></p>
      </div>
    </div>
  {% endfor %}
  </div>
{% else %}
  <p>今後予定されている企画展はありません。</p>
{% endif %}
