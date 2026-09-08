---
name: "pdf"
description: "Use when tasks involve reading, creating, rendering, enhancing, or reviewing PDF files. Includes host-independent rendering (PyMuPDF via uv), resolution-agnostic document scan restoration (deformity/crease/shadow/bleed-through removal), idempotency checks for native vector PDFs, and visual quality validation."
---


# PDF Skill

## When to use
- Read or review PDF content where layout and visuals matter.
- Create PDFs programmatically with reliable formatting.
- Convert PDF documents to high-resolution images (JPG/PNG).
- Clean up scanned or photographed PDF documents (remove paper creases, shadows, bleed-through text, and skew).
- Validate final rendering before delivery.

## Workflow

### 1. Host-Independent Rendering (Default)
- **Mandatory Execution**: Render PDF pages to images using `pymupdf` executed via `uv run` (or Python with PyMuPDF). Do NOT assume host-bound utilities like Poppler (`pdftoppm`) or Ghostscript are available.
- **DPI Selection**: Default to 300 DPI for high legibility (`matrix = pymupdf.Matrix(300 / 72, 300 / 72)`).

### 2. Idempotency Check (Bypass for Native Vector PDFs)
- Always verify document bimodality and text vector streams before applying raster restoration.
- If a document contains native digital vector text and exhibits high background uniformity (e.g., pure white background with >98% pixel brightness uniformity and standard font rendering), **bypass raster restoration** completely to preserve vector anti-aliasing and prevent unnecessary raster artifacts.

### 3. Deformity Removal Protocol (Resolution-Agnostic)
When processing scanned or photographed paper documents with physical deformities:
- **Deskewing**: Compute text line orientation via Hough Line Transform (`cv2.HoughLinesP`) on inverted binary text mask, calculate median angle of near-horizontal lines, and rotate the image affine matrix to level text.
- **Illumination Division (Dynamic Kernel)**:
  - Do NOT hardcode kernel sizes. Compute dynamic kernel dimensions based on image scale:
    ```python
    ksize = int(max(width, height) * 0.05)
    if ksize % 2 == 0:
        ksize += 1
    sigma = max(10, ksize // 3)
    bg = cv2.GaussianBlur(gray, (ksize, ksize), sigma)
    normalized = np.clip((gray.astype(np.float32) / (bg.astype(np.float32) + 1e-5)) * 255, 0, 255).astype(np.uint8)
    ```
  - Dividing the raw grayscale by this low-frequency background flattens lighting gradients, erases creases, folds, and reverse-side bleed-through without paragraph halos.
- **Dynamic Range Mapping (Percentile-Based)**:
  - Do NOT use absolute pixel cutoffs. Compute percentile-based stretching to adapt to varying paper tint and scan exposure:
    ```python
    p_low = np.percentile(normalized, 1.5)
    p_high = np.percentile(normalized, 96.0)
    stretched = np.clip((normalized.astype(np.float32) - p_low) / (p_high - p_low) * 255, 0, 255).astype(np.uint8)
    ```
- **Safe Margin Cleaning & Barcode Preservation**:
  - Never apply blind coordinate cropping. Compute the outer convex/bounding hull of all dark components.
  - Zero out outer noise strictly outside the text/content bounding box.
  - Protect corner headers (`Page X of Y`), routing codes, and machine-readable barcodes (USPS Intelligent Mail, 2D DataMatrix) by using connected-component analysis with distance constraints before clearing small isolated dust speckles.

### 4. PDF Generation & Extraction
- Use `reportlab` to generate PDFs when creating new documents.
- Use `pdfplumber` (or `pypdf`) for text extraction and quick checks; do not rely on it for layout fidelity.
- After each meaningful update, re-render pages and verify alignment, spacing, and legibility.

## Temp and output conventions
- Use `tmp/pdfs/` for intermediate files; delete when done.
- Write final artifacts under `output/pdf/` when working in this repo.
- Keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```bash
uv pip install reportlab pdfplumber pypdf pymupdf opencv-python numpy pillow
```
If `uv` is unavailable:
```bash
python -m pip install reportlab pdfplumber pypdf pymupdf opencv-python numpy pillow
```

## Verified Deterministic Script
For one-command conversion, idempotency checks, and resolution-agnostic restoration, run:
```bash
uv run E:/curo/scripts/enhance_scanned_pdf.py --input document.pdf --output output_dir/
```

## Quality expectations
- Maintain polished visual design: consistent typography, spacing, margins, and section hierarchy.
- Avoid rendering issues: clipped text, overlapping elements, broken tables, black squares, or unreadable glyphs.
- Charts, tables, barcodes, and images must be sharp, aligned, and clearly labeled.
- Use ASCII hyphens only. Avoid U+2011 (non-breaking hyphen) and other Unicode dashes.
- Citations and references must be human-readable; never leave tool tokens or placeholder strings.

## Final checks
- Do not deliver until visual inspection shows zero defects.
- Confirm headers/footers, page numbering, barcodes, and section transitions look polished.
- Clean intermediate files after final verification.
