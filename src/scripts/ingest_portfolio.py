#!/usr/bin/env python3
"""
Ingest all portfolio files from candidate.portfolio_dir (e.g. mind-palace) into out/okf/sources/
"""
import html
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Set
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.scripts.canonical_loader import load_canonical_career_record


def format_okf_frontmatter(data: Dict[str, Any]) -> str:
    """Safely serializes a mapping into YAML frontmatter using yaml.safe_dump."""
    dumped = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{dumped}\n---\n"


def clean_html_text(raw_html: str) -> str:
    cleaned = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
    cleaned = html.unescape(cleaned)
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
    p = rel_path.replace('\\', '/').lower()
    p = re.sub(r'\.(md|html|pdf|txt)$', '', p)
    p = re.sub(r'[^a-z0-9]+', '-', p)
    return p.strip('-')


def _resolve_target_path(target_rel: str, repo_root: Path) -> Path:
    target_path = Path(target_rel)
    if target_path.is_absolute():
        return target_path
    return repo_root / target_rel


def ingest_portfolio(config_path: Path, repo_root: Path) -> int:
    """Ingests portfolio sources and canonical employment records into out/okf/."""
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    portfolio_dir = Path(config["candidate"]["portfolio_dir"])
    if not portfolio_dir.exists() or not portfolio_dir.is_dir():
        raise FileNotFoundError(f"Configured portfolio_dir does not exist or is not a directory: {portfolio_dir}")

    target_rel = config["target_opportunity"]["source"]
    target_opp_path = _resolve_target_path(target_rel, repo_root)
    if not target_opp_path.exists():
        raise FileNotFoundError(f"Configured target_opportunity.source does not exist: {target_opp_path}")

    print(f"Ingesting portfolio from: {portfolio_dir}")

    out_sources_dir = repo_root / "out" / "okf" / "sources"
    out_sources_dir.mkdir(parents=True, exist_ok=True)

    discovered_sources = []
    written_filenames: Set[str] = set()

    for root, dirs, files in os.walk(portfolio_dir):
        # Skip hidden dirs like .git and strictly exclude quarantine directory
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and d.lower() != 'quarantine')
        rel_root = Path(root).relative_to(portfolio_dir).as_posix().lower()
        if "quarantine" in rel_root.split("/"):
            continue
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

            try:
                if ext == '.md':
                    content = full_path.read_text(encoding='utf-8', errors='ignore')
                    title = extract_md_title(content, file)
                    snippet = re.sub(r'\s+', ' ', content[:300]).strip()
                elif ext == '.html':
                    content = full_path.read_text(encoding='utf-8', errors='ignore')
                    title = extract_html_title(content, file)
                    snippet = clean_html_text(content)[:300]
                elif ext == '.txt':
                    content = full_path.read_text(encoding='utf-8', errors='ignore')
                    title = file.replace('.txt', '').replace('-', ' ').replace('_', ' ').title()
                    snippet = re.sub(r'\s+', ' ', content[:300]).strip()
                elif ext == '.pdf':
                    title = file.replace('.pdf', '')
                    snippet = "PDF Document"
            except Exception as e:
                print(f"Warning: Failed to read {full_path}: {e}")
                log_file = repo_root / "out" / "okf" / "log.md"
                if log_file.exists():
                    with open(log_file, "a", encoding="utf-8") as lf:
                        lf.write(f"\n- **WARNING (portfolio-ingestor)**: Skipped unreadable file `{rel_path}`: {e}\n")
                continue

            source_info = {
                "id": slug,
                "title": title,
                "rel_path": rel_path,
                "abs_path": str(full_path),
                "category": category,
                "snippet": snippet,
            }
            discovered_sources.append(source_info)

            frontmatter = format_okf_frontmatter({
                "type": "Source",
                "id": slug,
                "title": title,
                "resource": rel_path,
                "category": category,
                "author": "human:alexandre.franco",
                "sources": [
                    {
                        "id": slug,
                        "resource": rel_path,
                        "title": title,
                    }
                ],
            })
            summary_line = (
                f"[evidence] {snippet} [^{slug}]"
                if snippet
                else f"[evidence] No text preview extracted for `{rel_path}`. [^{slug}]"
            )
            source_content = (
                f"{frontmatter}\n"
                f"# {title}\n\n"
                f"[evidence] Discovered portfolio source file: `{rel_path}` in `{portfolio_dir}`. [^{slug}]\n"
                f"[inference] Classified as `{category}` document.\n\n"
                f"## Summary / Abstract\n"
                f"{summary_line}\n"
            )
            source_filename = f"{slug}.md"
            (out_sources_dir / source_filename).write_text(source_content, encoding='utf-8')
            written_filenames.add(source_filename)

    # Register target opportunity
    target_slug = "target-" + make_slug(target_rel)
    target_filename = f"{target_slug}.md"
    target_fm = format_okf_frontmatter({
        "type": "Source",
        "id": target_slug,
        "title": "Target Position Specification",
        "resource": target_rel,
        "category": "TargetOpportunitySource",
        "author": "recruiter",
        "sources": [
            {
                "id": target_slug,
                "resource": target_rel,
                "title": "Target Position Specification",
            }
        ],
    })
    target_source_content = (
        f"{target_fm}\n"
        f"# Target Position Specification\n\n"
        f"[evidence] Target position specification file: `{target_rel}`. [^{target_slug}]\n"
        f"[inference] Classified as TargetOpportunitySource.\n"
    )
    (out_sources_dir / target_filename).write_text(target_source_content, encoding='utf-8')
    written_filenames.add(target_filename)

    # Write SourceIndex with safe YAML frontmatter and dynamic UTC timestamp
    index_sources = [
        {"id": src["id"], "resource": src["rel_path"], "title": src["title"]}
        for src in discovered_sources
    ]
    index_sources.append({
        "id": target_slug,
        "resource": target_rel,
        "title": "Target Position Specification",
    })
    index_fm = format_okf_frontmatter({
        "okf_version": "0.2",
        "type": "SourceIndex",
        "title": "Discovered Portfolio & Opportunity Sources Index",
        "description": f"Master index of all discovered candidate portfolio files from {portfolio_dir}.",
        "generated": {
            "by": "portfolio-ingestor",
            "at": datetime.now(timezone.utc).isoformat(),
        },
        "status": "verified",
        "sources": index_sources,
    })

    index_lines = [index_fm, "\n# Ingested Portfolio & Opportunity Sources\n\n"]
    for src in discovered_sources:
        index_lines.append(f"- [{src['title']} ({src['category']})]({src['id']}.md)\n")
    index_lines.append(f"- [Target Position Specification]({target_filename})\n\n")
    first_source_id = discovered_sources[0]["id"] if discovered_sources else target_slug
    index_lines.append("# Source Coverage Map\n\n")
    index_lines.append(
        f"[evidence] Discovered {len(discovered_sources)} portfolio documents across subdirectories in `{portfolio_dir}` and 1 target opportunity specification. [^{first_source_id}]\n"
    )
    index_lines.append(
        "[inference] Comprehensive automated ingestion covering all articles, weekly learning logs, architecture philosophies, experiments, SOPs, and narrative case studies.\n"
    )
    (out_sources_dir / "index.md").write_text("".join(index_lines), encoding='utf-8')
    written_filenames.add("index.md")

    # Prune stale source markdown files from previous runs (e.g. files moved to quarantine/)
    for existing_file in out_sources_dir.glob("*.md"):
        if existing_file.name not in written_filenames:
            existing_file.unlink()

    # Generate okf/employment-records.yaml strictly from canonical/career-record.yaml
    canonical_record = load_canonical_career_record(config_path=str(config_path))
    emp_records = []
    for entry in canonical_record.career:
        emp_records.append({
            "id": f"emp-{entry.id.lower()}",
            "employer": entry.employer,
            "client": entry.client,
            "engagement_type": entry.engagement_type,
            "title": entry.formal_title,
            "start_date": entry.start_date,
            "end_date": entry.end_date,
            "status": entry.status,
            "location": entry.location,
            "operational_scope": entry.operational_scope,
            "acting_responsibilities": entry.acting_responsibilities,
            "responsibilities_scope": entry.responsibilities_scope,
            "sources": ["canonical-career-record"],
            "approved_aliases": entry.approved_aliases,
        })

    emp_yaml_path = repo_root / "out" / "okf" / "employment-records.yaml"
    emp_yaml_path.parent.mkdir(parents=True, exist_ok=True)
    with open(emp_yaml_path, "w", encoding="utf-8") as yf:
        yaml.safe_dump({"employment_records": emp_records}, yf, sort_keys=False, default_flow_style=False)
    print(f"Updated {emp_yaml_path} with {len(emp_records)} verified employment records from canonical career record.")
    print(f"Successfully ingested {len(discovered_sources)} source documents into {out_sources_dir}")
    return len(discovered_sources)


def main():
    config_path = REPO_ROOT / "config" / "config.yaml"
    try:
        ingest_portfolio(config_path=config_path, repo_root=REPO_ROOT)
    except Exception as e:
        print(f"FATAL: Portfolio ingestion failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
