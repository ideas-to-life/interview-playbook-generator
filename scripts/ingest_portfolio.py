#!/usr/bin/env python3
"""
Ingest all portfolio files from candidate.portfolio_dir (e.g. mind-palace) into out/okf/sources/
"""
import os
import re
import html
import yaml
from pathlib import Path

def clean_html_text(raw_html: str) -> str:
    # Remove script and style elements
    cleaned = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
    # Unescape HTML entities
    cleaned = html.unescape(cleaned)
    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def extract_html_title(raw_html: str, filename: str) -> str:
    match = re.search(r'<title[^>]*>(.*?)</title>', raw_html, flags=re.IGNORECASE | re.DOTALL)
    if match:
        t = html.unescape(match.group(1)).strip()
        if t:
            return t
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', raw_html, flags=re.IGNORECASE | re.DOTALL)
    if h1_match:
        t = clean_html_text(h1_match.group(1))
        if t:
            return t
    return filename.replace('-', ' ').replace('_', ' ').title()

def extract_md_title(content: str, filename: str) -> str:
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return filename.replace('.md', '').replace('-', ' ').replace('_', ' ').title()

def determine_category(rel_path: str) -> str:
    parts = Path(rel_path).parts
    if len(parts) > 1:
        folder = parts[0].lower()
        if folder == 'articles':
            return 'ArticleSource'
        elif folder == 'learnings':
            return 'LearningLogSource'
        elif folder == 'architecture-philosophy':
            return 'PhilosophySource'
        elif folder in ('experiments', 'standard-operational-procedure'):
            return 'PracticeSource'
        elif folder in ('resume-profile', 'portfolio', 'about', 'narratives'):
            return 'PortfolioNarrativeSource'
    return 'PortfolioSource'

def make_slug(rel_path: str) -> str:
    # sanitize path into unique slug
    p = rel_path.replace('\\', '/').lower()
    p = re.sub(r'\.(md|html|pdf|txt)$', '', p)
    p = re.sub(r'[^a-z0-9]+', '-', p)
    return p.strip('-')

