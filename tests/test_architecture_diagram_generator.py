import os
import subprocess
import pytest


def test_architecture_diagram_generator_script_runs():
    script_path = "scripts/generate_architecture_diagrams.py"
    assert os.path.exists(script_path), f"Missing script at {script_path}"
    
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"
    assert "Architecture Diagram Auto-Generation Complete" in result.stdout


def test_drawio_xml_file_exists_and_valid():
    xml_path = "docs/architecture/4-layer-pipeline.drawio.xml"
    assert os.path.exists(xml_path), f"Missing Draw.io XML at {xml_path}"
    with open(xml_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<mxfile" in content
    assert "4-Layer Pipeline Architecture" in content


def test_architecture_md_contains_mermaid_markers():
    arch_path = "ARCHITECTURE.md"
    assert os.path.exists(arch_path)
    with open(arch_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<!-- BEGIN AUTO-GENERATED ARCHITECTURE DIAGRAM -->" in content
    assert "<!-- END AUTO-GENERATED ARCHITECTURE DIAGRAM -->" in content
    assert "```mermaid" in content
