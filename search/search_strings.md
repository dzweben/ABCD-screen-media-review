# Exact Search Strings

Copy-paste ready for each database. Last executed: 2026-04-06.

## PubMed/MEDLINE

Paste into PubMed Advanced Search or use with E-utilities API:

```
("Adolescent Brain Cognitive Development"[tiab] OR "ABCD Study"[tiab] OR "ABCD cohort"[tiab] OR "ABCD sample"[tiab] OR "ABCD dataset"[tiab] OR "ABCD participants"[tiab]) AND ("social media"[tiab] OR "Social Media"[mh] OR "smartphone"[tiab] OR "Smartphone"[mh] OR "smart phone"[tiab] OR "mobile phone"[tiab] OR "cell phone"[tiab] OR "Cell Phone"[mh] OR "internet use"[tiab] OR "internet addiction"[tiab] OR "Internet Addiction Disorder"[mh] OR "texting"[tiab] OR "text messaging"[tiab] OR "Text Messaging"[mh] OR "problematic phone"[tiab] OR "problematic smartphone"[tiab] OR "problematic social media"[tiab] OR "problematic internet"[tiab] OR "digital media"[tiab] OR "screen media"[tiab] OR "screen time"[tiab] OR "Screen Time"[mh] OR "media use"[tiab] OR "phone use"[tiab] OR "mobile device"[tiab] OR "social networking"[tiab] OR "Social Networking"[mh] OR "Instagram"[tiab] OR "TikTok"[tiab] OR "Snapchat"[tiab] OR "Facebook"[tiab] OR "YouTube"[tiab] OR "Twitter"[tiab] OR "video game"[tiab] OR "Video Games"[mh] OR "gaming"[tiab] OR "television"[tiab] OR "Television"[mh] OR "screen use"[tiab] OR "online"[tiab])
```

**Result:** 171 records

## OpenAlex API

Two-step programmatic search:

**Step 1 — Retrieve all ABCD Study papers:**
```
GET https://api.openalex.org/works?filter=title_and_abstract.search:Adolescent%20Brain%20Cognitive%20Development&per_page=200&cursor=*

GET https://api.openalex.org/works?filter=title_and_abstract.search:ABCD%20Study%20adolescent%20brain&per_page=200&cursor=*
```

**Step 2 — Post-filter for screen/media keywords in title+abstract:**

Keywords: screen time, social media, smartphone, smart phone, mobile phone, cell phone, internet use, internet addiction, texting, text messaging, digital media, screen media, media use, phone use, screen use, video game, gaming, television, social networking, online, problematic phone, problematic smartphone, problematic social media, problematic internet, instagram, tiktok, snapchat, facebook, youtube, twitter, cyberbullying

**Additional filter:** Year >= 2015

**Result:** 450 records

## ABCD Study Website

**Source:** https://abcdstudy.org/publications/

**Method:** Programmatic scrape of JSON-LD structured data containing all ~1,443 publications, followed by keyword filtering against title and PubMed-retrieved abstracts using the same keyword set as the database searches.

**Result:** 101 candidate records
