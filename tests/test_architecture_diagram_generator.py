import os
import subprocess
import sys
import xml.etree.ElementTree as ET
import pytest


def test_architecture_diagram_generator_script_runs(tmp_path):
    script_path = "src/scripts/generate_architecture_diagrams.py"
    assert os.path.exists(script_path), f"Missing script at {script_path}"

    result = subprocess.run(
        [sys.executable, script_path, "--output-dir", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"
    assert "Architecture Diagram Auto-Generation Complete" in result.stdout
    out_xml = tmp_path / "4-layer-pipeline.drawio.xml"
    assert out_xml.exists()
    ET.parse(out_xml)


def test_drawio_xml_file_exists_and_valid():
    xml_path = "docs/architecture/4-layer-pipeline.drawio.xml"
    assert os.path.exists(xml_path), f"Missing Draw.io XML at {xml_path}"
    tree = ET.parse(xml_path)
    root = tree.getroot()
    assert root.tag == "mxfile"
    with open(xml_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "4-Layer Pipeline Architecture" in content


def test_architecture_md_contains_mermaid_markers():
    arch_path = "ARCHITECTURE.md"
    assert os.path.exists(arch_path)
    with open(arch_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<!-- BEGIN AUTO-GENERATED ARCHITECTURE DIAGRAM -->" in content
    assert "<!-- END AUTO-GENERATED ARCHITECTURE DIAGRAM -->" in content
    assert "```mermaid" in content
