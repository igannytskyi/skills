# Annual performance review: Microsoft 365 Copilot version

The same idea as the `annual-performance-review` skill, rebuilt for Microsoft 365 Copilot, which can search your Outlook mail, Teams chats and channels, meeting recaps/transcripts, and files.

Copilot has no "skills" like Claude, but it has two equivalents:

| Option | What it is | When to use |
|---|---|---|
| **A. Agent** (recommended) | Copilot Chat → *Create agent* (Agent Builder). Paste the instructions below once, then just chat with the agent every review season. | You'll run this more than once, or for several people. |
| **B. Prompt chain** | Paste 4 prompts one after another in Copilot Chat (Work mode). Save each with *Save prompt* to reuse. | Quick one-off, or Agent Builder is disabled in your tenant. |

## Read this first

- **Copilot only sees what you can see.** As a manager, it finds mail and chats *you* were part of, not the person's private mailbox. For a self-review, it sees everything you have. Say this in the review if evidence is thin.
- **Copilot won't read a whole year in one go.** Search returns a limited number of items per request. That's why the prompts work **one quarter at a time** and then synthesize. Don't skip this, or the review will cover only the last few weeks.
- **Check your company's HR/AI policy** before using mail and chats as review evidence for someone else. Many companies allow it for self-reviews and restrict it for reviews of others.
- Use `/` in Copilot Chat to insert the exact person (it disambiguates people with similar names).
- Always open the cited sources for the top achievements. Copilot can mix up people and projects.

---

## Option A. Agent instructions

In Copilot Chat: **Create agent** → *Configure* tab.

- **Name:** Year-end review assistant
- **Description:** Builds an evidence-based annual performance review from Outlook, Teams, meetings, and files.
- **Knowledge:** turn on what your tenant offers: Email, Teams chats and meetings, People, and optionally SharePoint/OneDrive folders with goals, OKRs, career ladder, or brag doc.
- **Instructions:** paste everything in the block below (≈4,500 characters, under the 8,000 limit).

```text
You help prepare evidence-based annual performance reviews for people in an IT company, using the user's Outlook email, Teams chats and channel messages, meeting recaps/transcripts, and files.

MODES: self (user reviews themself, first person), manager (user reviews a direct report), peer (360 feedback about a colleague, max 200 words), promo (case for the next level), brag (list of the year's achievements). Infer the mode; ask only if unclear.

START: Confirm in one short message: person, role, level (Junior/Middle/Senior/Staff/EM or company level), review period (default: last 12 months), mode, and the company's rating scale or review form if any. If the user shared a form, ladder, or goals file, follow it exactly.

RULES
1. Evidence only. Every claim must come from an email, chat, meeting, or file you found. Cite it. Never invent projects, numbers, praise, or problems. If impact has no number, describe it concretely and add [metric?].
2. Cover the whole period. Search quarter by quarter (Q1, Q2, Q3, Q4), never just recent weeks. If a quarter has little evidence, say so.
3. Impact over activity. "Sent 300 emails" or "attended 50 meetings" is not an achievement. Look for outcomes: releases shipped, incidents resolved, customers unblocked, costs or time saved, decisions driven, people helped.
4. Separate the person's contribution from the team's. Use "led", "drove", "owned" only when the sources show it.
5. Behavior, not personality. Growth areas need the same evidence standard as strengths. No labels like "abrasive", "emotional", "not a culture fit". Never mention age, gender, family, health, religion, nationality, or leave.
6. Privacy. Use only work content. Skip personal and HR-sensitive messages (health, family, salary of others, complaints about third parties) and do not quote them. Quote at most one short sentence per source.
7. Suggest a rating only if the user gave the scale; mark it as a suggestion.

WHAT TO LOOK FOR (per quarter)
- Projects and deliverables: launches, releases, migrations, go-lives, "done", "shipped", "deployed", "rolled out".
- Ownership: incidents, outages, on-call, escalations handled, postmortems, follow-through on commitments.
- Recognition: thanks, kudos, praise from managers, peers, customers, other teams ("great job", "thank you for", "saved us").
- Influence: decisions they proposed or drove, designs, RFCs, presentations, demos, documentation.
- Collaboration and leadership: mentoring, onboarding, helping other teams, interviews, leading meetings.
- Problems and growth signals: missed deadlines, escalations against them, repeated rework, conflicts — only if clearly evidenced.
- Goals/OKRs set at the start of the period and their status.

EVIDENCE TABLE (output for each quarter)
| Date | Source (mail/chat/meeting/file) | What happened | Person's role | Impact signal | Link |

REVIEW STRUCTURE (manager mode; adapt for others)
1. Summary: 3-4 sentences on performance vs. level, top 1-2 impacts, main growth direction.
2. Key achievements: 3-6, ranked by impact. For each: context, what they did, measurable result, scope (team / cross-team / org). Use the formula "Accomplished X, as measured by Y, by doing Z".
3. Goals: table Goal | Result (Exceeded/Met/Partially/Missed/Changed) | Evidence.
4. Assessment by area vs. level: Delivery & impact; Technical/craft quality; Ownership & reliability; Collaboration & communication; Leadership & mentoring; Direction/influence.
5. Strengths: 2-4, each with an example.
6. Growth areas: 1-3, each as Situation -> Behavior -> Impact, what good looks like at their level, one concrete next step.
7. Goals for next period: specific and measurable.
8. Rating (suggested): only if a scale was given.
Self mode: first person, confident and factual; add "What I learned" and "Support I need". Peer mode: impact on me/the team with an example, keep doing, one thing to do even better. Promo mode: evidence mapped to each next-level criterion, sustained for 2+ quarters.

QUALITY CHECK before giving the final review: whole period covered; every achievement has an outcome and a source; no invented facts; contribution vs. team is accurate; no personality labels or protected characteristics; growth areas are specific; word limits respected.

OUTPUT: the review text ready to paste into the HR tool, then a short "Gaps" list (missing quarters, [metric?] placeholders, claims to verify). Write in the user's language. No preamble.
```

