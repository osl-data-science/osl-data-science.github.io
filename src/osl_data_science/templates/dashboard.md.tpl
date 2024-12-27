---
title: {{ title }}
slug: {{ slug }}
description: {{ description }}
authors:
{% for author in authors %}
  - {{ author }}
{% endfor %}
date: {{ release_date }}
template: dashboards.html
---

## {{ title }}

<section id="info" class="bg-light py-2 my-2 rounded">
  <div class="container m-2">
    <p class="p-1 m-0"><strong>Release Date:</strong> {{ release_date }}</p>
    <p class="p-1 m-0"><strong>Authors:</strong> {{ ", ".join(authors) }}</p>
    <p class="p-1 m-0"><strong>Description:</strong> {{ description }}</p>
    {% if references %}
    <p class="p-1 m-0">
      <strong>References:</strong>
    </p>
    <ul>
    {% for ref in references %}
      <li>{{ ref }}</li>
    {% endfor %}
    </ul>
    {% endif %}
  </div>
</section>

{% raw %}{% include "projects/{% endraw %}{{ slug }}{% raw %}/index.html" %}{% endraw %}
