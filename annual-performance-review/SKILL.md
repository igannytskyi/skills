---
name: annual-performance-review
description: Prepare an end-of-year / annual performance review for a person in an IT company - self-assessment, manager review of a direct report, peer (360) feedback, or promotion packet - built from evidence of their achievements over the year (brag doc, PRs, tickets, incidents, OKRs, 1:1 notes, feedback). Frames impact the way top tech companies do (Google GRAD, Meta PSC, Amazon, Microsoft Connects), maps it to the level/career ladder, and checks for bias. Use when the user asks for a performance review, year-end review, self-review, annual review, perf, PSC, promo packet, 360 feedback, brag document, "review of the year", "employee year-end summary", "self-assessment", "promotion review", "feedback for a colleague".
argument-hint: "[self|manager|peer|promo|brag] <person, role/level, period> + evidence"
---

# Annual performance review (IT)

Write a review that a calibration committee would believe: specific achievements, measurable impact, mapped to the person's level, with honest growth areas. A review is an evidence document, not a eulogy and not a character assessment.

For how specific companies structure reviews (axes, rating scales, terminology), see [references/frameworks.md](references/frameworks.md). Read it when the user names their company's process or asks to match a format.

## Modes

- **self**: self-assessment written by the person about themselves (first person).
- **manager** (default if the user is clearly a manager writing about someone): review of a direct report.
- **peer**: 360 feedback about a colleague for their annual review, short and specific.
- **promo**: promotion packet / case for the next level.
- **brag**: no review yet; collect and organize the year's achievements into a brag document the user can keep updating.

If the mode is unclear from context, infer it; ask only if the inference could go either way (for example, "write a review of Anna" from someone who may be her peer or her manager).

## Core rules

1. **Evidence only.** Every claim traces to something in the input: a PR, ticket, incident, doc, metric, quote from feedback, OKR. Never invent numbers, projects, or praise. If impact isn't quantified in the source, describe it concretely without a number and add a `[metric?]` placeholder the user can fill.
2. **Impact over activity.** "Closed 140 tickets" is activity. "Cut checkout p95 latency from 1.2 s to 400 ms, conversion +3%" is impact. For each achievement, push to the outcome for users, the business, the team, or the system.
3. **Scope and level.** The same work means different things at different levels. Always judge against the person's current level expectations (and next level for promo). If the user has a career ladder, use its exact wording.
4. **Behavior, not personality.** "Didn't update the incident channel for 2 hours during the June outage", not "is careless". Growth areas get the same specificity as strengths.
5. **No surprises, no padding.** Don't hide a real problem in soft wording; don't turn a minor nit into a growth area to look balanced. Two real growth areas beat five filler ones.
6. **Whole year, not last month.** Actively fight recency bias: look for Q1–Q2 work explicitly.
7. **Ratings are the user's call.** Suggest a rating only if the user gave their company's scale or asked; explain it against the scale's definition and mark it as a suggestion.
8. **Observer scope.** When reviewing someone else from the user's own data (their mail, chats, meetings, shared repos), it's the user's first-hand view, not the full picture. Write it that way ("in our work on X"), mark areas without evidence as **Not observed** instead of guessing, never count missing evidence as a weakness, and in Gaps suggest who could cover the rest.
9. **Confidentiality.** Treat all input as private HR data. Don't put it in external requests. Don't include compensation numbers unless the user explicitly asks.

## Step 1. Calibrate

A name alone is enough to start: default to the last 12 months, infer the mode, take role/level from available data, state the assumptions in one line and proceed. If the level is unknown, skip the level comparison. Otherwise find out or infer:
- Person, role (backend, SRE, QA, PM, EM, designer, data...), **level** (Junior / Middle / Senior / Staff / Principal / EM, or company-specific like L4/E5/SDE II), time in role.
- Review period (default: last 12 months / calendar year).
- Company format: rating scale, review axes, word limits, required sections. If the user pastes the company form or ladder, follow it exactly; it overrides the default template.
- Goals/OKRs set at the start of the period.
- Writing language: same as the user's request; keep tech terms and product names as is.

## Step 2. Gather evidence

