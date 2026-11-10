# skills

Claude skills.

| Skill | What it does |
|---|---|
| [humanize-text-en](humanize-text-en/SKILL.md) | Rewrites English text so it reads like a person wrote it: strips AI tells, keeps meaning and facts. Modes: rewrite, light, detect. |
| [it-meeting-notes](it-meeting-notes/SKILL.md) | Turns an IT meeting transcript or notes into minutes: topics, decisions, action items (owner, due), open questions, risks, plus a Slack follow-up. Covers standups, planning, retros, design reviews, postmortems, releases, client calls. |

## Install

Copy a skill folder into `~/.claude/skills/` (personal) or `.claude/skills/` in a project:

```bash
cp -r humanize-text-en ~/.claude/skills/
```
