# Screening Phase

## Files

| File | Purpose |
|------|---------|
| `screening_criteria.md` | Formal inclusion/exclusion criteria with edge case rules |
| `results/deduplicated.csv` | All 545 unique papers merged across sources |
| `results/screening_decisions.csv` | Multi-coder screening database |
| `results/prisma_counts.json` | PRISMA flow numbers |

## Multi-Coder Workflow

`screening_decisions.csv` supports multiple coders:

1. Each row = one paper screened by one coder
2. Papers already coded from prior pilot work have `coder = AI_prior`
3. AI screening adds rows with `coder = AI_screen`
4. Human coders add their own rows with their initials
5. The `abstract` column contains the full abstract for every row

### Adding Your Screening

Open `screening_decisions.csv` and add a new row for any paper you want to screen:
- Copy the `screen_id`, `doi`, `title`, etc. from the existing row
- Set `coder` to your initials
- Set `decision` to INCLUDE, EXCLUDE, or UNSURE
- Set `exclusion_code` if excluding (see screening_criteria.md)
- Add notes explaining your reasoning
