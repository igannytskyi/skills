---
name: it-cv
description: Create, keep up to date, tailor, and check a CV/resume for IT roles (engineers, SRE/DevOps, QA, data, EMs, PMs) so it passes ATS parsing and AI screening and convinces a human recruiter and hiring manager. Keeps a master CV and an achievements log in markdown, adds new achievements over time, tailors a version per job description with a match report, audits an existing CV, and exports an ATS-safe PDF, .docx, and plain text. Use when the user asks to write, update, improve, review, score, or tailor a CV/resume, adapt it to a vacancy, prepare it for applying, check whether it passes ATS/AI filters, or log new achievements for the CV, in any language.
argument-hint: "[create|update|tailor|review|export] <old CV / LinkedIn / brag doc / job description>"
---

# IT CV

Build a CV that gets interviews: parsed correctly by the ATS, ranked well by keyword and AI matching, and convincing to a recruiter in a 10-second skim and to a hiring manager in a 2-minute read. Simple beats fancy. Proof beats adjectives.

Detailed references (read when relevant):
- [references/ats-and-ai-screening.md](references/ats-and-ai-screening.md): how ATS parsing, recruiter search, and AI screening work; formatting rules; what's myth.
- [references/writing-guide.md](references/writing-guide.md): bullet formulas, verbs, before/after examples by role, seniority signals, regional norms.

## Core rules

1. **Never invent.** No made-up numbers, titles, dates, technologies, or employers. If a bullet needs a metric the user hasn't given, write `[metric?]` and ask. Rounded, defensible numbers ("~30%", "40+ services") are fine if the user confirms them. Anything on the CV must survive "tell me more about that" in an interview.
2. **Impact, not duties.** Each bullet: what you did + how (tech, approach) + result (number, scale, or concrete outcome). "Responsible for the payment service" becomes "Rebuilt the payment retry flow in Go and Kafka; failed charges down 38%, ~$1.2M/yr recovered".
3. **Plain format.** One column, standard section headings, no tables, text boxes, icons, photos, skill bars, or graphics; contact info in the body, not in the page header. Real text, not images.
4. **Honest keywords.** Use the job description's exact terms for skills the user really has, inside bullets that prove them. Never add skills the user doesn't have, never keyword-stuff, never hide text (white text, tiny fonts, "instructions to AI"): modern screening flags it and recruiters reject on sight.
5. **Written by a person.** No AI-sounding filler: "results-driven", "passionate", "dynamic", "leveraged", "spearheaded synergies", "proven track record", "in today's fast-paced". Specific nouns and numbers make a CV credible to both humans and AI reviewers.
6. **Relevance decides space.** Recent and relevant roles get 3–6 bullets; older roles 1–2 lines or a single combined "Earlier experience" line. Cut anything that doesn't support the target role.
7. **Privacy.** The CV holds personal data: keep files local, don't send them to external services, and don't add age, photo, marital status, nationality, or ID numbers unless the user's target market expects it (see the regional notes in the writing guide).

## Files (the system that keeps the CV current)

Keep everything in one folder the user chooses (default `./cv/`, ideally a private git repo):

