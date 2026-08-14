import os
import shutil
import tempfile
import yaml
import pytest
from pathlib import Path
from scripts.ingest_portfolio import make_slug, determine_category, clean_html_text, extract_html_title, extract_md_title

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
