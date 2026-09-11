# parliamentary-mic-check

**Project:** The Parliamentary Mic Check — 17th Lok Sabha Decoded
**Data Source:** PRS India MP Track (17th Lok Sabha, 2019–2024)
**Narrative Posture:** Explanatory
**Artifact Mode:** Hybrid (aggregate analysis + record-by-record MP exploration)

---

## Project Ledger

| Stage | Skill | Model | Status | Decisions / Evidence | Outputs |
| --- | --- | --- | --- | --- | --- |
| Brief | data-vizard | claude-sonnet-4-6 | Completed | User provided full system prompt with act structure, narrative framework, and dataset CSV | Project brief captured |
| Curation | data-curator | claude-sonnet-4-6 | Completed | CSV profiled: 559 MPs, 63 ministry columns, 1,00,030 total questions. 8 thematic categories derived. Archetype classification via debates/questions/diversity (Shannon entropy) | `data/debates_macro_summary.json`, `data/mp_master_dataset.json` |
| Analysis | data-analyst | claude-sonnet-4-6 | Completed | Key findings: Health+Welfare=21.5%, State+Special=21.6%, top 10% MPs=42% of debates, 440/559 MPs are Silent Observers, max 1261 debates (1 MP) | Evidence brief embedded in narrative |
| Narrative | narrator | claude-sonnet-4-6 | Completed | Explanatory posture. 5-act structure: Hook → Breakdown → Party Playbooks → Participation Gap → MP Explorer → Verdict. Language load: moderate, editorial tone | Narrative embedded in HTML step copy |
| Design | designer | claude-sonnet-4-6 | Completed | Direction chosen: Newspaper Broadsheet meets Neo-noir aesthetic. Dark mode (#0A0F1E). Sticky 40/60 scrollytelling layout. D3.js beeswarm + CSS waffle + party bars. Avoided: dashboard-grammar, KPI strips, generic hero+card shell | `index.html`, `styles.css`, `script.js`, `data_embedded.js` |
| Build | designer | claude-sonnet-4-6 | Draft built | Files created and opened in browser. Embedded data to bypass file:// CORS. CSS var bug fixed (--c-regional → --p-regional). D3 v7 force simulation for beeswarm. | `outcome/parliamentary-mic-check/` |
| Critic review | critic | — | Pending | Final critique pass not yet run | — |

---

## Curation Notes

- **Raw file:** `mp_17th_loksabha_questions_matrix.csv` — 559 rows × 76 columns
- **Ministry columns:** 63 ministry-level question counts per MP
- **Caveats:**
  - `attendance_pct` has some `N/A` values (handled gracefully)
  - Questions matrix is a flat count per ministry, not a transcript of debates
  - "Debate count" from PRS India measures appearances, not speaking minutes
  - Archetype classification is a computed heuristic, not an official designation
  - Some MPs joined mid-term (by-elections), affecting participation baselines

## Category Mapping (8 themes from 63 ministries)

| Category | % Share | Ministries |
|---|---|---|
| State & Special Motions | 21.6% | Civil aviation, telecom, tourism, textiles, labour, ports |
| Health, Education & Welfare | 21.5% | Health, education, women & child, social justice, AYUSH, tribal |
| Infrastructure & Energy | 18.2% | Railways, roads, power, coal, petroleum, steel, mines |
| Agriculture & Rural | 13.2% | Agriculture, rural development, fisheries, food distribution |
| Finance & Economy | 10.0% | Finance, commerce, MSMEs, corporate affairs |
| Environment & Water | 7.9% | Environment, Jal Shakti, earth sciences, panchayat |
| Law & Home Affairs | 4.6% | Home affairs, law & justice, parliamentary affairs |
| Defence & Foreign Affairs | 2.9% | Defence, external affairs, atomic energy, space |

## Key Statistical Findings

- **559 MPs** tracked across 5 years
- **1,00,030 questions** across 63 ministries
- **Top 10% MPs (55 people)** → 42.1% of all debate appearances
- **440 MPs (79%)** → Silent Observer archetype
- **Max debates:** 1,261 (Pushpendra Singh Chandel, BJP, UP)
- **Most questions:** Supriya Sule (NCP) — 629 questions

## File Structure

```
outcome/parliamentary-mic-check/
├── index.html          (29KB — main artifact, 5-act scrollytelling)
├── styles.css          (18KB — dark-mode editorial CSS)
├── script.js           (28KB — D3.js beeswarm, waffle, party bars, MP modal)
├── data_embedded.js    (364KB — embedded JSON to bypass file:// CORS)
├── data/
│   ├── mp_master_dataset.json     (458KB)
│   └── debates_macro_summary.json (2KB)
└── assets/             (reserved)
```

## Outcome Path

```
outcome/parliamentary-mic-check/index.html
```

Status: **Draft built** — browser opened, visual verification in progress. Critic final pass pending.
