# main.py
# NyG — NF-e Organizer
# Issue #2 — Extract basic NF-e data (CNPJ, value, date)

import xml.etree.ElementTree as ET
import os

# ── Config ────────────────────────────────────────────────
SAMPLE_FILE = "sample_nfe.xml"                                  # path to the sample XML file used for testing
NAMESPACE   = {"nfe": "http://www.portalfiscal.inf.br/nfe"}     # NF-e namespace prefix required for tag lookup
SAMPLE_DIR = "samples"                                          # path to the folder containing XML files
OUTPUT_DIR = "Notes"                                            # root folder where organized files will be stored

# ── Loader ────────────────────────────────────────────────
def load_xml(filepath: str) -> ET.Element | None:               # receives a file path and returns the root element or None
    if not os.path.exists(filepath):                            # checks if the file exists before trying to open it
        print(f"[ERROR] File not found: {filepath}")            # warns the user if the path is invalid
        return None                                             # stops execution and returns None to the caller

    try:
        tree = ET.parse(filepath)                               # parses the XML file into an ElementTree object
        root = tree.getroot()                                   # gets the root element of the XML tree
        print(f"[OK] File loaded: {filepath}")                  # confirms the file was loaded successfully
        print(f"[OK] Root tag:    {root.tag}")                  # prints the root tag including namespace
        return root                                             # returns the root element for further processing

    except ET.ParseError as e:                                  # catches malformed or corrupted XML files
        print(f"[ERROR] Failed to parse XML: {e}")              # prints the parse error details
        return None                                             # returns None so the caller can handle the failure

# ── Extractor ─────────────────────────────────────────────
def extract_data(root: ET.Element) -> dict | None:              # receives the root of the XML and returns a dictionary or None
    try:
        ns = NAMESPACE                                          # local shortcut to the namespace

        cnpj  = root.find(".//nfe:emit/nfe:CNPJ", ns).text                    # Navigate to the CNPJ tag and retrieve the text
        value = root.find(".//nfe:total/nfe:ICMSTot/nfe:vNF", ns).text        # Navigate to the total value of the invoice
        date  = root.find(".//nfe:ide/nfe:dhEmi", ns).text                    # navigate to the issue date

        return {
            "cnpj" : cnpj,                                      # CNPJ as a string, e.g., 12345678000195
            "value": float(value),                              # value converted to float ex: 1500.0
            "date" : date[:10],                                 # only the first 10 characters e.g. 2026-04-14
        }

    except AttributeError:                                      # Triggered when .find() returns None and .text fails
        print("[ERROR] Required tag not found in XML")          # indicates which file is having problems
        return None                                             # Returns None for the caller to handle.

# ── Processor ─────────────────────────────────────────────
def process_directory(folder: str) -> list:                     # receives a folder path and returns a list of dicts
    results = []                                                # stores successfully extracted data from each file

    for filename in os.listdir(folder):                         # iterates over every item in the folder
        if not filename.endswith(".xml"):                       # skips any file that is not an XML
            continue

        filepath = os.path.join(folder, filename)               # builds the full path to the file
        root = load_xml(filepath)                               # loads and parses the XML file

        if root is None:                                        # skips the file if loading failed
            continue

        data = extract_data(root)                               # extracts CNPJ, value and date from the root

        if data:                                                # only appends if extraction was successful
            data["filename"] = filename                         # adds the filename to the dict for reference
            results.append(data)                                # adds the extracted data to the results list

    return results                                              # returns all successfully processed records

# ── Folder Builder ────────────────────────────────────────
def create_folder_structure(date: str) -> str:                  # receives a date string and returns the created path
    year = date[:4]                                             # extracts the year  ex: "2026"
    month = date[5:7]                                           # extracts the month ex: "04"

    path = os.path.join(OUTPUT_DIR, year, month)                # builds the full path ex: Notes/2026/04

    os.makedirs(path, exist_ok=True)                            # creates all folders in the path, skips if they exist

    print(f"[OK] Folder ready: {path}")                         # confirms the folder was created or already exists
    return path                                                 # returns the path for use in the next step

# ── Main ──────────────────────────────────────────────────
if __name__ == "__main__":                                      # ensures that it only runs when run directly
    records = process_directory(SAMPLE_DIR)                     # processes all XML files in the samples folder

    print(f"\n[OK] {len(records)} file(s) processed\n")         # prints the total number of files processed
    for record in records:                                      # loops through each successfully extracted record
        print(f"  File:  {record['filename']}")                 # prints the source filename
        print(f"  CNPJ:  {record['cnpj']}")                     # prints the issuer CNPJ
        print(f"  Value: {record['value']}")                    # prints the total invoice value
        print(f"  Date:  {record['date']}")                     # prints the emission date
        print()                                                 # blank line between records