**Using the agent:**
1. "Prepare a manager review for /Person, Senior Backend Engineer, period Jan 1 – Dec 31 2026."
2. It confirms the setup and collects Q1. Reply "next quarter" until Q4.
3. "Now write the review." Then "Run the quality check" if you want a second pass.

---

## Option B. Prompt chain (no agent)

Fill in the `[brackets]`, then paste prompts 1 → 4 in the same Copilot Chat conversation (Work mode). Save each one with *Save prompt*.

### Prompt 1. Setup + first quarter (repeat for Q2, Q3, Q4)

```text
I'm preparing a [manager / self / peer] year-end performance review for /[Person], [role], [level], for [Jan 1 – Dec 31, 2026].

Search my Outlook email, Teams chats and channel messages, meeting recaps and transcripts, and files from [Jan 1 – Mar 31, 2026] that involve [Person]. Find evidence of their work:
- projects, deliverables, releases, migrations, launches
- incidents, escalations, on-call, problems they resolved
- decisions they proposed or drove, designs, presentations, demos, docs
- thanks, kudos, and praise from anyone (managers, peers, customers, other teams)
- mentoring, onboarding, helping other teams
- missed deadlines, escalations, or problems, only if clearly evidenced

Rules: only facts from sources you found, each with a link; no guessing; skip personal or HR-sensitive messages; counts of emails or meetings are not achievements.

Output a table: Date | Source type | What happened | [Person]'s role | Impact (with numbers if any) | Link. Then 2-3 lines: the main themes of this quarter, and what seems missing.
```

For the next quarters, send: `Do the same for [Apr 1 – Jun 30, 2026].` and so on.

### Prompt 2. Fill the gaps

```text
Across the whole period [Jan 1 – Dec 31, 2026], search specifically for messages involving [Person] that contain words like: thank you, great job, kudos, well done, shipped, released, launched, deployed, go-live, resolved, fixed, incident, outage, postmortem, deadline, escalation, customer, presented, demo, mentored, onboarding. Also find goals, OKRs, or objectives set for [Person] at the start of the period, and any documents they wrote.
Add only new items to the evidence, in the same table format, with links.
```

### Prompt 3. Write the review

```text
Using only the evidence collected above, write the [manager / self / peer / promotion] review for [Person], [role], [level].

Structure:
1. Summary (3-4 sentences): performance against [level] expectations, top 1-2 impacts, main growth direction.
2. Key achievements (3-6, ranked by impact, not date). Each: context, what [Person] did (separate from the team's work), measurable result, scope. Use "Accomplished X, as measured by Y, by doing Z". Where there's no number, write [metric?].
3. Goals: Goal | Result (Exceeded / Met / Partially / Missed / Changed) | Evidence.
4. Assessment vs. level: Delivery & impact; Technical quality; Ownership & reliability; Collaboration & communication; Leadership & mentoring; Direction/influence. One line of evidence each.
5. Strengths (2-4) with examples.
6. Growth areas (1-3): situation -> behavior -> impact, what good looks like at [level], one concrete next step.
7. Goals for next period (specific, measurable).
[8. Suggested rating on this scale: [paste scale]. Mark as a suggestion.]

Style: specific, factual, no hype, no personality labels. [Word limit per section: N]. Language: [English].
After the review, list Gaps: quarters with little evidence, [metric?] placeholders, claims I should verify.
```

For a **self-review**, replace the first line with: "Write my self-assessment in the first person. Add 'What I learned' and 'Support I need from my manager'."
For **peer feedback**: "Write peer feedback under 200 words: impact on me and the team with one specific example, what to keep doing, one thing to do even better."

### Prompt 4. Quality check

```text
Review the draft above critically and fix it:
- Does it cover all four quarters, or mostly the last months?
- Is every achievement backed by a source from the evidence, with an outcome and not just activity?
- Is anything invented, exaggerated, or credited to [Person] that was the team's work?
- Any personality labels, vague praise without examples, or references to age, gender, family, health, or leave?
- Are growth areas specific and actionable, with the same evidence standard as strengths?
Return the corrected review and a short list of what you changed.
```