Use whatever the user provides; if tools are available and the user agrees, pull more:
- **GitLab merge requests**: run the bundled script [scripts/gitlab_mrs.py](scripts/gitlab_mrs.py) (Python stdlib only, run with `python3 -I`). Ask the user which sources to cover; they can be combined in one run:
  - a whole **group** with all its subgroups and repos: `--group company/backend` (repeatable);
  - specific **projects**, e.g. private personal repos: `--project jdoe/my-tool` (repeatable);
  - **everything the token can see**, incl. all private personal repos: `--all-visible`.

  ```bash
  python3 -I scripts/gitlab_mrs.py --group company/backend --group company/infra \
    --all-visible --author jdoe --role both --since 2026-01-01 --until 2026-12-31 --format json
  ```
  `--role author|reviewer|both` (MRs written vs. reviewed), `--state merged|all`, `--host gitlab.example.com` for self-hosted (or `GITLAB_HOST`). Without `--author` it uses the token owner (good for **self** mode). Auth: the user sets `GITLAB_TOKEN` (personal access token, `read_api` scope) in their own shell, or has `glab` logged in. Never ask the user to paste the token into chat, never print it, and never send it anywhere except their GitLab host. Without a token only public projects are visible; say so if results look short. Use `--format json` for analysis (titles, descriptions, labels, dates), `md` for a table to show the user.
- **GitHub PRs**: `gh search prs --author <login> --merged --merged-at <from>..<to> --limit 200` (add `--owner <org>` for an organization; private repos are included when `gh` is logged in with access); reviewed PRs: `gh search prs --reviewed-by <login> --merged-at <from>..<to>`.
- After collecting MRs/PRs: group them by project and theme (labels, milestones, title prefixes like `feat`/`fix`), find the 3–6 streams of work that mattered, and open the descriptions of the biggest ones for context and numbers. Review counts show collaboration/mentoring; they are not achievements by themselves.
- **Design docs, RFCs, ADRs** the person wrote.
- **Mail and chat connectors** (Microsoft 365 / Outlook / Teams, Gmail, Slack), if connected: search the user's own interactions with the person, quarter by quarter (emails from/to them, direct chats, shared channels and meetings, shared files). Look for deliverables, decisions, incidents, thanks/kudos, escalations. Skip personal and HR-sensitive messages. This is first-hand evidence from the user's side only (see rule 8). If the user pastes exported chats instead, treat them the same way.
- **Tracker (Jira / Linear)**: epics delivered, tickets resolved, incidents owned.
- **Incidents / on-call**: incidents led or resolved, postmortems written, MTTR changes.
- **Docs, 1:1 notes, brag doc, Slack kudos, peer feedback, customer feedback.**
- **Goals/OKRs**: status of each.

Don't treat raw counts (commits, PRs, tickets) as achievements. Use them only to locate the work that mattered, or as supporting context.

If evidence is thin, say so plainly and list what's missing (for example: "No data for Q1–Q2; nothing on mentoring; no metrics for the migration"). Ask the user for it once, then write with what exists.

## Step 3. Organize by impact

1. Cluster the evidence into **3–6 key achievements** (projects or themes), ranked by impact, not by date. Small stuff goes into one "Other contributions" line.
2. Write each achievement with **XYZ** (Google): *Accomplished [X] as measured by [Y] by doing [Z]*, expanded into:
   - **Context**: the problem and why it mattered (1 line).
   - **Their contribution**: what *they* did, separated from what the team did. Use "led", "designed", "drove", "implemented" accurately; don't upgrade "contributed" to "led".
   - **Impact**: the measurable result (latency, uptime/SLO, cost, incidents, revenue, conversion, delivery time, developer time saved, customers unblocked).
   - **Scope / difficulty**: team, multi-team, org, company-wide; ambiguity, technical risk.
