# Screening Criteria

## Inclusion Criteria (ALL must be met)

| Code | Criterion |
|------|-----------|
| **IC1** | Uses data from the Adolescent Brain Cognitive Development (ABCD) Study |
| **IC2** | Primary or secondary exposure is smartphone use, social media use, internet use, texting/text messaging, or problematic/compulsive use of these technologies |
| **IC3** | Reports original empirical findings (quantitative analysis of ABCD data) |
| **IC4** | Published in a peer-reviewed journal |

## Exclusion Criteria (ANY triggers exclusion)

| Code | Criterion | Example |
|------|-----------|---------|
| **EC1** | Not ABCD Study data | Paper uses MTF, NHANES, or other cohort |
| **EC2_tv_only** | Exposure is exclusively television viewing | No smartphone/social media/internet component |
| **EC2_gaming_only** | Exposure is exclusively video gaming | No smartphone/social media/internet component |
| **EC2_aggregate** | Only aggregate "screen time" reported without modality breakdown | Total hours/day with no subscale results |
| **EC3_review** | Review, editorial, commentary, protocol, meta-analysis, or methods paper without original ABCD analysis | Systematic review of screen time literature; editorial about ABCD data |
| **EC4_abstract** | Conference abstract only (no full-text peer-reviewed article) | Poster presentation abstract |
| **EC5_duplicate** | Duplicate publication of the same study | Same analysis published in two venues |

## Edge Case Decision Rules

### Papers using the ABCD Screen Time Questionnaire (STQ)

The STQ measures multiple modalities including social media, texting, TV, and video games.

- **INCLUDE** if the paper reports results for individual STQ modalities that include smartphone/social media/internet/texting, even if it also reports TV/gaming
- **INCLUDE** if the paper reports only aggregate total screen time BUT the methods indicate STQ subscales were available (can extract modality-specific effects at full-text coding)
- **EXCLUDE (EC2_aggregate)** if the paper reports only aggregate screen time and there is no indication that modality-specific data was available or analyzed

### Multiple exposures

A paper studying gaming AND social media using ABCD STQ subscales is **INCLUDED** because the target exposure (social media) is present. The gaming component does not trigger exclusion.

### Problematic use measures

Papers using SMAQ (Social Media Addiction Questionnaire), problematic smartphone use scales, or similar problematic use measures are **INCLUDED** regardless of whether duration is also measured.

### Passive sensing / EARS data

Papers using ABCD's Effortless Assessment Research System (EARS) app-logged phone usage data are **INCLUDED** as smartphone/internet use measures.

### Screen time as outcome (not exposure)

Papers where screen time is the **outcome** predicted by other variables (e.g., ACEs predicting screen time) are **INCLUDED** but flagged during full-text coding as "reversed directionality." They contribute to understanding measurement and correlates even if the causal arrow points the other direction.

### "Online" in abstract only

If a paper mentions "online activity" but the actual measured exposure is total screen time without modality breakdown, **EXCLUDE (EC2_aggregate)** at full-text stage.

## Screening Instructions for Coders

1. Read the **title** first. If it clearly meets all IC and no EC, mark INCLUDE.
2. If unclear from title, read the **abstract**.
3. If still unclear after abstract, mark **UNSURE** with a note explaining the ambiguity.
4. Record your decision, exclusion code (if applicable), notes, and confidence level.
5. UNSURE papers are resolved at full-text review or by consensus between coders.

## Confidence Levels

- **high**: Decision is clear from title/abstract alone
- **medium**: Required reading the full abstract carefully; reasonable people might disagree
- **low**: Genuinely ambiguous; needs full-text review or second coder
