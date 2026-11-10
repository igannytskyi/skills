# skills

Claude skills.

| Skill | What it does |
|---|---|
| [humanize-text-en](humanize-text-en/SKILL.md) | Rewrites English text so it reads like a person wrote it: strips AI tells, keeps meaning and facts. Modes: rewrite, light, detect. |
| [it-meeting-notes](it-meeting-notes/SKILL.md) | Turns an IT meeting transcript or notes into minutes: topics, decisions, action items (owner, due), open questions, risks, plus a Slack follow-up. Covers standups, planning, retros, design reviews, postmortems, releases, client calls. |
| [annual-performance-review](annual-performance-review/SKILL.md) | Prepares a year-end performance review for an IT employee from evidence of their achievements: self, manager, peer (360), promo packet, or brag doc. Impact framing (XYZ), level mapping, bias check; reference on Google, Meta, Amazon, Microsoft, Netflix, GitLab formats. |

## Microsoft 365 Copilot

Prompts and agent instructions for Copilot (no skills there):

| Prompt | What it does |
|---|---|
| [annual-performance-review](m365-copilot/annual-performance-review.md) | Year-end review from Outlook mail, Teams chats, meetings, and files: agent instructions for Agent Builder, or a 4-step prompt chain that goes quarter by quarter. |

## Install

Copy a skill folder into `~/.claude/skills/` (personal) or `.claude/skills/` in a project:

```bash
cp -r humanize-text-en ~/.claude/skills/
```
