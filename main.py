# main.py
# NyG — NF-e Organizer
# Issue #1 — Create XML reader base structure

import xml.etree.ElementTree as ET
import os

# ── Config ────────────────────────────────────────────────
SAMPLE_FILE = "sample_nfe.xml"
NAMESPACE   = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

# ── Loader ────────────────────────────────────────────────
def load_xml(filepath: str) -> ET.Element | None:
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return None

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        print(f"[OK] File loaded: {filepath}")
        print(f"[OK] Root tag:    {root.tag}")
        return root

    except ET.ParseError as e:
        print(f"[ERROR] Failed to parse XML: {e}")
        return None

# ── Main ──────────────────────────────────────────────────
if __name__ == "__main__":
    root = load_xml(SAMPLE_FILE)