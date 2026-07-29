import os
import yaml
import pytest

def test_skills_exist():
    expected_skills = [
        "playbook-orchestrator",
        "portfolio-ingestor",
        "portfolio-analyzer",
        "achievement-extractor",
        "evidence-card-generator",
        "signature-theme-miner",
        "narrative-generator",
        "interview-strategy-generator",
        "knowledge-gaps",
        "playbook-assembler",
    ]
    skills_dir = "skills"
    for skill in expected_skills:
        skill_path = os.path.join(skills_dir, skill, "SKILL.md")
        assert os.path.exists(skill_path), f"Missing skill definition at {skill_path}"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert content.startswith("---"), f"Skill {skill} missing frontmatter delimiter"
            assert "name: " + skill in content, f"Skill {skill} missing name frontmatter"


def test_config_example_valid():
    config_path = "config/config.example.yaml"
    assert os.path.exists(config_path), "Missing config/config.example.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        assert "project" in data
        assert "inputs" in data
        assert "target_opportunity" in data
        assert "output" in data
        assert "pipeline" in data


def test_fixtures_minimal_exist():
    fixture_dir = "tests/fixtures/portfolio_minimal"
    for filename in ["cv.md", "target-jd.md", "config.yaml"]:
        assert os.path.exists(os.path.join(fixture_dir, filename))
