# N2 — Substantive Coding Rubric

**Stage:** Level N2 — content analysis of news articles confirmed at N1 to be coverage of one or more ABCD papers.

**Scope:** Each linked news article is coded on the dimensions below to characterize how the original empirical finding is translated to public-facing media. The goal is to compare what the article says about the paper to what the paper itself reports.

**Approach:** Pre-specified rubric, double-coded (AI × 4 + human resolver), inter-rater reliability (Cohen's κ) reported per code. Same pipeline structure as Stage 2 (full-text eligibility) screening.

---

## Coding dimensions

Each article × paper-mapping is coded on the following 14 dimensions.

### A — Reporting fidelity (effect, sample, design)

#### A1. Effect size disclosed
- `Y` — article reports a numeric effect size (β, OR, %, mean diff, etc.)
- `N` — article describes association without numeric magnitude

#### A2. Sample size disclosed
- `Y` — article reports the n analyzed
- `N` — article describes sample without n (or only refers to "ABCD's 11,000 children" without specifying analytic n)

#### A3. Study design correctly characterized
- `Faithful` — article correctly describes design (cross-sectional, longitudinal, etc.)
- `Imprecise` — article uses ambiguous language (e.g., "tracked over time" for cross-sectional)
- `Misrepresents` — article asserts a design feature the paper does not have (e.g., calling cross-sectional analysis "longitudinal")
- `Not stated` — article does not address design

### B — Causal-language drift

#### B1. Causal verbs (count)
Count of explicitly causal verbs in body text referring to the smartphone/social media → outcome relationship: "causes," "causing," "leads to," "triggers," "results in," "drives," "produces," "makes [outcome] worse," "affects" (when used causally).

#### B2. Associational verbs (count)
Count of associational verbs: "associated with," "linked to," "correlated with," "related to," "predicts" (when used in the regression sense).

#### B3. Causal-upgrade vs. paper claim
- `None` — article's causal language matches or is more conservative than paper's
- `Mild` — article uses softly causal language ("affects," "shapes") where paper used purely associational language
- `Strong` — article asserts strong causation ("causes," "triggers") where paper used associational language
- `Misleading` — article asserts causation contrary to explicit paper caveats

### C — Magnitude framing

#### C1. Magnitude language
- `Faithful` — article's framing of effect size matches the paper (e.g., "modest association")
- `Amplified` — article uses stronger framing than paper (e.g., paper: "small effect," article: "significant impact")
- `Alarmist` — article uses risk-amplifying framing ("alarming," "crisis," "epidemic," "harmful," "damaging") not present in or stronger than paper
- `Minimized` — article downplays effect relative to paper (rare in this corpus)

#### C2. Limitations mentioned
- `Y` — article notes at least one of: study design limits causal inference, modest effect size, single-cohort findings, self-report measurement, etc.
- `N` — article presents findings without limitations

### D — Policy framing

#### D1. Policy advocacy by article
- `Y` — article (in its own voice, not via author quote) advocates for policy changes (age limits, bans, regulation, school policies, parental controls, screen time guidelines, etc.)
- `N` — article does not advocate for policy

#### D2. Policy advocacy by quoted source
- `Y` — article quotes the paper's authors or external experts advocating for policy
- `N` — no such quotes

#### D3. Policy stance fidelity
- `Faithful` — policy implications match paper's discussion section
- `Extends` — policy advocacy in article goes beyond what the paper recommended
- `Contradicts` — policy advocacy contradicts paper's own caveats (e.g., paper says "too early to recommend policy"; article calls for ban)

### E — Source attribution

#### E1. Paper authors quoted
- `Y` / `N`

#### E2. Outside expert quoted
- `Y` (independent researcher commenting on the study) / `N`

#### E3. Critical perspective included
- `Y` — article includes any critical or skeptical perspective on the findings
- `N` — article presents findings uncritically

---

## Output

`N2-scoring.csv` with one row per (article × paper) mapping. Columns:

| Column | Source |
|---|---|
| `article_id` | from N1 |
| `paper_id` | from N1 |
| `outlet` | search results |
| `title`, `url`, `published_date` | search results |
| `A1_effect_disclosed`, `A2_sample_disclosed`, `A3_design` | coder |
| `B1_causal_verbs`, `B2_associational_verbs`, `B3_causal_upgrade` | coder |
| `C1_magnitude`, `C2_limitations` | coder |
| `D1_policy_article`, `D2_policy_quoted`, `D3_policy_fidelity` | coder |
| `E1_authors_quoted`, `E2_outside_quoted`, `E3_critical` | coder |
| `coder_id` | C1–C4 / C5_resolver |
| `confidence` | 0–1 |
| `evidence` | direct quotes supporting the codes |

---

## Inter-rater reliability

Each article is coded by 4 independent AI coders using identical input (full article text where accessible; otherwise headline + lead + snippet) and the rubric above. Cohen's κ is reported per code, both pairwise and pooled. Disagreements (any 4-way split) are adjudicated by a single human resolver.

Per code, expected baseline κ ≥ 0.70 (substantial agreement) for the binary codes; ≥ 0.60 for the ordinal/categorical codes (causal-upgrade, magnitude, design fidelity).

---

## Analysis (planned)

Once N2-scoring.csv is complete, planned analyses:

1. **Aggregate prevalence**: % of articles overclaiming causality, advocating policy, omitting effect size, etc.
2. **By outlet type**: tabloid / broadsheet / wire service / specialty health press / academic press release.
3. **By paper topic**: depression, sleep, cognition, brain imaging, etc.
4. **By paper effect size**: do articles overclaim more for papers with smaller effects?
5. **Paper → article delta**: for each paper, compare the article's framing to the paper's own conclusions section.
