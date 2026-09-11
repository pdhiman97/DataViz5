# Project Ledger: loksabha-questions

| Stage | Skill | Model | Status | Decisions / Evidence | Outputs |
|-------|-------|-------|--------|---------------------|---------|
| Brief | Data Vizard | claude-sonnet-4-6 | Completed | Narrative posture: Balanced-to-data-art-led scrollytelling. Question: "Do MPs from same state share parliamentary priorities?" | Project framing |
| Curation | Data Curator | claude-sonnet-4-6 | Completed | Used uploaded CSV: `mp_17th_loksabha_questions_matrix.csv`. Merged 5 duplicate/secondary columns (AYUSH/Ayush, Micro/MSME, Statistics duplicates, Consumer Affairs, Heavy Industries). Excluded 60 MPs with zero questions. Final: 499 MPs, 58 sectors, 36 states (26 with 2+ MPs). | `data/loksabha-questions/raw/mp_17th_loksabha_questions_matrix.csv`, `data/loksabha-questions/curated/viz_data.json` |
| Analysis | Data Analyst | claude-sonnet-4-6 | Completed | Key findings: (1) Health dominates nationally at 7.4%. (2) State patterns exist but within-state variation typically > between-state variation. (3) Some states are distinctively cohesive: Tripura, Kerala, Tamil Nadu. (4) Most distinctive: Manipur (HRD +12.6pp), J&K (Home Affairs +9.3pp), Himachal (Road Transport +8.9pp). (5) Party affiliation adds independent signal — AITC overindexes Communications+Rural Dev; JD(U) on Railways+Jal Shakti; YSRCP on Finance+Fisheries. | `eda.py` analysis, `curated_analysis.json` |
| Narrative | Narrator | claude-sonnet-4-6 | Completed | Posture: Balanced (visual carries most meaning, selective language). Language load: guided narrative. Five-chapter progression: National Beat → State Signatures → Within & Between → Exceptional Voices → Party Lines → Coda. | Narrative structure embedded in HTML |
| Design | Designer | claude-sonnet-4-6 | Completed | Aesthetic family: Neo-noir editorial. Typography: EB Garamond + Space Mono. Color system: saffron-ember (over-representation) ↔ ice-blue (under-representation) on deep ink ground. Spatial archetype: Scrollytelling broadsheet. Rendering: D3.js SVG + Canvas hero animation. Interaction: hover tooltips, click-locked state details, sector-switcher, animated chart entry. | `outcome/loksabha-questions/` |
| Build | Designer | claude-sonnet-4-6 | Draft built | Self-contained HTML (919 KB). `index.html` with inlined CSS, JS, and VIZ_DATA. External: D3@7 CDN, Google Fonts. 5 chapters: animated hero canvas, horizontal bar chart, state heatmap (diverging), scatter plot (cohesion vs. distinctiveness), sector focus bars with MP dots, party fingerprint heatmap, coda with 4 key findings. | `outcome/loksabha-questions/index.html` |
| Critique | Critic | claude-sonnet-4-6 | Completed | Pass with cuts. Main findings applied: no dashboard grammar, no KPI strips, local tooltip reveals, neo-noir palette consistent, bar animations tied to IntersectionObserver, within-state MP dots in sector bars, no generic editorial copy. Remaining: browser verification only on local file (no server). |  |

## Project Storage

```
data/loksabha-questions/raw/mp_17th_loksabha_questions_matrix.csv
data/loksabha-questions/curated/viz_data.json
outcome/loksabha-questions/index.html  (self-contained, 919 KB)
outcome/loksabha-questions/styles.css  (separate, for maintenance)
outcome/loksabha-questions/script.js   (separate, for maintenance)
outcome/loksabha-questions/data.js     (minified data variable)
project-ledgers/loksabha-questions.md
```

## Key Analytical Findings

1. **State patterns are real but weak**: MPs from the same state show more similarity than random, but within-state MP-to-MP variation is typically larger than between-state variation for most sectors.
2. **Cohesive states**: Tripura, Kerala, Tamil Nadu, Maharashtra. **Scattered states**: Punjab, West Bengal, Uttar Pradesh.
3. **Most distinctive states**: Manipur (HRD), J&K (Home Affairs), Himachal Pradesh (Road Transport), Dadra & Nagar Haveli (Tribal Affairs).
4. **Party adds a layer**: AITC, JD(U), and YSRCP show party fingerprints that cut across state patterns.
5. **Health is universal**: No state or party de-prioritizes Health below 4% — it's the one true parliamentary floor.

## Narrative Posture

- `posture`: Balanced
- `language_load`: guided narrative
- `text_budget`: Title + eyebrow + 5 chapter bodies + coda grid (4 cards) + tooltip copy
- `focal_point`: State-to-state deviation heatmap (Chapter 2)
- `default_to_avoid`: Dashboard-first layout, generic bar charts without interaction, summary KPI strips

## Status: Draft built (verification on local file; browser-verified opening confirmed)
