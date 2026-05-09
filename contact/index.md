---
title: Contact
nav:
  order: 5
  tooltip: Email, address, and location
---

# {% include icon.html icon="fa-regular fa-envelope" %}Contact

{%
  include button.html
  type="email"
  text="pritam.das [at] iitb.ac.in"
  link="pritam.das&#64;iitb.ac.in"
%}
{%
  include button.html
  type="external"
  text="Google Scholar"
  link="https://scholar.google.com/citations?user=lrfA5goAAAAJ"
%}
{%
  include button.html
  type="github"
  text="pritamd47"
  link="pritamd47"
%}
{%
  include button.html
  type="linkedin"
  text="pdas47"
  link="pdas47"
%}

{% include section.html %}

{% capture col1 %}

**Pritam Das**  
Assistant Professor  
Centre of Studies in Resources Engineering (CSRE)  
Indian Institute of Technology Bombay  
Powai, Mumbai – 400 076  
Maharashtra, India

{% endcapture %}

{% capture col2 %}

**Prospective students and collaborators**  
Please read the [Join](../join) page before reaching out.
Include a brief description of your background and what you would like to work on.

**Media / outreach**  
Email is the best way to reach us.

{% endcapture %}

{% include cols.html col1=col1 col2=col2 %}
