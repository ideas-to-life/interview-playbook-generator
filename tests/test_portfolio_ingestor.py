import os
import shutil
import tempfile
import yaml
import pytest
from pathlib import Path
from src.scripts.ingest_portfolio import make_slug, determine_category, clean_html_text, extract_html_title, extract_md_title

def test_make_slug():
    assert make_slug("articles/my-article.html") == "articles-my-article"
    assert make_slug("learnings\\20260109.md") == "learnings-20260109"
    assert make_slug("Special_Chars & Name.md") == "special-chars-name"

def test_determine_category():
    assert determine_category("articles/post.html") == "ArticleSource"
    assert determine_category("learnings/20260109.md") == "LearningLogSource"
    assert determine_category("architecture-philosophy/doc.md") == "PhilosophySource"
    assert determine_category("experiments/test.md") == "PracticeSource"
    assert determine_category("resume-profile/cv.md") == "PortfolioNarrativeSource"

def test_clean_html_text():
    raw = "<html><head><title>Test</title><style>body {color:red}</style></head><body><h1>Hello World</h1><p>Text here &amp; more.</p></body></html>"
    cleaned = clean_html_text(raw)
    assert "Hello World" in cleaned
    assert "Text here & more." in cleaned
    assert "body {color:red}" not in cleaned

def test_extract_html_title():
    raw = "<html><head><title>My Article Title</title></head><body><h1>Heading</h1></body></html>"
    assert extract_html_title(raw, "file.html") == "My Article Title"

    raw_no_title = "<html><body><h1>Only H1 Heading</h1></body></html>"
    assert extract_html_title(raw_no_title, "file.html") == "Only H1 Heading"

def test_extract_md_title():
    content = "---\nkey: val\n---\n# Real Title\n\nSome text"
    assert extract_md_title(content, "file.md") == "Real Title"

    content_no_h1 = "Just text line 1\nJust text line 2"
    assert extract_md_title(content_no_h1, "my-file.md") == "My File"


def test_ingest_portfolio_yaml_injection_safety_txt_tagging_and_pruning(tmp_path):
    """Ingestor safely serializes tricky titles, reads .txt, tags summary lines, uses dynamic timestamp, and prunes stale files."""
    from src.scripts.ingest_portfolio import ingest_portfolio

    portfolio_dir = tmp_path / "portfolio"
    portfolio_dir.mkdir()
    target_file = tmp_path / "target.md"
    target_file.write_text("# Target Role\nEnterprise Architect\n", encoding="utf-8")

    # Tricky title with quotes, colons, backslashes, plus canonical career record
    (portfolio_dir / "canonical").mkdir()
    (portfolio_dir / "canonical" / "career-record.yaml").write_text(
        "metadata: {}\nidentity: {}\neducation: []\ncertifications: []\ncareer: []\n",
        encoding="utf-8",
    )
    (portfolio_dir / "articles").mkdir()
    (portfolio_dir / "articles" / "tricky.md").write_text(
        '# Title with "quotes": and \\ backslash\nLine one\nLine two\n',
        encoding="utf-8",
    )
    (portfolio_dir / "notes.txt").write_text(
        "Plain text portfolio note content.\nSecond line.\n",
        encoding="utf-8",
    )

    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(
        yaml.safe_dump(
            {
                "candidate": {
                    "name": "Candidate",
                    "portfolio_dir": str(portfolio_dir),
                    "canonical_record": "canonical/career-record.yaml",
                },
                "target_opportunity": {"source": str(target_file)},
            }
        ),
        encoding="utf-8",
    )

    out_root = tmp_path / "repo"
    stale_dir = out_root / "out" / "okf" / "sources"
    stale_dir.mkdir(parents=True)
    (stale_dir / "stale-quarantined.md").write_text("old", encoding="utf-8")

    ingest_portfolio(config_path=cfg_path, repo_root=out_root)

    # Stale file pruned
    assert not (stale_dir / "stale-quarantined.md").exists()

    # YAML frontmatter parses cleanly with safe_load
    tricky_out = (stale_dir / "articles-tricky.md").read_text(encoding="utf-8")
    fm_text = tricky_out.split("---", 2)[1]
    parsed_fm = yaml.safe_load(fm_text)
    assert parsed_fm["title"] == 'Title with "quotes": and \\ backslash'

    # Summary line is tagged with [evidence] and footnote
    assert "[evidence] " in tricky_out
    assert "[^articles-tricky]" in tricky_out
    summary_section = tricky_out.split("## Summary / Abstract", 1)[1].strip()
    assert summary_section.startswith("[evidence]")

    # .txt file snippet captured
    txt_out = (stale_dir / "notes.md").read_text(encoding="utf-8")
    assert "Plain text portfolio note content." in txt_out

    # index.md timestamp is dynamic (not hardcoded 2026-08-14)
    index_text = (stale_dir / "index.md").read_text(encoding="utf-8")
    assert "2026-08-14T14:12:00+01:00" not in index_text


def test_ingest_portfolio_fails_fast_on_missing_portfolio_dir(tmp_path):
    from src.scripts.ingest_portfolio import ingest_portfolio

    target_file = tmp_path / "target.md"
    target_file.write_text("# Target", encoding="utf-8")
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(
        yaml.safe_dump(
            {
                "candidate": {"portfolio_dir": str(tmp_path / "does-not-exist")},
                "target_opportunity": {"source": str(target_file)},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(FileNotFoundError):
        ingest_portfolio(config_path=cfg_path, repo_root=tmp_path)
