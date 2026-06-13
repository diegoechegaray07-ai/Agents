# Editing Existing DOCX Documents

Word document (.docx) editing follows a strict **Unpack → Edit XML → Pack** workflow.

## The 3-Step Workflow

### Step 1: Unpack
Unzip and pretty-print the document XML:
```bash
python scripts/office/unpack.py document.docx unpacked/
```
This script extracts the XML, formatting it so it can be edited, and converts smart quotes to XML entities (e.g., `&#x2019;`) to preserve them.

### Step 2: Edit XML
Edit the XML files located in `unpacked/word/`.
- Use the editor tool directly for replacements.
- **Do not write Python scripts for simple string replacements** — this keeps diffs clean and avoids bugs.
- Reference the XML tag structure in [xml-reference.md](xml-reference.md).

#### Tracked Changes Author
- **Always use "Claude"** as the author for tracked changes (`w:author="Claude"`) and comments, unless the user requests otherwise.

### Step 3: Pack
Re-compile the folder back into a valid `.docx` file:
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
This script compresses the XML back into a `.docx` file and runs schema validation.

---

## Inserting Comments (Helper Script)
Use the `comment.py` script to generate XML comments and replies:

```bash
# Add a comment (comment ID 0)
python scripts/comment.py unpacked/ 0 "Comment text here"

# Add a reply to comment 0 (ID 1)
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0

# Set a custom author
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"
```
After executing the script, insert the comment markers (`<w:commentRangeStart>` and `<w:commentRangeEnd>`) at the correct locations in `word/document.xml` (see [xml-reference.md](xml-reference.md)).

---

## Accepting Tracked Changes
To accept all tracked changes and produce a clean document:
```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## Adding Images to XML
To insert an image manually in the XML:
1. Copy the image file to `word/media/`.
2. Register the relationship in `word/_rels/document.xml.rels`:
   ```xml
   <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
   ```
3. Add the content type mapping in `[Content_Types].xml`:
   ```xml
   <Default Extension="png" ContentType="image/png"/>
   ```
4. Insert a `<w:drawing>` element in `word/document.xml` referencing the relationship ID (`rId5`):
   ```xml
   <w:drawing>
     <wp:inline>
       <wp:extent cx="914400" cy="914400"/> <!-- 914400 EMUs = 1 inch -->
       <a:graphic>
         <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/main">
           <pic:pic>
             <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
           </pic:pic>
         </a:graphicData>
       </a:graphic>
     </wp:inline>
   </w:drawing>
   ```
