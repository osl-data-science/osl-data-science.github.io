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

# {{ title }} ({{ release_date }})

#### Authors: {{ ", ".join(authors) }}

{{ description }}

{% raw %}{% include "projects/{% endraw %}{{ slug }}{% raw %}/index.html" %}{% endraw %}
