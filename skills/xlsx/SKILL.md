---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
license: Proprietary. LICENSE.txt has complete terms
---

# Excel Processing

Use this skill to create, modify, or analyze spreadsheet files.

## 1. Core Workflow

1. **Select Tool**: Choose `pandas` for bulk data analysis or `openpyxl` for formatting, styling, and dynamic formulas.
2. **Build Formulas**: **NEVER** hardcode values computed in Python if they can be calculated dynamically. Write Excel formulas (e.g., `=SUM(...)`, `=AVERAGE(...)`).
3. **Apply Design System**: Maintain a clean, professional, and consistent format. Refer to [output-requirements.md](references/output-requirements.md) for color codes and standards.
4. **Recalculate (MANDATORY)**: Always run `python scripts/recalc.py <output_file>` after creating or modifying spreadsheets with formulas to generate cached values.
5. **Verify**: Check the recalculation JSON output and follow the verification checklist in [verificacion-formulas.md](references/verificacion-formulas.md).

## 2. Reference Library

- **Design Rules**: Consult [output-requirements.md](references/output-requirements.md) for details on fonts, color conventions, margins, decimals, and assumptions placement.
- **Code Snippets**: Consult [pandas-openpyxl.md](references/pandas-openpyxl.md) for templates on reading/writing with pandas and openpyxl.
- **Verification Checklist**: Consult [verificacion-formulas.md](references/verificacion-formulas.md) for error checking and debugging.