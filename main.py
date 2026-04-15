# main.py
# NyG — NF-e Organizer
# Issue #2 — Extract basic NF-e data (CNPJ, value, date)

import xml.etree.ElementTree as ET
import os

# ── Config ────────────────────────────────────────────────
SAMPLE_FILE = "sample_nfe.xml"                                  # path to the sample XML file used for testing
NAMESPACE   = {"nfe": "http://www.portalfiscal.inf.br/nfe"}     # NF-e namespace prefix required for tag lookup

# ── Loader ────────────────────────────────────────────────
def load_xml(filepath: str) -> ET.Element | None:    # receives a file path and returns the root element or None
    if not os.path.exists(filepath):                 # checks if the file exists before trying to open it
        print(f"[ERROR] File not found: {filepath}") # warns the user if the path is invalid
        return None                                  # stops execution and returns None to the caller

    try:
        tree = ET.parse(filepath)                    # parses the XML file into an ElementTree object
        root = tree.getroot()                        # gets the root element of the XML tree
        print(f"[OK] File loaded: {filepath}")       # confirms the file was loaded successfully
        print(f"[OK] Root tag:    {root.tag}")       # prints the root tag including namespace
        return root                                  # returns the root element for further processing

    except ET.ParseError as e:                       # catches malformed or corrupted XML files
        print(f"[ERROR] Failed to parse XML: {e}")   # prints the parse error details
        return None                                  # returns None so the caller can handle the failure

# ── Extractor ─────────────────────────────────────────────
def extract_data(root: ET.Element) -> dict | None:  # receives the root of the XML and returns a dictionary or None
    try:
        ns = NAMESPACE                                                        # local shortcut to the namespace

        cnpj  = root.find(".//nfe:emit/nfe:CNPJ", ns).text                    # Navigate to the CNPJ tag and retrieve the text
        value = root.find(".//nfe:total/nfe:ICMSTot/nfe:vNF", ns).text        # Navigate to the total value of the invoice
        date  = root.find(".//nfe:ide/nfe:dhEmi", ns).text                    # navigate to the issue date

        return {
            "cnpj" : cnpj,          # CNPJ as a string, e.g., 12345678000195
            "value": float(value),  # value converted to float ex: 1500.0
            "date" : date[:10],     # only the first 10 characters e.g. 2026-04-14
        }

    except AttributeError:                                      # Triggered when .find() returns None and .text fails
        print("[ERROR] Required tag not found in XML")          # indicates which file is having problems
        return None                                             # Returns None for the caller to handle.

# ── Main ──────────────────────────────────────────────────
if __name__ == "__main__":          # ensures that it only runs when run directly
    root = load_xml(SAMPLE_FILE)    # loads the XML and returns the root element

    if root is not None:                # only proceeds if the file was loaded successfully
        data = extract_data(root)       # extracts CNPJ, value and date from the root element

        if data:                                        # only prints if extraction returned valid data
            print(f"[OK] CNPJ: {data['cnpj']}")         # prints the issuer CNPJ
            print(f"[OK] Value: {data['value']}")       # prints the total invoice value as float
            print(f"[OK] Date: {data['date']}")         # prints the emission date formatted as YYYY-MM-DD