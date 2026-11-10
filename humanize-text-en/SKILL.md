---
name: humanize-text-en
description: Rewrite or write English text so it reads like a real person wrote it, not an AI. Strips AI tells, filler, and corporate gloss while keeping meaning and facts. Modes - rewrite (default), light (remove tells only), detect (list tells and score). Use when asked to humanize, de-AI, make text sound natural or less robotic, polish a post/email/essay/cover letter, or check whether text sounds AI-generated.
---

# Humanize English text

Make the text read like a specific person wrote it. Keep meaning and facts; change the voice. Output in English (translate first if the source is another language). Short replies to the user go in their language.

## Three principles

1. **Substance before style.** AI tells are symptoms. The disease is emptiness: generic claims, inflated importance, no point of view. Scrubbing tells off empty text leaves empty text. Replace vague claims with what actually happened, or cut them.
2. **Fit the register.** Personality belongs in posts, emails, essays, reviews. Docs, specs, and formal reports need a clean, direct, neutral voice, not jokes and opinions. Never change API names, product names, numbers, or versions.
3. **Trust the reader.** State things directly. No softening, no hand-holding, no explaining your own metaphors.

## Modes

- **rewrite** (default): full pass.
- **light**: remove tells only; keep the author's structure and wording.
- **detect**: list tells with short quotes and severity; don't rewrite.

## Step 1. Calibrate

Identify writer, reader, channel (email, Slack, LinkedIn, blog, report, README, cover letter). Match US/UK spelling to the source (default US). Ask only if a wrong guess would clearly miss.

If the user gives a sample of their own writing, it overrides everything below. Note its sentence length, word level, how paragraphs open, punctuation habits, verbal tics, and transitions. Replace AI patterns with the sample's patterns. Don't lengthen their sentences or upgrade their vocabulary.

## Step 2. Remove the tells

### Content

- Inflated significance: pivotal, a testament to, marks a milestone, plays a crucial role, underscores the importance.
- Vague authorities: experts say, studies show, many believe. Name the source or cut.
- Empty -ing tails: "..., highlighting its commitment to...", "..., paving the way for...".
- "Despite challenges, X continues to thrive" / "The future looks bright."
- Promotional adjectives: seamless, cutting-edge, robust, innovative, vibrant, game-changing.
- False agency: "the data tells us", "the market decided". Say who acted.
- The same point restated to fill space.

### Words

- Cut or replace: delve, tapestry, landscape, realm, leverage, foster, navigate, unlock, empower, showcase, bolster, garner, multifaceted, holistic, utilize (use), facilitate (help).
- Cut: "it's worth noting", "in today's fast-paced world", "when it comes to", "in order to", "due to the fact that".
- "Serves as" / "stands as" where "is" works.
- Moreover / Furthermore / Additionally opening paragraph after paragraph.
- Synonym cycling (the company / the firm / the organization). Repeat the same word.
- Intensifiers (truly, incredibly, deeply) and false absolutes (always, never, every).

### Structure

- "Not X, but Y" / "It's not about X, it's about Y." Just say Y.
- Groups of three everywhere. Two usually beats three.
- False ranges: "from startups to global enterprises."
- Setups and reveals: "Here's the thing:", "The result? Stunning.", "Let that sink in."
- Pull-quote lines. If a sentence sounds like it belongs on a poster, rewrite it.
- Paragraphs that all end on a punchy one-liner.
- Signposting intros ("In this article we'll explore", "Let's dive in") and recap outros ("In conclusion", "Ultimately"). Start with the point; stop when done.

### Format and punctuation

- Em dashes (—): the strongest English tell. Use commas, periods, parentheses, colons. Zero or one per piece; never before a "reveal".
- Bullets and headers where a person would write prose (emails, posts, answers). "Bold label:" bullets, bold on key phrases, emoji decoration.
- Title Case Headings → sentence case. Markdown in email or chat.
- No contractions in informal text (do not, it is) reads robotic. Use don't, it's, we'll.
- Curly quotes in casual channels; use straight ones.

### Chatbot residue

- "Great question!", "Certainly! Here's...", "I hope this helps", "Feel free to reach out", "Let me know if...".
- Sycophancy, hype, "as an AI" or knowledge-cutoff disclaimers.
- Stacked hedges ("may potentially", "could possibly"). Commit, or hedge once.
- Reflexive both-sidesing on every point.

## Step 3. Add a pulse (where the register allows)

- **Rhythm:** vary sentence length hard. Never three similar-length sentences in a row. End paragraphs in different ways.
- **Specifics over abstractions:** a number, a name, an incident ("the server was down for 40 minutes on Tuesday", not "technical challenges arose"). Use only facts from the source or the user. Never invent. No specifics available → shorter and plainer.
- Active voice, positive form, concrete words, no needless words.
- **A point of view:** react to the facts, use "I" when honest, admit mixed feelings or uncertainty, name the specific feeling ("what bothers me is X", not "this is concerning").
- **Some looseness:** an aside in parentheses, a sentence starting with "And" or "So", a fragment. No deliberate typos.
- **Shorter:** if it can lose half its length without losing meaning, cut it.

Don't overcorrect. Wall-to-wall fragments ("It works. Fast. Simple."), forced slang, fake bluntness, and a joke every other line are tells too.

## Step 4. Audit

1. Ask: "What makes this obviously AI-generated?" List the remaining tells, then fix them.
2. Score 1–10: **directness** (statements, not announcements), **rhythm** (varied, not metronomic), **trust** (respects the reader, no hype), **authenticity** (sounds like a person in this channel), **density** (nothing cuttable). Under 40/50 or any score under 7 → revise once more.
3. Confirm: meaning unchanged, no invented facts, spelling consistent.

## Output

- **rewrite / light:** the final text only, no preamble. Then at most one line offering an adjustment ("Want it shorter or more formal?"). Show the audit or scores only if asked.
- **detect:** tells with short quotes and severity (high/medium/low), then the five scores.
