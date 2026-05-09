# RIVER Lab Website

This is the source for the RIVER Lab website at CSRE, IIT Bombay. 

---

## Adding a new publication

1. Add the paper to the **my-publications** collection in Zotero. Setup the collection with better-bibtex to create an automatic export every time an item is added to the collection. This file is stored in `repo/db/my-publications.bib`. `db` is .git-ignored.
2. Optionally, add a representative figure from the paper: place the image in `images/` and add an `image:` field to the entry in `_data/sources.yaml`:
   ```yaml
   - id: doi:10.xxxx/xxxxx
     image: images/fig-my-paper.jpg
   ```
3. Optionally, add a downloadable PDF link. If the paper is open access, link directly to the publisher's PDF. For paywalled papers, upload the author accepted manuscript as a GitHub Release asset and link to that URL:
   ```yaml
   - id: doi:10.xxxx/xxxxx
     buttons:
       - type: pdf
         link: https://link-to-pdf.pdf
   ```
4. Run the sync script to update `_data/sources.yaml` from the bib file:
   ```sh
   python3 _cite/bib_sync.py
   ```
   This adds new DOIs while preserving all custom fields (figures, PDF buttons, descriptions, tags) for existing entries.
5. Regenerate `_data/citations.yaml`:
   ```sh
   python3 _cite/cite.py
   ```

---

## Adding a news post

Create a new Markdown file in `_posts/` with the filename format `YYYY-MM-DD-short-title.md`. The frontmatter controls how the post appears in the news feed:

```markdown
---
title: Your post title
author: pritam-das
tags:
  - lab news
---

Post content in Markdown goes here.
```

- **`author`** should match the member's filename in `_data/members.yaml`.
- **`tags`** are freeform — they appear as filter chips on the blog page. Common ones: `lab news`, `publication`, `software`.
- The post will automatically appear on the homepage (latest 3) and the `/blog` page.
- Images can be embedded with standard Markdown or with the `figure.html` include for captioned figures.

---

This website is built using the [Lab Website Template](https://github.com/greenelab/lab-website-template) (DOI: [10.5281/zenodo.17228741](https://doi.org/10.5281/zenodo.17228741)) — if you are looking to create your own lab website, start there.
