# Excel Formula Recalculation & Verification

This guide explains how to recalculate and verify formulas in generated Excel sheets.

## Recalculating Formulas

Excel files created or modified by libraries like `openpyxl` contain formulas as strings but not calculated values. You **MUST** run the recalculation tool to populate the formula results and ensure compatibility.

Run `recalc.py` (which uses LibreOffice headlessly):

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

Example:
```bash
python scripts/recalc.py output.xlsx 30
```

### Script Behavior
- Automatically sets up a LibreOffice macro on the first run.
- Recalculates all formulas in all sheets.
- Scans ALL cells for Excel errors (`#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`).
- Returns JSON with detailed error locations and counts.

---

## Interpreting scripts/recalc.py Output

The script returns JSON detailing calculation errors:

```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

If the status is `"errors_found"`, investigate the locations listed and fix the calculations in your code, then run `recalc.py` again.

---

## Formula Verification Checklist

Use this checklist to ensure formulas and data are correct:

### Essential Verification
- [ ] **Test 2-3 sample references**: Verify they pull correct values before building the full model.
- [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK).
- [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6).

### Common Pitfalls
- [ ] **NaN handling**: Check for null values with `pd.notna()`.
- [ ] **Far-right columns**: FY data often in columns 50+.
- [ ] **Multiple matches**: Search all occurrences, not just the first.
- [ ] **Division by zero**: Check denominators before using `/` in formulas (`#DIV/0!`).
- [ ] **Wrong references**: Verify all cell references point to intended cells (`#REF!`).
- [ ] **Cross-sheet references**: Use correct format (`Sheet1!A1`) for linking sheets.

### Formula Testing Strategy
- [ ] **Start small**: Test formulas on 2-3 cells before applying broadly.
- [ ] **Verify dependencies**: Check all cells referenced in formulas exist.
- [ ] **Test edge cases**: Include zero, negative, and very large values.
