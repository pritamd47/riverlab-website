---
title: Tools & Projects
nav:
  order: 2
  tooltip: Open-source tools, dashboards, and more
---

# {% include icon.html icon="fa-solid fa-wrench" %}Tools & Projects

We build open-source software and operational tools for satellite-based water-resource monitoring. Our packages are designed to be globally scalable, reproducible, and accessible to researchers and water managers alike.

{% include tags.html tags="software, reservoirs, streamflow, website" %}

{% include search-info.html %}

{% include section.html %}

## Featured

{% include list.html component="card" data="projects" filter="group == 'featured'" %}

{% include section.html %}

## More

{% include list.html component="card" data="projects" filter="!group" style="small" %}
