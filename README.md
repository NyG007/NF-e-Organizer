# NyG — Organizer de NF-e

NyG Organizer de NF-e is a Python-based system designed to automate the processing and organization of Brazilian electronic invoices (NF-e).

The system reads XML files, extracts key financial and identification data, and organizes documents into a structured directory hierarchy based on year and month.

## Problem

Companies often deal with large volumes of NF-e files stored in unstructured folders, leading to:

- Time-consuming manual organization
- High risk of human error
- Difficulty in tracking financial data

## Solution

This project automates the entire workflow:

1. Reads XML invoice files
2. Extracts relevant data (CNPJ, value, date)
3. Organizes files into folders (year/month)
4. Generates structured reports for analysis

## Features
- XML batch processing
- NF-e data extraction:
  - CNPJ (issuer)
  - Total invoice value
  - Emission date
- Automatic folder organization (/YYYY/MM)
- Data aggregation with pandas
- Report generation (CSV / Excel)
- Error handling for invalid XML files

## Tech Stack
- Language: Python 3.x
- Libraries:
  - xml.etree.ElementTree
  - os
  - pandas

# License

This project is licensed under the MIT License.

# Author

NyG007 — Built for real-world automation and scalability.
