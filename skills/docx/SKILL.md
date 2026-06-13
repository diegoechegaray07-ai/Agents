---
name: docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
license: Proprietary. LICENSE.txt has complete terms
---

# Word Document Processing (.docx)

Use this skill to create, extract text from, or edit Word documents.

## 1. Core Workflow

1. **Decide the Task**:
   - For **reading/analyzing** Word files: Use `extract-text <file.docx>` or unpack to inspect raw XML.
   - For **creating new** documents: Use the `docx-js` JavaScript library (run using Node.js).
   - For **editing existing** documents: Follow the Unpack → Edit XML → Pack workflow.
2. **Design Standards**: Always use Arial as the default font, explicitly set US Letter page size, and use numbering lists (never unicode bullet text runs).
3. **Execute & Pack**: If modifying XML, package the folder back to a `.docx` file using the packing tool.
4. **Recalculation & Validation (MANDATORY)**: Always run `python scripts/office/validate.py <file.docx>` to verify XML structure compliance.

## 2. References

- **Creating Documents**: Read [creation-guide.md](references/creation-guide.md) for code structure, table column layouts, images, tab stops, and page numbering.
- **Editing Documents**: Read [editing-guide.md](references/editing-guide.md) for unpacking/packing CLI commands, tracked changes, and comments.
- **XML Properties & Schemas**: Read [xml-reference.md](references/xml-reference.md) for schema-compliant paragraph structures, tracked changes XML tags, and comment range starts/ends.
