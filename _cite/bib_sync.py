#!/usr/bin/env python3
"""
Sync sources.yaml from a Zotero BibTeX export.

Usage:
    python _cite/bib_sync.py [--bib db/my-publications.bib] [--author "Das, Pritam"]

- Reads the bib file, finds all entries where --author appears.
- Updates _data/sources.yaml: adds new DOIs, removes absent ones.
- Preserves existing custom fields (image, buttons, description, tags).
- Entries without a DOI are skipped.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml


def extract_field(entry: str, field: str) -> str:
    """Extract a bib field value, handling nested braces."""
    m = re.search(rf"{field}\s*=\s*\{{", entry, re.IGNORECASE)
    if not m:
        return ""
    start = m.end()
    depth = 1
    i = start
    while i < len(entry) and depth > 0:
        if entry[i] == "{":
            depth += 1
        elif entry[i] == "}":
            depth -= 1
        i += 1
    return entry[start : i - 1].strip()


def parse_bib(bib_path: Path) -> list[dict]:
    """Return list of {doi, title, year, entry_type} for each bib entry."""
    text = bib_path.read_text(encoding="utf-8")
    entries = re.split(r"\n(?=@)", text)
    results = []
    for entry in entries:
        doi_m = re.search(r"doi\s*=\s*\{([^}]+)\}", entry, re.IGNORECASE)
        if not doi_m:
            continue
        doi = doi_m.group(1).strip()
        title_m = re.search(r"title\s*=\s*\{([^}]+)\}", entry, re.IGNORECASE)
        year_m = re.search(r"year\s*=\s*\{([^}]+)\}", entry, re.IGNORECASE)
        type_m = re.match(r"@(\w+)\{", entry)
        results.append({
            "doi": doi,
            "title": title_m.group(1) if title_m else "",
            "year": year_m.group(1) if year_m else "0",
            "entry_type": type_m.group(1).lower() if type_m else "article",
            "raw": entry,
        })
    return results


JOURNAL_TYPES = {"article", "incollection", "inbook", "book", "phdthesis"}


def filter_author(entries: list[dict], author: str, journal_only: bool = True) -> list[dict]:
    """Keep only entries where author string appears in the author field."""
    out = []
    for e in entries:
        if journal_only and e["entry_type"] not in JOURNAL_TYPES:
            continue
        authors = extract_field(e["raw"], "author")
        if author.lower() in authors.lower():
            out.append(e)
    return out


def load_sources(sources_path: Path) -> list[dict]:
    text = sources_path.read_text(encoding="utf-8")
    return yaml.safe_load(text) or []


def save_sources(sources_path: Path, entries: list[dict]) -> None:
    # Preserve header comment
    header = "# Publications for RIVER Lab\n# The cite pipeline resolves each DOI and pulls metadata automatically.\n\n"
    body = yaml.dump(entries, allow_unicode=True, sort_keys=False, default_flow_style=False)
    sources_path.write_text(header + body, encoding="utf-8")


def normalize_doi(doi: str) -> str:
    return doi.lower().removeprefix("doi:").strip()


def sync(bib_path: Path, sources_path: Path, author: str, dry_run: bool = False) -> None:
    bib_entries = parse_bib(bib_path)
    my_entries = filter_author(bib_entries, author, journal_only=True)
    bib_dois = {normalize_doi(e["doi"]) for e in my_entries}

    sources = load_sources(sources_path)
    existing = {normalize_doi(e["id"].removeprefix("doi:")): e for e in sources}
    existing_dois = set(existing.keys())

    added = bib_dois - existing_dois
    removed = existing_dois - bib_dois

    if removed:
        print(f"Removing {len(removed)} entries no longer in bib:")
        for doi in sorted(removed):
            print(f"  - {doi}")
    if added:
        print(f"Adding {len(added)} new entries from bib:")
        for doi in sorted(added):
            print(f"  + {doi}")
    if not added and not removed:
        print("sources.yaml is already up to date.")
        return

    if dry_run:
        return

    # Build updated list: keep existing (in bib), add new
    updated = []
    for doi, entry in existing.items():
        if doi in bib_dois:
            updated.append(entry)

    for e in my_entries:
        doi = normalize_doi(e["doi"])
        if doi in added:
            updated.append({"id": f"doi:{doi}"})

    # Re-sort by year descending (best effort — cite pipeline will use publication date)
    bib_year = {normalize_doi(e["doi"]): e["year"] for e in my_entries}
    updated.sort(key=lambda x: bib_year.get(normalize_doi(x["id"].removeprefix("doi:")), "0"), reverse=True)

    save_sources(sources_path, updated)
    print("sources.yaml updated.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bib", default="db/my-publications.bib", help="Path to BibTeX file")
    parser.add_argument("--author", default="Das, Pritam", help="Author name to filter on")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    bib_path = repo_root / args.bib
    sources_path = repo_root / "_data" / "sources.yaml"

    if not bib_path.exists():
        print(f"Error: bib file not found at {bib_path}", file=sys.stderr)
        sys.exit(1)

    sync(bib_path, sources_path, args.author, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
