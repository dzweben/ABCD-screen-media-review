#!/usr/bin/env python3
"""
PubMed/MEDLINE Boolean search via NCBI E-utilities API.

Searches for ABCD Study papers with screen/digital media exposures.
No API key required (rate-limited to 3 requests/sec without key).

Output: search/results/pubmed_results.csv + pubmed_search_log.json
"""

import sys, time, json, csv, xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
from pathlib import Path
from datetime import date

# Config
EMAIL = "daniel.zweben@temple.edu"
OUT_DIR = Path(__file__).parent / "results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Boolean query — two blocks combined with AND
BLOCK_1 = (
    '"Adolescent Brain Cognitive Development"[tiab] OR "ABCD Study"[tiab] OR '
    '"ABCD cohort"[tiab] OR "ABCD sample"[tiab] OR "ABCD dataset"[tiab] OR '
    '"ABCD participants"[tiab]'
)

BLOCK_2 = (
    '"social media"[tiab] OR "Social Media"[mh] OR '
    '"smartphone"[tiab] OR "Smartphone"[mh] OR '
    '"smart phone"[tiab] OR "mobile phone"[tiab] OR '
    '"cell phone"[tiab] OR "Cell Phone"[mh] OR '
    '"internet use"[tiab] OR "internet addiction"[tiab] OR "Internet Addiction Disorder"[mh] OR '
    '"texting"[tiab] OR "text messaging"[tiab] OR "Text Messaging"[mh] OR '
    '"problematic phone"[tiab] OR "problematic smartphone"[tiab] OR '
    '"problematic social media"[tiab] OR "problematic internet"[tiab] OR '
    '"digital media"[tiab] OR "screen media"[tiab] OR '
    '"screen time"[tiab] OR "Screen Time"[mh] OR '
    '"media use"[tiab] OR "phone use"[tiab] OR "mobile device"[tiab] OR '
    '"social networking"[tiab] OR "Social Networking"[mh] OR '
    '"Instagram"[tiab] OR "TikTok"[tiab] OR "Snapchat"[tiab] OR '
    '"Facebook"[tiab] OR "YouTube"[tiab] OR "Twitter"[tiab] OR '
    '"video game"[tiab] OR "Video Games"[mh] OR "gaming"[tiab] OR '
    '"television"[tiab] OR "Television"[mh] OR '
    '"screen use"[tiab] OR "online"[tiab]'
)

QUERY = f"({BLOCK_1}) AND ({BLOCK_2})"
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed():
    print(f"Searching PubMed with {len(QUERY)}-char query...")

    # Step 1: Get count
    url = (f"{BASE_URL}/esearch.fcgi?db=pubmed&term={quote_plus(QUERY)}"
           f"&retmode=json&retmax=0&tool=abcd-review&email={EMAIL}")
    resp = json.loads(urlopen(Request(url), timeout=30).read())
    count = int(resp["esearchresult"]["count"])
    print(f"Total hits: {count}")

    # Step 2: Get all PMIDs
    time.sleep(0.5)
    url2 = (f"{BASE_URL}/esearch.fcgi?db=pubmed&term={quote_plus(QUERY)}"
            f"&retmode=json&retmax={count}&tool=abcd-review&email={EMAIL}")
    resp2 = json.loads(urlopen(Request(url2), timeout=30).read())
    pmids = resp2["esearchresult"]["idlist"]
    print(f"Retrieved {len(pmids)} PMIDs")

    # Step 3: Fetch full records in batches
    all_papers = []
    batch_size = 200
    for start in range(0, len(pmids), batch_size):
        batch = pmids[start:start + batch_size]
        time.sleep(0.4)
        url3 = (f"{BASE_URL}/efetch.fcgi?db=pubmed&id={','.join(batch)}"
                f"&rettype=xml&retmode=xml&tool=abcd-review&email={EMAIL}")
        xml_data = urlopen(Request(url3), timeout=60).read()
        root = ET.fromstring(xml_data)

        for article in root.findall(".//PubmedArticle"):
            paper = parse_article(article)
            all_papers.append(paper)

        print(f"  Fetched {min(start + batch_size, len(pmids))}/{len(pmids)}")

    return all_papers, count


def parse_article(article):
    pmid = article.findtext(".//PMID", "")
    title = article.findtext(".//ArticleTitle", "")

    # Authors
    authors = []
    for auth in article.findall(".//Author"):
        last = auth.findtext("LastName", "")
        fore = auth.findtext("ForeName", "")
        if last:
            authors.append(f"{last}, {fore}" if fore else last)

    # Journal + year
    journal = article.findtext(".//Journal/Title", "")
    year = article.findtext(".//PubDate/Year", "")
    if not year:
        md = article.findtext(".//PubDate/MedlineDate", "")
        if md:
            year = md[:4]

    # DOI
    doi = ""
    for aid in article.findall(".//ArticleId"):
        if aid.get("IdType") == "doi":
            doi = aid.text or ""
            break
    if not doi:
        for eid in article.findall(".//ELocationID"):
            if eid.get("EIdType") == "doi":
                doi = eid.text or ""
                break

    # Abstract
    abstract_parts = []
    for atext in article.findall(".//AbstractText"):
        label = atext.get("Label", "")
        text = "".join(atext.itertext())
        abstract_parts.append(f"{label}: {text}" if label else text)
    abstract = " ".join(abstract_parts)

    # Pub types + MeSH
    pub_types = [pt.text for pt in article.findall(".//PublicationType") if pt.text]
    mesh = [m.findtext("DescriptorName", "") for m in article.findall(".//MeshHeading")]

    return {
        "pmid": pmid, "doi": doi, "title": title,
        "authors": "; ".join(authors),
        "first_author": authors[0] if authors else "",
        "year": year, "journal": journal, "abstract": abstract,
        "pub_types": "; ".join(pub_types),
        "mesh_terms": "; ".join(mesh),
    }


def main():
    papers, count = search_pubmed()

    # Write CSV
    csv_path = OUT_DIR / "pubmed_results.csv"
    fields = ["pmid", "doi", "title", "authors", "first_author", "year",
              "journal", "abstract", "pub_types", "mesh_terms"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(papers)

    # Write log
    log = {
        "database": "PubMed/MEDLINE",
        "search_date": str(date.today()),
        "query": QUERY,
        "total_hits": count,
        "records_retrieved": len(papers),
        "tool": "NCBI E-utilities API",
        "email": EMAIL,
    }
    with open(OUT_DIR / "pubmed_search_log.json", "w") as f:
        json.dump(log, f, indent=2)

    print(f"\nDone! {len(papers)} papers -> {csv_path}")


if __name__ == "__main__":
    main()
