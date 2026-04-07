#!/usr/bin/env python3
"""
Phase 1A: Scrape all publications from abcdstudy.org
Extracts JSON-LD ItemList containing all ~1,443 papers.
Outputs: data/raw/all_publications.json, data/ABCD_SM_Review_Codebook.xlsx (tab 1A)
"""

import json
import re
import csv
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
LOG_DIR = BASE_DIR / "logs"

def fetch_publications_page():
    """Fetch the publications page HTML."""
    url = "https://abcdstudy.org/publications/"
    print(f"Fetching {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    resp = requests.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    print(f"  Got {len(resp.text)} bytes")
    return resp.text

def extract_jsonld(html):
    """Extract JSON-LD data from the page."""
    soup = BeautifulSoup(html, "lxml")
    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            data = json.loads(script.string)
            # Could be a list of JSON-LD objects
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "ItemList":
                        return item
            elif isinstance(data, dict):
                if data.get("@type") == "ItemList":
                    return data
                # Check nested @graph
                if "@graph" in data:
                    for item in data["@graph"]:
                        if item.get("@type") == "ItemList":
                            return item
        except json.JSONDecodeError:
            continue

    return None

def parse_authors(author_data):
    """Parse author array into semicolon-delimited string."""
    if not author_data:
        return ""
    if isinstance(author_data, dict):
        return author_data.get("name", "")
    authors = []
    for a in author_data:
        if isinstance(a, dict):
            name = a.get("name", "")
            if name:
                authors.append(name)
        elif isinstance(a, str):
            authors.append(a)
    return "; ".join(authors)

def extract_doi(url):
    """Extract DOI from a URL, or return empty string."""
    if not url:
        return "", "unknown"
    if "doi.org/" in url:
        doi = url.split("doi.org/", 1)[1].rstrip("/")
        return doi, "DOI"
    if "pubmed.ncbi" in url or "ncbi.nlm.nih.gov/pubmed" in url:
        return "", "PubMed"
    return "", "other"

def parse_items(itemlist):
    """Parse ItemList into structured records."""
    elements = itemlist.get("itemListElement", [])
    records = []

    for i, elem in enumerate(elements):
        item = elem if elem.get("@type") == "ScholarlyArticle" else elem.get("item", elem)

        title = item.get("name", "").strip()
        year = item.get("datePublished", "")
        url = item.get("url", "")

        # Journal
        journal_data = item.get("isPartOf", {})
        if isinstance(journal_data, dict):
            journal = journal_data.get("name", "")
        else:
            journal = str(journal_data)

        # Authors
        authors = parse_authors(item.get("author", []))

        # DOI
        doi, url_type = extract_doi(url)

        records.append({
            "row_id": i + 1,
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": year,
            "doi": doi,
            "url": url,
            "url_type": url_type,
            "coder": "AI",
            "date_coded": datetime.now().strftime("%Y-%m-%d"),
            "notes": ""
        })

    return records

def save_json(records, path):
    """Save records as JSON."""
    with open(path, "w") as f:
        json.dump(records, f, indent=2)
    print(f"  Saved {len(records)} records to {path}")

def save_csv(records, path):
    """Save records as CSV."""
    if not records:
        return
    keys = records[0].keys()
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
    print(f"  Saved {len(records)} records to {path}")

def save_excel_tab(records, wb_path):
    """Create or update the Excel workbook with tab 1A."""
    wb = Workbook()
    ws = wb.active
    ws.title = "1A_All_Publications"

    if not records:
        wb.save(wb_path)
        return

    # Header
    headers = list(records[0].keys())
    ws.append(headers)

    # Bold headers
    from openpyxl.styles import Font
    for cell in ws[1]:
        cell.font = Font(bold=True)

    # Data
    for rec in records:
        ws.append([rec[h] for h in headers])

    # Auto-width (approximate)
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, min(len(str(cell.value)), 60))
        ws.column_dimensions[col_letter].width = max_length + 2

    wb.save(wb_path)
    print(f"  Saved Excel workbook with tab '1A_All_Publications' to {wb_path}")

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Fetch and parse
    html = fetch_publications_page()

    # Save raw HTML for debugging
    raw_html_path = RAW_DIR / "publications_page.html"
    with open(raw_html_path, "w") as f:
        f.write(html)

    itemlist = extract_jsonld(html)
    if not itemlist:
        print("ERROR: Could not find JSON-LD ItemList on the page!")
        print("Trying alternative: parsing HTML directly...")
        # Fallback: try to parse publication entries from HTML
        return fallback_html_parse(html)

    n_elements = len(itemlist.get("itemListElement", []))
    print(f"  Found ItemList with {n_elements} elements")

    records = parse_items(itemlist)
    print(f"  Parsed {len(records)} publication records")

    # Save outputs
    save_json(records, RAW_DIR / "all_publications.json")
    save_csv(records, RAW_DIR / "all_publications.csv")
    save_excel_tab(records, DATA_DIR / "ABCD_SM_Review_Codebook.xlsx")

    # Summary stats
    years = {}
    for r in records:
        y = r["year"]
        years[y] = years.get(y, 0) + 1
    print(f"\n  Year distribution:")
    for y in sorted(years.keys()):
        print(f"    {y}: {years[y]}")

    doi_count = sum(1 for r in records if r["doi"])
    print(f"\n  {doi_count}/{len(records)} have DOIs")
    print(f"  {len(records) - doi_count} have PubMed or other URLs only")

    return records

def fallback_html_parse(html):
    """Fallback: parse publications from HTML structure if JSON-LD fails."""
    soup = BeautifulSoup(html, "lxml")
    # Try to find publication entries in the HTML
    # This is a fallback — structure may vary
    print("Fallback HTML parsing not yet implemented. Check the page structure.")
    return []

if __name__ == "__main__":
    records = main()
    print(f"\nDone. Total publications: {len(records) if records else 0}")