| File | What it is |
|---|---|
| `achievements.md` | Running log of everything worth mentioning, newest first. Grows forever. |
| `master.md` | Full CV with every role and all good bullets. Longer than any version sent out. |
| `tailored/<yyyy-mm>-<company>-<role>.md` | The version sent for a specific job, plus its match report. |
| `build/` | Exported `.docx` and `.txt` (generated, don't edit by hand). |

Achievement log entry format:

```markdown
## 2026-Q3 · Company · Role
- **What:** Migrated 14 services from EC2 to EKS with Terraform and ArgoCD
- **Result:** deploy time 40 min -> 6 min; infra cost -22%
- **Scope:** team of 4, I led design and rollout
- **Tags:** kubernetes, terraform, argocd, aws, cost, leadership
- **Proof:** MR links, dashboard, postmortem (private, for interviews)
```

`master.md` format (the exporter understands exactly this):

```markdown
# Full Name
Senior Backend Engineer · Berlin, Germany · name@email.com · +49 ... · linkedin.com/in/name · github.com/name

## Summary
2–3 lines: who you are for this kind of role, years, core stack, the strongest proof.

## Experience
### Senior Backend Engineer, Company Name
Berlin, Germany (Hybrid) | Mar 2022 – Present
Optional one line about the company or team if not well known (product, scale).
- Bullet
- Bullet

## Skills
**Languages:** Go, Python, SQL
**Cloud & Infra:** AWS (EKS, RDS, SQS), Terraform, Kubernetes

## Education
### BSc Computer Science, University Name
City | 2014 – 2018

## Certifications
- AWS Certified Solutions Architect – Associate (2025)
```

## Modes

### create

1. Collect inputs: old CV (any format; read it fully), LinkedIn export or profile text, achievements/brag doc, performance reviews, target roles and markets. If the user has the `annual-performance-review` skill output or GitLab/GitHub MR lists, use them as evidence.
2. Ask only what blocks a good CV, in one short batch: target role(s) and level, target countries (format and norms differ), work authorization/relocation if relevant, and metrics for the 3–5 biggest achievements.
3. Fill `achievements.md` first, then write `master.md` from it following the writing guide.
4. Run **review** on the result, fix, then **export**.

### update (keep it current)

Trigger: a quarter ended, a project shipped, a review cycle finished, a promotion, a job change.
1. Ask what happened since the last entry, or read new sources (brag doc, perf review, MR/PR lists from the `annual-performance-review` scripts, release notes). Turn each item into an achievement log entry with a result.
2. Promote the strongest new items into `master.md`; merge or demote weaker old bullets so the CV doesn't just get longer. Update title, dates, skills.
3. Show a short diff summary: added, rewritten, removed.
4. Suggest a reminder cadence: a 10-minute log update every quarter, a master CV refresh twice a year.

### tailor (per job)

1. Read the job description. Extract: must-have skills, nice-to-haves, seniority signals, domain, responsibilities, and the exact wording they use (e.g. "Kubernetes" vs "K8s", "CI/CD", "event-driven").
2. Build a **match report**:

   | Requirement | Evidence in master/achievements | Status |
   |---|---|---|
   | 5+ yrs Go | Company A 2021–now, Go services | Strong |
   | Kafka | one project in 2023 | Partial: surface it |
   | GCP | none | Gap: don't claim |

3. Write the tailored version from `master.md`: reorder and pick bullets for this job, mirror their terminology where true, adjust the summary and title line to the role, trim to length. Don't change facts between versions.
4. Report gaps honestly and suggest how to address them in the cover letter or interview, not in the CV.
5. Save to `tailored/` with the match report at the bottom (commented out of the export).

### review (audit any CV)

Score and list concrete fixes, highest impact first:
1. **Parsing (ATS):** run `python3 -I scripts/cv_tool.py check <file>` for .md/.docx/.txt. For PDFs, ask for the text the user gets by copying all from the PDF, or the .docx source. Look for columns, tables, header/footer contact info, graphics, non-standard headings, inconsistent dates.
2. **10-second skim (recruiter):** title, current company, years, core stack, and one strong result visible at the top of page 1?
3. **Evidence (hiring manager):** share of bullets with a measurable result (target: most recent-role bullets), clear personal contribution, scope and seniority signals matching the target level.
4. **Keywords and AI match** (if a job description is given): coverage of must-haves with evidence, exact terms.
5. **Language:** buzzwords, AI-sounding filler, passive "responsible for", pronouns, typos, tense consistency (past for finished roles, present for current).
6. **Length and relevance:** 1 page for under ~8–10 years or early career, 2 pages max for senior/staff/managers; older roles condensed.

Output: overall verdict in 2 lines, a scores table (Parsing, Skim, Evidence, Keywords, Language, Length; 1–10 each), then the fix list with before → after rewrites for the weakest 3–5 bullets.

### export

```bash
python3 -I scripts/cv_tool.py build cv/master.md --out cv/build/                 # .pdf + .docx + .txt
python3 -I scripts/cv_tool.py build cv/tailored/2026-11-acme-sre.md --out cv/build/ --formats pdf --paper letter
python3 -I scripts/cv_tool.py check cv/build/Name_CV.docx                       # re-check the output
```

- No dependencies: the script writes all three formats with the Python standard library.
- The `.pdf` is text-based (Helvetica, real selectable text in reading order, clickable email/LinkedIn/GitHub links), single column, A4 by default (`--paper letter` for US/Canada). It's what most people should send: it looks the same everywhere and modern ATS parse it well. Latin script only; `→`, `≈` and similar symbols are converted to ASCII.
- The `.docx` is single-column, Calibri 10.5pt, standard headings, contact in the body, real bullets, no tables. Send it when a portal asks for Word or parses the PDF badly, or when the user wants to fine-tune the layout by hand.
- Files are named `Firstname_Lastname_CV.*` (override with `--name`). Long CVs flow onto page 2 automatically; the build prints the page count, so if it says 3 pages, cut.
- After building, check the PDF the way an ATS sees it: open it, select all, copy, paste into a plain-text editor. Name, contacts, titles, companies, and dates should all come out in order.
- The `.txt` is for pasting into application forms and for checking how a parser "sees" the CV.
- LinkedIn: on request, produce a headline (≤220 chars), an About section (first person, 3–5 short paragraphs), and Experience entries adapted from the master. Keep LinkedIn and CV consistent in titles and dates.

## Before returning anything

1. Every fact traces to the user's input; `[metric?]` placeholders are listed for the user.
2. Each recent-role bullet has an action, a how, and a result; no "responsible for".
3. Must-have keywords (when tailoring) appear in context, spelled like the job description.
4. Format rules hold: one column, standard headings, consistent dates `Mon YYYY – Mon YYYY`, contact in body.
5. No AI filler or buzzwords; no hidden text; no invented skills.
6. Length fits the level; the top third of page 1 sells the candidate on its own.

Return the CV text (or the diff for update), then a short list: placeholders to fill, decisions the user should make, files written.
