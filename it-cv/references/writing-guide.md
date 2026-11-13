# Writing an IT CV that gets interviews

Sources of these practices: Google's XYZ formula (Laszlo Bock), Gayle Laakmann McDowell (ex-Google, *Cracking the Coding Interview*), Gergely Orosz (*The Tech Resume Inside Out*), Tech Interview Handbook (Yangshun Tay), and what FAANG and scale-up recruiters consistently ask for. They agree on almost everything below.

## Structure (in this order)

1. **Name + one contact line:** target title · city, country (and "open to relocation"/"EU work permit" if relevant) · email · phone · LinkedIn · GitHub.
2. **Summary** (optional, 2–3 lines): useful for career changers, seniors, and tailored applications. No adjectives about yourself; facts only. Example: "Backend engineer, 8 years, Go and Python, payments and high-load APIs. Led the rebuild of a checkout platform serving 3M users/day. Looking for staff-level backend roles."
3. **Experience** (reverse chronological): the main part, 70–80% of the page.
4. **Skills:** 3–5 grouped lines.
5. **Education**, then **Certifications**, **Projects/Open source**, **Publications/Talks**, **Languages** as relevant.

New grads: Education and Projects can go above Experience.

## The bullet formula

**Action verb + what + how (tech) + result (number or concrete outcome).**

Google's XYZ: *Accomplished [X] as measured by [Y] by doing [Z].*

Measures that work in IT: latency (p95/p99), throughput, uptime/SLO, incidents and MTTR, error rate, cost ($ or %), deploy frequency and lead time, build/CI time, test coverage only if meaningful, users/customers/requests affected, revenue or conversion, time saved for people (hours/week), team size led, number of services/teams adopting your work, hiring numbers.

No number available? Use scale or a concrete outcome: "adopted by all 6 product teams", "unblocked the EU launch", "became the default deployment path".

### Before → after

- "Responsible for maintaining CI/CD pipelines."
  → "Rebuilt CI on GitHub Actions with build caching and parallel test shards; pipeline time 42 → 11 min for 30 engineers."
- "Worked on microservices using Java and Spring."
  → "Split the order monolith into 5 Spring Boot services behind Kafka; release cadence weekly → daily, zero-downtime deploys."
- "Helped improve application performance."
  → "Cut API p95 latency from 900 ms to 250 ms by adding Redis caching and fixing N+1 queries in the catalog service."
- "Participated in on-call rotation."
  → "Led 12 production incidents as incident commander; introduced runbooks and alert tuning, pages down 60% in two quarters."
- "Mentored junior developers."
  → "Mentored 3 engineers; two promoted to mid-level within a year. Ran the team's onboarding, ramp-up time 6 → 3 weeks."
- "Managed a team of developers." (EM)
  → "Managed 8 engineers across 2 squads; hired 5, retained everyone through a reorg, delivered the billing migration 3 weeks early."

### Verbs

Use: built, designed, led, shipped, migrated, automated, reduced, cut, increased, scaled, replaced, introduced, owned, launched, debugged, optimized, mentored, hired, negotiated, drove.
Avoid: responsible for, worked on, helped, participated, assisted, involved in, utilized, leveraged, spearheaded, orchestrated (unless literal), synergized.

Use "led" only when you led. Use "co-designed" or "as part of a team of 4" when honest; interviewers ask.

## Role-specific signals

- **Backend:** scale (RPS, data volume), reliability, data modeling, APIs, performance, migrations.
- **Frontend:** Core Web Vitals, bundle size, conversion, accessibility, design systems adopted by N teams.
- **Mobile:** crash-free rate, app size, startup time, store rating, release cadence.
- **SRE / DevOps / Platform:** SLOs, MTTR, deploy frequency, cost savings, IaC coverage, developer adoption.
- **Data / ML:** pipeline freshness and reliability, model metrics tied to business impact, cost per query, users of the platform.
- **QA / SDET:** escaped defects, automation coverage of critical paths, test time, flakiness reduction.
- **Security:** vulnerabilities closed, audit/compliance passed (SOC 2, ISO 27001), mean time to patch.
- **Engineering manager:** team size, hiring, retention, delivery, process changes and their effect, cross-team outcomes. Keep 1–2 technical bullets to show judgment.
- **Product manager:** outcomes (revenue, retention, activation), launches, discovery that changed direction, stakeholders aligned.

## Seniority signals

| Level | Bullets should show |
|---|---|
| Junior | Shipped features, learned fast, quality of own work, good projects |
| Mid | Owns features end to end, measurable results, reliability |
| Senior | Leads projects, designs systems, owns production, mentors, influences team |
| Staff+ | Cross-team technical direction, org-wide impact, ambiguous problems, multipliers |
| EM | People, hiring, delivery, team health, cross-team outcomes |

A senior CV full of task-level bullets reads as mid-level. Lead with scope.

## What to cut

- Objective statements ("Seeking a challenging position...").
- Soft-skill adjectives: team player, hard-working, detail-oriented, passionate, results-driven, self-starter.
- Skill bars, ratings ("Python ★★★★☆"), "MS Office", "Git" for experienced engineers, outdated tech unless the job asks for it.
- References and "References available on request".
- High school, GPA after a few years of experience, hobbies (unless genuinely relevant or a strong conversation starter, one line).
- Every technology from a 15-year-old job. Older roles: title, company, dates, one line.
- First-person pronouns in bullets.

## Gaps, short stints, career changes

- Gaps: one honest line is enough ("2024: career break, relocation"; "2023: parental leave"). Don't hide dates.
- Short jobs (<1 year): keep if relevant; one or two bullets. Contract work: group under one "Independent contractor" entry with clients.
- Layoffs: no need to mention on the CV.
- Career change: summary states the target role; projects and transferable results go first.

## Regional notes

- **US / Canada / UK / Ireland / Australia:** no photo, age, marital status, nationality. "Resume" in the US is 1–2 pages.
- **Germany / Austria / Switzerland:** photo and date of birth are still common in traditional companies but optional and increasingly dropped in tech; the traditional tabular German CV style isn't required for international tech companies. Mention work permit / EU Blue Card if relevant. German-language roles expect a German CV.
- **Netherlands / Nordics:** English CV fine for tech; no photo needed; direct and concise tone.
- **France / Spain / Italy / Eastern Europe:** photo common locally, not needed for international companies.
- **Remote / international:** state time zone and work authorization clearly ("Based in Warsaw, UTC+1, EU citizen").
- **Language level:** CEFR (B2, C1) or "native/fluent/professional working proficiency".

## Tailoring checklist

1. Title line matches the job's title (if true: "Senior Backend Engineer", not "Software Developer III").
2. Summary mentions their domain and top 2–3 must-haves you actually have.
3. The first 2 bullets of the current role prove the job's most important requirement.
4. Their exact terms are used where true.
5. Irrelevant bullets moved down or removed. Facts unchanged.