3. Map achievements to **evaluation axes**. Default axes for IT (use the company's if given):
   - **Delivery & impact**: shipped outcomes, against goals.
   - **Technical excellence / craft**: quality, design, reliability, security, tech-debt work, code review.
   - **Ownership & reliability**: on-call, incidents, follow-through, operating what they built.
   - **Collaboration & communication**: cross-team work, docs, stakeholder management.
   - **Leadership & people**: mentoring, onboarding, hiring/interviews, raising the bar, culture (scale expectations by level).
   - **Direction**: influencing what the team builds, not only how (expected more at Senior+).
4. Goals review: each goal → **Exceeded / Met / Partially / Missed / Changed** with evidence. Missed or changed goals get a reason (re-prioritized, blocked, underestimated), not silence.

## Step 4. Strengths and growth

- **Strengths**: 2–4, each backed by 1–2 concrete examples from the achievements.
- **Growth areas**: 1–3, using **SBI** (Situation → Behavior → Impact) + what "good" looks like at their level + one concrete next step. Frame as the gap to the next level where relevant ("to operate at Senior, drive the design, not only implement it").
- In **self** mode, growth areas show self-awareness: what I learned, what I'd do differently, what I'm working on. Not false modesty, not excuses.

## Step 5. Write

Use the company's form if provided. Otherwise use the templates below. Match length to the format: many companies cap answers at 200–500 words per section; if there's a limit, respect it.

### manager

```markdown
# Performance review: <Name> — <Role, Level> — <Period>

## Summary
<3–4 sentences: overall performance against level expectations, the 1–2 biggest impacts, the main growth direction.>

## Key achievements
### 1. <Achievement>
<Context. What they did. Impact with numbers. Scope.>
### 2. ...

## Goals
| Goal | Result | Evidence |
|---|---|---|

## Assessment by area
| Area | Assessment vs. level | Evidence |
|---|---|---|
| Delivery & impact | <Below / Meets / Exceeds> | <1 line> |
| ... | | |

## Strengths
- <Strength>: <example>

## Growth areas
- <Area>: <situation → behavior → impact>. Next level looks like: <...>. Next step: <...>

## Goals for next period
1. <Specific, measurable, tied to growth area or team priority>

## Rating (suggested)
<Only if the scale was provided: rating + 2-line justification against the scale definition.>
```

### self

First person, confident, factual. Sections: Summary; Key achievements (XYZ, "I"); Goals review; What I learned / what I'd do differently; Growth focus for next year; Support I need from my manager. Use "I" for one's own work and "we" for team work, and keep them distinct. No apologizing, no superlatives.

### peer

Under ~200 words unless asked. Sections: what they did that had impact on you/the team (with a specific example); what they should keep doing; one thing they could do even better (specific, kind, actionable). Only what the writer saw firsthand.

### promo

Case for <next level>: Summary of why now → evidence mapped criterion-by-criterion to the next-level ladder (table: criterion | evidence | sustained since) → scope and complexity of top 2–3 projects → feedback quotes from peers/stakeholders (if provided) → risks/gaps and how they're addressed. Show the person has *already been operating* at the next level for a sustained period (usually 2+ quarters), not just potential.

### brag

A living doc: Goals for the year → Projects (one line each with impact and links) → Collaboration & mentoring → Design docs / talks / hiring → Learning → Kudos & feedback quotes → Incidents & on-call. Grouped by quarter, with a `[metric?]` placeholder where impact needs a number.

## Step 6. Check before returning

1. Every achievement has impact, not just activity, and comes from the input.
2. Their contribution is separated from the team's; verbs match reality.
3. The whole period is covered, not just the last quarter.
4. Assessment matches level expectations; promo claims are sustained, not one-off.
5. **Bias check**: no personality labels (abrasive, emotional, aggressive, "not a culture fit"); same standard of evidence for strengths and growth areas; no references to age, gender, family, health, nationality, or leave; no vague praise ("great team player") without an example.
6. Growth areas are specific and actionable; nothing in them would surprise the person if their manager did regular 1:1s. If something would, flag it to the user.
7. Fits the word limits and the requested language.

## Output

- Return the review text only, ready to paste into the HR tool. No preamble.
- After it, a short **Gaps** list if any: missing evidence, `[metric?]` placeholders, claims the user should verify.
- At most one line offering a next step (a shorter version for a form with a word limit, the self-review version, the promo case, or talking points for the review conversation).
