# OpenXML Word Processing (docx) XML Reference

This guide details the schemas and tag structures required when modifying Word processing XML files directly.

## Schema Compliance

Word is strict about element order inside property blocks.

### Property Block (`<w:pPr>`) Element Order
Tags inside `<w:pPr>` must appear in this order:
1. `<w:pStyle>` (Style reference)
2. `<w:numPr>` (Numbering configuration)
3. `<w:spacing>` (Paragraph spacing)
4. `<w:ind>` (Indentation)
5. `<w:jc>` (Justification / Alignment)
6. `<w:rPr>` (Run properties - must be last)

### Whitespace Preservation
Always add `xml:space="preserve"` to `<w:t>` elements that contain leading or trailing spaces:
```xml
<w:t xml:space="preserve"> leading space and trailing </w:t>
```

### Relationship IDs (RSIDs)
Must be valid 8-digit hex values (e.g., `<w:p w:rsidR="00AB1234">`).

---

## Tracked Changes (w:ins & w:del)

Always replace the entire `<w:r>` run with the tracked changes tags. Do not put tracked change tags inside a run.

### Insertion (`<w:ins>`)
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r>
    <w:rPr>
      <!-- Copy style formatting from parent run -->
    </w:rPr>
    <w:t>inserted text</w:t>
  </w:r>
</w:ins>
```

### Deletion (`<w:del>`)
Deletions use `<w:delText>` instead of `<w:t>`:
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r>
    <w:rPr>
      <!-- Copy style formatting from parent run -->
    </w:rPr>
    <w:delText>deleted text</w:delText>
  </w:r>
</w:del>
```

### Deleting Paragraphs / List Items
To delete a paragraph mark (so it merges with the next paragraph), add `<w:del/>` inside `<w:pPr><w:rPr>`:
```xml
<w:p>
  <w:pPr>
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Paragraph content being deleted</w:delText></w:r>
  </w:del>
</w:p>
```

---

## Comments XML Structures

Comment range marks are direct children of `<w:p>`. They are siblings of `<w:r>`, **NEVER** children of `<w:r>`.

```xml
<w:p>
  <!-- Comment starts here -->
  <w:commentRangeStart w:id="0"/>
  <w:r>
    <w:t>This text is commented on</w:t>
  </w:r>
  <!-- Comment ends here -->
  <w:commentRangeEnd w:id="0"/>
  
  <!-- Comment reference marker -->
  <w:r>
    <w:rPr>
      <w:rStyle w:val="CommentReference"/>
    </w:rPr>
    <w:commentReference w:id="0"/>
  </w:r>
</w:p>
```