def main():
    repo_root = Path(__file__).resolve().parent.parent
    config_path = repo_root / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    portfolio_dir = Path(config["candidate"]["portfolio_dir"])
    target_rel = config["target_opportunity"]["source"]

    print(f"Ingesting portfolio from: {portfolio_dir}")

    out_sources_dir = repo_root / "out" / "okf" / "sources"
    out_sources_dir.mkdir(parents=True, exist_ok=True)

    discovered_sources = []

    for root, dirs, files in os.walk(portfolio_dir):
        # Skip hidden dirs like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in sorted(files):
            if file.startswith('.') or file == 'CLAUDE.md':
                continue
            ext = os.path.splitext(file)[1].lower()
            if ext not in ('.md', '.html', '.pdf', '.txt'):
                continue

            full_path = Path(root) / file
            rel_path = full_path.relative_to(portfolio_dir).as_posix()
            slug = make_slug(rel_path)
            category = determine_category(rel_path)

            title = file
            snippet = ""

            if ext == '.md':
                try:
                    content = full_path.read_text(encoding='utf-8', errors='ignore')
                    title = extract_md_title(content, file)
                    snippet = content[:300].replace('\n', ' ')
                except Exception as e:
                    print(f"Warning: Failed to read {full_path}: {e}")
                    log_file = repo_root / "out" / "okf" / "log.md"
                    if log_file.exists():
                        with open(log_file, "a", encoding="utf-8") as lf:
                            lf.write(f"\n- **WARNING (portfolio-ingestor)**: Skipped unreadable file `{rel_path}`: {e}\n")
                    continue
            elif ext == '.html':
                try:
                    content = full_path.read_text(encoding='utf-8', errors='ignore')
                    title = extract_html_title(content, file)
                    snippet = clean_html_text(content)[:300]
                except Exception as e:
                    print(f"Warning: Failed to read {full_path}: {e}")
                    log_file = repo_root / "out" / "okf" / "log.md"
                    if log_file.exists():
                        with open(log_file, "a", encoding="utf-8") as lf:
                            lf.write(f"\n- **WARNING (portfolio-ingestor)**: Skipped unreadable file `{rel_path}`: {e}\n")
                    continue
            elif ext == '.pdf':
                title = file.replace('.pdf', '')
                snippet = "PDF Document"

            source_info = {
                "id": slug,
                "title": title,
                "rel_path": rel_path,
                "abs_path": str(full_path),
                "category": category,
                "snippet": snippet
            }
            discovered_sources.append(source_info)

            # Write OKF Source concept file
            source_file = out_sources_dir / f"{slug}.md"
            source_content = f"""---
type: Source
id: "{slug}"
title: "{title}"
resource: "{rel_path}"
category: "{category}"
author: "human:alexandre.franco"
sources:
  - id: "{slug}"
    resource: "{rel_path}"
    title: "{title}"
---

# {title}

[evidence] Discovered portfolio source file: `{rel_path}` in `{portfolio_dir}`. [^{slug}]
[inference] Classified as `{category}` document.

## Summary / Abstract
{snippet}
"""
            source_file.write_text(source_content, encoding='utf-8')

    # Also register target opportunity
    target_slug = "target-" + make_slug(target_rel)
    target_source_file = out_sources_dir / f"{target_slug}.md"
    target_source_content = f"""---
type: Source
id: "{target_slug}"
title: "Target Position Specification"
resource: "{target_rel}"
category: "TargetOpportunitySource"
author: "recruiter"
sources:
  - id: "{target_slug}"
    resource: "{target_rel}"
    title: "Target Position Specification"
---

# Target Position Specification

[evidence] Target position specification file: `{target_rel}`. [^{target_slug}]
[inference] Classified as TargetOpportunitySource.
"""
    target_source_file.write_text(target_source_content, encoding='utf-8')

    # Write SourceIndex
    source_index_file = out_sources_dir / "index.md"
    index_md = f"""---
okf_version: "0.2"
type: SourceIndex
title: "Discovered Portfolio & Opportunity Sources Index"
description: "Master index of all discovered candidate portfolio files from {portfolio_dir}."
generated:
  by: "portfolio-ingestor"
  at: "2026-08-14T14:12:00+01:00"
status: verified
sources:
"""
    for src in discovered_sources:
        index_md += f"""  - id: "{src['id']}"
    resource: "{src['rel_path']}"
    title: "{src['title']}"
"""
    index_md += f"""  - id: "{target_slug}"
    resource: "{target_rel}"
    title: "Target Position Specification"

---

# Ingested Portfolio & Opportunity Sources

"""
    for src in discovered_sources:
        index_md += f"- [{src['title']} ({src['category']})]({src['id']}.md)\n"
    index_md += f"- [Target Position Specification]({target_slug}.md)\n"

    index_md += f"""
# Source Coverage Map

[evidence] Discovered {len(discovered_sources)} portfolio documents across subdirectories in `{portfolio_dir}` and 1 target opportunity specification. [^{discovered_sources[0]['id'] if discovered_sources else target_slug}]
[inference] Comprehensive automated ingestion covering all articles, weekly learning logs, architecture philosophies, experiments, SOPs, and narrative case studies.
"""
    source_index_file.write_text(index_md, encoding='utf-8')

    # Parse Positions.csv if present to update okf/employment-records.yaml
    positions_csv = portfolio_dir / "resume-profile" / "Positions.csv"
    if positions_csv.exists():
        import csv
        emp_records = []
        with open(positions_csv, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                company = row.get("Company Name", "").strip()
                title = row.get("Title", "").strip()
                location = row.get("Location", "").strip()
                start_date = row.get("Started On", "").strip()
                finished_on = row.get("Finished On", "").strip()
                if not company or not title:
                    continue
                end_date = finished_on if finished_on else None
                status = "former" if finished_on else "current"
                emp_id = f"emp-{re.sub(r'[^a-z0-9]+', '-', company.lower()).strip('-')}-{i}"
                aliases = [title]
                if "Lead Enterprise Architect" in title:
                    aliases.extend(["Lead Enterprise Architect", "Lead Enterprise Architect – Technology Transformation Group & Commercial"])
                if "Agentic AI" in title:
                    aliases.extend(["Senior Director, Agentic AI Systems Architecture", "Senior Director, System Architect – Agentic AI"])
                if "Enterprise Architect" in title:
                    aliases.append("Enterprise Architect")
                if "Global Solution Architect" in title:
                    aliases.append("Global Solution Architect")
                if "BAT" in company or "British American Tobacco" in company:
                    aliases.extend(["Enterprise Architect & Global Solution Architect", "Enterprise Architect Scientific Research and Development (SR&D)", "Global Solution Architect - Integration & Automation", "Regional Solution Architect", "Enterprise Architect"])
                if "Mostelli" in company:
                    aliases.extend(["Enterprise Architect | AI Transformation Advisor", "Enterprise Architect & AI Transformation Advisor"])


                emp_records.append({
                    "id": emp_id,
                    "employer": company,
                    "title": title,
                    "start_date": start_date,
                    "end_date": end_date,
                    "status": status,
                    "location": location or "London, UK",
                    "sources": ["positions-csv"],
                    "approved_aliases": list(dict.fromkeys(aliases))
                })

        if emp_records:
            emp_yaml_path = repo_root / "out" / "okf" / "employment-records.yaml"
            with open(emp_yaml_path, "w", encoding="utf-8") as yf:
                yaml.dump({"employment_records": emp_records}, yf, sort_keys=False, default_flow_style=False)
            print(f"Updated {emp_yaml_path} with {len(emp_records)} employment records from Positions.csv")

    print(f"Successfully ingested {len(discovered_sources)} source documents into {out_sources_dir}")

if __name__ == "__main__":
    main()

