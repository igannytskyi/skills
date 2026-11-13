#!/usr/bin/env python3
"""CV toolkit: build an ATS-safe .docx/.txt from markdown, check a CV, match it to a job.

Python standard library only. Run with `python3 -I`.

  build  CV.md [--out DIR] [--paper a4|letter]   -> DIR/First_Last_CV.docx + .txt
  check  CV.(md|docx|txt)                        -> parsing, structure, and language report
  match  CV.(md|docx|txt) JOB.txt                -> job keywords found / missing in the CV

Markdown format (see SKILL.md):
  # Name
  contact line
  ## Section
  ### Title, Company
  meta line (location | dates)
  - bullet
  **Label:** text
  <!-- comments are dropped (e.g. match reports) -->
"""

import argparse
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- markdown model

def parse_md(text):
    """Return a list of blocks: (kind, text). kinds: name, contact, h2, h3, meta, bullet, para."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    blocks, after_name, after_h3 = [], False, False
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        s = line.strip()
        if s.startswith("# "):
            blocks.append(("name", s[2:].strip())); after_name = True; after_h3 = False; continue
        if s.startswith("## "):
            blocks.append(("h2", s[3:].strip())); after_name = after_h3 = False; continue
        if s.startswith("### "):
            blocks.append(("h3", s[4:].strip())); after_h3 = True; after_name = False; continue
        if re.match(r"^[-*+•]\s+", s):
            blocks.append(("bullet", re.sub(r"^[-*+•]\s+", "", s))); after_name = after_h3 = False; continue
        if after_name:
            blocks.append(("contact", s)); after_name = False; continue
        if after_h3:
            blocks.append(("meta", s)); after_h3 = False; continue
        blocks.append(("para", s))
    return blocks


def inline_runs(s):
    """Split markdown inline text into (text, bold, italic) runs. Links become their text."""
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", s)
    s = s.replace("`", "")
    runs = []
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|_[^_]+_)", s):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            runs.append((part[2:-2], True, False))
        elif (part.startswith("*") and part.endswith("*")) or (part.startswith("_") and part.endswith("_")):
            runs.append((part[1:-1], False, True))
        else:
            runs.append((part, False, False))
    return runs


def plain(s):
    return "".join(t for t, _, _ in inline_runs(s))

# ---------------------------------------------------------------- docx writer

FONT = "Calibri"

def run_xml(text, bold=False, italic=False, size=None):
    props = f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>'
    if bold:
        props += "<w:b/>"
    if italic:
        props += "<w:i/>"
    if size:
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para_xml(runs, style=None, align=None, space_before=0, space_after=40, bullet=False,
             border=False, keep_next=False, size=None, all_bold=False, all_italic=False):
    ppr = ""
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if keep_next:
        ppr += "<w:keepNext/>"
    if bullet:
        ppr += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    if border:
        ppr += '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="808080"/></w:pBdr>'
    ppr += f'<w:spacing w:before="{space_before}" w:after="{space_after}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    body = "".join(run_xml(t, b or all_bold, i or all_italic, size) for t, b, i in runs)
    return f"<w:p><w:pPr>{ppr}</w:pPr>{body}</w:p>"


def build_docx(blocks, path, paper="a4", title="CV", author=""):
    w, h = (11906, 16838) if paper == "a4" else (12240, 15840)
    out = []
    for kind, text in blocks:
        r = inline_runs(text)
        if kind == "name":
            out.append(para_xml(r, align="center", size=32, all_bold=True, space_after=40))
        elif kind == "contact":
            out.append(para_xml(r, align="center", size=20, space_after=120))
        elif kind == "h2":
            out.append(para_xml([(plain(text).upper(), True, False)], style="Heading1", border=True,
                                keep_next=True, space_before=200, space_after=80, size=22))
        elif kind == "h3":
            out.append(para_xml(r, style="Heading2", keep_next=True, space_before=120, space_after=0,
                                size=21, all_bold=True))
        elif kind == "meta":
            out.append(para_xml(r, keep_next=True, space_after=40, size=20, all_italic=True))
        elif kind == "bullet":
            out.append(para_xml(r, bullet=True, space_after=20, size=21))
        else:
            out.append(para_xml(r, space_after=40, size=21))

    sect = (f'<w:sectPr><w:pgSz w:w="{w}" w:h="{h}"/>'
            '<w:pgMar w:top="850" w:right="900" w:bottom="850" w:left="900" w:header="400" w:footer="400" w:gutter="0"/>'
            "<w:cols w:space=\"708\"/></w:sectPr>")
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {ns}><w:body>{"".join(out)}{sect}</w:body></w:document>'

    styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {ns}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="40" w:line="252" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/></w:rPr></w:style>
</w:styles>'''

    numbering = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering {ns}>
<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/>
<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/>
<w:pPr><w:ind w:left="300" w:hanging="220"/></w:pPr><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/></w:rPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>'''

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''

    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''

    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>{escape(title)}</dc:title><dc:creator>{escape(author)}</dc:creator>
<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/numbering.xml", numbering)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("docProps/core.xml", core)


def blocks_to_text(blocks):
    lines = []
    for kind, text in blocks:
        t = plain(text)
        if kind == "h2":
            lines += ["", t.upper()]
        elif kind == "h3":
            lines += ["", t]
        elif kind == "bullet":
            lines.append(f"- {t}")
        else:
            lines.append(t)
    return "\n".join(lines).strip() + "\n"

# ---------------------------------------------------------------- reading any CV

def read_docx(path):
    """Return (lines, issues) where lines are (kind, text) and issues are format findings."""
    issues = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        xml = z.read("word/document.xml").decode("utf8", "replace")
        for n in names:
            if re.match(r"word/(header|footer)\d*\.xml", n):
                t = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", z.read(n).decode("utf8", "replace"))).strip()
                if t:
                    issues.append(("high", f"Text in page {('header' if 'header' in n else 'footer')}: "
                                   f"'{t[:60]}'. Many ATS skip headers/footers; move contact info into the body."))
    if "<w:tbl>" in xml or "<w:tbl " in xml:
        issues.append(("high", "Tables found. Parsers often scramble table cells; use plain paragraphs."))
    if "txbxContent" in xml:
        issues.append(("high", "Text boxes found. Their text is often skipped or misplaced by ATS."))
    if re.search(r'<w:cols [^>]*w:num="([2-9])"', xml):
        issues.append(("high", "Multi-column layout. Use a single column."))
    if "<w:drawing" in xml or "<w:pict" in xml:
        issues.append(("medium", "Images/graphics found (photo, icons, skill bars?). They add nothing for ATS."))
    if "<w:vanish/>" in xml:
        issues.append(("high", "Hidden text found. Remove it: it's treated as keyword stuffing."))
    if re.search(r'<w:color w:val="(FFFFFF|ffffff|FEFEFE)"', xml):
        issues.append(("high", "White text found. Remove it: hidden keywords get flagged."))
    sizes = [int(s) for s in re.findall(r'<w:sz w:val="(\d+)"', xml)]
    if sizes and min(sizes) < 16:
        issues.append(("medium", f"Very small font ({min(sizes)/2:g} pt) somewhere. Keep body text 10–11 pt."))

    lines = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()
        if not text:
            continue
        style = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        style = style.group(1).lower() if style else ""
        if "<w:numPr>" in p or "list" in style or re.match(r"^[•\-–▪●◦*]\s", text):
            lines.append(("bullet", re.sub(r"^[•\-–▪●◦*]\s*", "", text)))
        elif "heading" in style or "title" in style or (text.isupper() and len(text) < 40):
            lines.append(("h2" if ("1" in style or text.isupper()) else "h3", text))
        else:
            lines.append(("para", text))
    return lines, issues


def read_any(path):
    p = Path(path)
    if p.suffix.lower() == ".docx":
        return read_docx(p)
    if p.suffix.lower() == ".pdf":
        sys.exit("PDF: copy all text from the PDF into a .txt file and check that, or check the .docx/.md source.")
    text = p.read_text(encoding="utf8", errors="replace")
    if p.suffix.lower() in (".md", ".markdown"):
        return [(k if k in ("h2", "h3", "bullet") else "para", plain(t)) for k, t in parse_md(text)], []
    lines = []
    for s in (l.strip() for l in text.splitlines()):
        if not s:
            continue
        if re.match(r"^[•\-–▪●◦*]\s", s):
            lines.append(("bullet", re.sub(r"^[•\-–▪●◦*]\s*", "", s)))
        elif s.isupper() and len(s) < 40:
            lines.append(("h2", s))
        else:
            lines.append(("para", s))
    return lines, []

# ---------------------------------------------------------------- check

STANDARD_HEADINGS = {
    "summary", "profile", "professional summary", "experience", "work experience", "professional experience",
    "employment", "employment history", "skills", "technical skills", "core skills", "education",
    "certifications", "certificates", "projects", "open source", "publications", "talks",
    "publications & talks", "languages", "awards", "volunteering", "earlier experience", "patents",
}
WEAK_STARTS = ["responsible for", "worked on", "helped", "assisted", "participated", "involved in",
               "tasked with", "duties included", "in charge of", "was part of", "contributed to"]
BUZZWORDS = ["results-driven", "results driven", "passionate", "dynamic", "self-starter", "team player",
             "hard-working", "hardworking", "detail-oriented", "go-getter", "synergy", "synergies",
             "think outside the box", "proven track record", "rockstar", "ninja", "guru", "leveraged",
             "leverage", "spearheaded", "utilized", "utilize", "fast-paced", "best-in-class",
             "cutting-edge", "seamless", "robust", "innovative", "visionary", "motivated", "excellent communication"]
MONTH = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?"
DATE_PATTERNS = {
    "Mon YYYY": rf"\b{MONTH}\s+(19|20)\d\d\b",
    "MM/YYYY": r"\b(0?[1-9]|1[0-2])/(19|20)\d\d\b",
    "MM.YYYY": r"\b(0?[1-9]|1[0-2])\.(19|20)\d\d\b",
    "YYYY-MM": r"\b(19|20)\d\d-(0[1-9]|1[0-2])\b",
}


def check(path):
    lines, issues = read_any(path)
    text = "\n".join(t for _, t in lines)
    words = len(re.findall(r"\w+", text))
    bullets = [t for k, t in lines if k == "bullet"]
    headings = [t for k, t in lines if k == "h2"]
    top = "\n".join(t for _, t in lines[:6])

    # contact
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", top):
        issues.append(("high", "No email found at the top of the CV (first lines of the body)."))
    if not re.search(r"\+?\d[\d\s().-]{7,}\d", top):
        issues.append(("low", "No phone number at the top. Optional, but most recruiters expect it."))
    if "linkedin.com" not in text.lower():
        issues.append(("low", "No LinkedIn URL. Recruiters check it; add linkedin.com/in/<you>."))

    # headings
    norm = [re.sub(r"[^a-z& ]", "", h.lower()).strip() for h in headings]
    if not any("experience" in h or "employment" in h for h in norm):
        issues.append(("high", "No 'Experience' heading found. Use a standard heading so the ATS maps your jobs."))
    if not any("skill" in h for h in norm):
        issues.append(("medium", "No 'Skills' section. Recruiter keyword search and AI matching use it."))
    if not any("education" in h for h in norm):
        issues.append(("low", "No 'Education' section (fine if intentional, but ATS forms expect it)."))
    odd = [h for h, n in zip(headings, norm) if n and n not in STANDARD_HEADINGS]
    if odd:
        issues.append(("medium", f"Non-standard headings: {', '.join(odd[:5])}. Prefer Summary, Experience, Skills, Education."))

    # dates
    used = {name for name, pat in DATE_PATTERNS.items() if re.search(pat, text, flags=re.I)}
    if len(used) > 1:
        issues.append(("medium", f"Mixed date formats ({', '.join(sorted(used))}). Use one: 'Mar 2022 – Present'."))
    if not used and not re.search(r"\b(19|20)\d\d\b", text):
        issues.append(("high", "No dates found. Every role needs start and end dates."))

    # bullets
    weak, long_b, pron, no_result = [], [], [], 0
    for b in bullets:
        lb = b.lower()
        if any(lb.startswith(w) for w in WEAK_STARTS):
            weak.append(b)
        if len(b) > 230:
            long_b.append(b)
        if re.match(r"^(i|my|we|our)\b", lb):
            pron.append(b)
        if not re.search(r"\d|%|\$|€|£|×|x\d", b):
            no_result += 1
    if bullets:
        share = 100 * (len(bullets) - no_result) // len(bullets)
        sev = "high" if share < 40 else "medium" if share < 60 else None
        if sev:
            issues.append((sev, f"Only {share}% of bullets contain a number/metric. Aim for most bullets in recent roles."))
    else:
        issues.append(("high", "No bullet points found. Use bullets for achievements under each role."))
    if weak:
        issues.append(("medium", f"{len(weak)} bullets start weak ('responsible for', 'worked on', 'helped'...). "
                       f"E.g.: '{weak[0][:80]}'"))
    if long_b:
        issues.append(("low", f"{len(long_b)} bullets longer than ~2 lines. Split or cut. E.g.: '{long_b[0][:60]}...'"))
    if pron:
        issues.append(("low", f"{len(pron)} bullets start with I/my/we. Start with a verb."))

    # language
    found = sorted({w for w in BUZZWORDS if re.search(rf"\b{re.escape(w)}\b", text, flags=re.I)})
    if found:
        issues.append(("medium", f"Buzzwords/AI-sounding filler: {', '.join(found)}. Replace with facts."))
    if "[metric?]" in text:
        issues.append(("high", f"{text.count('[metric?]')} unfilled [metric?] placeholders."))
    dashes = text.count("—")
    if dashes > 6:
        issues.append(("low", f"{dashes} em dashes. Heavy em-dash use reads as AI-written; use commas or semicolons."))

    # length
    pages = words / 500
    if words > 1150:
        issues.append(("medium", f"~{words} words (~{pages:.1f} pages). Keep to 2 pages max; condense older roles."))
    elif words < 250:
        issues.append(("medium", f"Only ~{words} words. Likely too thin to show impact."))

    order = {"high": 0, "medium": 1, "low": 2}
    issues.sort(key=lambda x: order[x[0]])
    print(f"# CV check: {Path(path).name}\n")
    print(f"Words: {words} (~{pages:.1f} pages) · Sections: {len(headings)} · Bullets: {len(bullets)} · "
          f"Bullets with numbers: {len(bullets) - no_result}/{len(bullets)}\n")
    if not issues:
        print("No issues found by automatic checks. Still review content: impact, relevance, seniority.")
        return
    for sev, msg in issues:
        print(f"- [{sev}] {msg}")

# ---------------------------------------------------------------- match

TECH_TERMS = """python java javascript typescript go golang rust c++ c# .net kotlin swift scala ruby php elixir
react angular vue next.js node.js express spring django flask fastapi rails laravel graphql rest grpc
aws gcp azure kubernetes k8s eks gke aks docker terraform ansible helm argocd pulumi cloudformation
ci/cd jenkins circleci linux bash
postgresql postgres mysql mongodb redis cassandra dynamodb elasticsearch opensearch clickhouse snowflake bigquery
redshift kafka rabbitmq sqs pubsub spark flink airflow dbt hadoop
prometheus grafana datadog opentelemetry sentry splunk elk
microservices event-driven serverless lambda
ml pytorch tensorflow llm nlp mlops ios android flutter
sql nosql oauth sso soc2 gdpr pci tdd selenium cypress playwright jest pytest
agile scrum kanban jira on-call sre devops observability mentoring hiring""".split()
MULTI = ["spring boot", "github actions", "gitlab ci", "new relic", "distributed systems", "api design",
         "system design", "machine learning", "deep learning", "react native", "soc 2", "iso 27001",
         "unit testing", "integration testing", "incident management", "people management",
         "stakeholder management"]


def terms_in(text):
    low = " " + re.sub(r"\s+", " ", text.lower()) + " "
    found = set()
    for term in MULTI + TECH_TERMS:
        if re.search(rf"(?<![\w.+#/-]){re.escape(term)}(?![\w+#/-])", low):
            found.add(term)
    # acronyms and product-like tokens from the job text itself (e.g. SAML, HIPAA, Temporal)
    for tok in re.findall(r"\b[A-Z][A-Za-z0-9+#.]*[A-Z0-9][A-Za-z0-9+#.]*\b|\b[A-Z]{2,}\b", text):
        if len(tok) > 1 and tok.lower() not in {"we", "you", "our", "the", "and", "or", "it", "us", "eu", "uk", "usa"}:
            found.add(tok.lower())
    return found


def match(cv_path, job_path):
    lines, _ = read_any(cv_path)
    cv = "\n".join(t for _, t in lines).lower()
    cv = re.sub(r"\S+\.(com|io|dev|org|net|me)/\S*", " ", cv)  # URLs like github.com/x aren't skills
    job = Path(job_path).read_text(encoding="utf8", errors="replace")
    terms = sorted(terms_in(job))
    alias = {"postgres": "postgresql", "k8s": "kubernetes", "golang": "go"}
    present, missing = [], []
    for t in terms:
        variants = {t, alias.get(t, t)} | {k for k, v in alias.items() if v == t}
        hit = any(re.search(rf"(?<![\w.+#/-]){re.escape(v)}(?![\w+#/-])", cv) for v in variants)
        (present if hit else missing).append(t)
    total = len(terms) or 1
    print(f"# Keyword match: {Path(cv_path).name} vs {Path(job_path).name}\n")
    print(f"Job terms found in CV: {len(present)}/{len(terms)} ({100*len(present)//total}%)\n")
    print("Present: " + (", ".join(present) or "-"))
    print("\nMissing: " + (", ".join(missing) or "-"))
    print("\nAdd a missing term only if it's true, inside a bullet that proves it. "
          "Heuristic list; read the job description for must-haves the script can't see.")

# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("md"); b.add_argument("--out", default="build")
    b.add_argument("--paper", choices=["a4", "letter"], default="a4"); b.add_argument("--name")
    c = sub.add_parser("check"); c.add_argument("file")
    m = sub.add_parser("match"); m.add_argument("cv"); m.add_argument("job")
    a = ap.parse_args()

    if a.cmd == "build":
        blocks = parse_md(Path(a.md).read_text(encoding="utf8"))
        person = next((plain(t) for k, t in blocks if k == "name"), "CV")
        stem = a.name or (re.sub(r"[^\w]+", "_", person).strip("_") + "_CV")
        out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
        build_docx(blocks, out / f"{stem}.docx", a.paper, title=f"{person} CV", author=person)
        (out / f"{stem}.txt").write_text(blocks_to_text(blocks), encoding="utf8")
        print(f"Wrote {out / (stem + '.docx')} and {out / (stem + '.txt')}")
    elif a.cmd == "check":
        check(a.file)
    else:
        match(a.cv, a.job)


if __name__ == "__main__":
    main()
