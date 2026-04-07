# AI Screening Prompt

This document records the exact prompt used for AI title/abstract screening so a second AI coder can use an identical or modified prompt for inter-rater reliability.

## Coder ID: `AI_coder1`
## Model: Claude Opus 4.6
## Date: 2026-04-07

## Prompt

For each paper, the AI is given: title, abstract, journal, year, and first author.

The AI applies these criteria:

### Inclusion (ALL required)
- IC1: Uses ABCD Study data
- IC2: Exposure includes smartphone, social media, internet, texting, or problematic use of these
- IC3: Original empirical findings
- IC4: Peer-reviewed journal

### Exclusion (ANY triggers)
- EC1: Not ABCD data
- EC2_tv_only: Exposure exclusively TV
- EC2_gaming_only: Exposure exclusively video games
- EC2_aggregate: Only aggregate screen time, no modality breakdown
- EC3_review: Review/editorial/commentary/protocol (no original ABCD analysis)
- EC4_abstract: Conference abstract only
- EC5_duplicate: Duplicate publication

### Decision format
For each paper, output:
- `decision`: INCLUDE, EXCLUDE, or UNSURE
- `exclusion_code`: If EXCLUDE, which EC code. If multiple, list primary.
- `notes`: 1-2 sentence explanation of reasoning. Must reference specific title/abstract content.
- `confidence`: high, medium, or low

### Edge case rules
- Papers with "screen time" in title that use ABCD STQ subscales: INCLUDE (modalities available)
- Papers where screen time is the OUTCOME: INCLUDE but note "screen_time_as_outcome"
- Papers with ABCD + non-ABCD samples: INCLUDE if ABCD results reported separately
- "Online" without modality specification: UNSURE unless abstract clarifies

## Inter-Rater Reliability Protocol

1. AI_coder1 screens all 545 papers (94 pre-included, 451 new)
2. A second coder (AI_coder2 or human) independently screens a random subset or all papers
3. Agreement is calculated on the `decision` field (INCLUDE/EXCLUDE)
4. UNSURE papers are resolved by discussion or full-text review
5. Cohen's kappa reported for the overlapping set
