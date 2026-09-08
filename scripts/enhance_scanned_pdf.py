# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pymupdf>=1.24.9",
#     "opencv-python>=4.10.0.84",
#     "numpy>=1.26.0",
# ]
# ///

"""
enhance_scanned_pdf.py
Deterministic pipeline for PDF restoration via PyMuPDF and OpenCV.
Includes idempotency checks for native PDFs and resolution-agnostic CV parameters.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
import cv2
import fitz  # PyMuPDF
import numpy as np


def is_digital_native(doc: fitz.Document, page_index: int = 0) -> bool:
    """
    Idempotency check: determines whether a PDF page is a clean native digital document
    or a rasterized/photographed physical scan.
    """
    page = doc[page_index]
    text = page.get_text()
    images = page.get_images()

    # If page has extractable text and NO full-page background images, it's digital native
    if len(text.strip()) > 50 and len(images) == 0:
        return True

    # If there is a single image spanning the full page rect, it's a scanned photo
    page_rect = page.rect
    for img_info in images:
        xref = img_info[0]
        base_img = doc.extract_image(xref)
        img_w, img_h = base_img["width"], base_img["height"]
        # Check if the image roughly matches page aspect ratio and covers the canvas
        if img_w > 500 and img_h > 500:
            aspect_page = page_rect.width / (page_rect.height + 1e-5)
            aspect_img = img_w / (img_h + 1e-5)
            if abs(aspect_page - aspect_img) < 0.2:
                # Also check background uniformity of rendered page
                pix = page.get_pixmap(dpi=72)
                img_arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.h, pix.w, pix.n))
                gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY) if pix.n >= 3 else img_arr[:, :, 0]
                # Scanned paper has mottled/noisy background with variance in high percentiles
                bg_sample = gray[int(pix.h * 0.3):int(pix.h * 0.4), int(pix.w * 0.3):int(pix.w * 0.7)]
                # If background is not pure uniform 255 (paper texture/shadows), it is a physical scan
                if np.mean(bg_sample) < 240 or np.std(bg_sample) > 3.0:
                    return False

    return len(text.strip()) > 30


def deskew_image(img_bgr: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Calculates median orientation of text lines using Hough line transform and deskews the image.
    """
    h, w = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Threshold inverted for Hough lines
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Use central region to avoid outer border skew
    y1, y2 = int(h * 0.05), int(h * 0.95)
    x1, x2 = int(w * 0.05), int(w * 0.95)
    center_roi = thresh[y1:y2, x1:x2]

    min_line_len = max(50, int(w * 0.08))
    lines = cv2.HoughLinesP(center_roi, 1, np.pi / 180, 100, minLineLength=min_line_len, maxLineGap=25)

    angles = []
    if lines is not None:
        for line in lines:
            lx1, ly1, lx2, ly2 = line.ravel()[:4]
            angle = np.degrees(np.arctan2(ly2 - ly1, lx2 - lx1))
            if abs(angle) < 15:
                angles.append(angle)

    median_angle = float(np.median(angles)) if angles else 0.0

    if abs(median_angle) > 0.1:
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated = cv2.warpAffine(img_bgr, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated, median_angle

    return img_bgr, 0.0


def restore_scanned_image(img_bgr: np.ndarray, deskew: bool = True) -> np.ndarray:
    """
    Resolution-agnostic document restoration pipeline:
    - Dynamic kernel Gaussian background division
    - Percentile-based contrast stretching
    - Bounding box margin filtering & barcode preservation
    """
    if deskew:
        img_bgr, _ = deskew_image(img_bgr)

    h, w = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # 1. Dynamic kernel Gaussian background estimation
    ksize = int(max(w, h) * 0.05)
    if ksize % 2 == 0:
        ksize += 1
    sigma = max(10, ksize // 3)

    bg = cv2.GaussianBlur(gray, (ksize, ksize), sigma)
    # Illumination division
    div = np.clip((gray.astype(np.float32) / (bg.astype(np.float32) + 1e-5)) * 255.0, 0, 255).astype(np.uint8)

    # 2. Dynamic range mapping using robust percentiles
    p_low = float(np.percentile(div, 1.5))
    p_high = float(np.percentile(div, 96.0))
    if p_high <= p_low:
        p_high = p_low + 1.0

    res = np.clip((div.astype(np.float32) - p_low) / (p_high - p_low) * 255.0, 0, 255).astype(np.uint8)

    # 3. Dynamic content bounding box & safe margin cleaning
    binary_content = (res < 200).astype(np.uint8)
    content_y, content_x = np.where(binary_content > 0)

    if len(content_x) > 0 and len(content_y) > 0:
        # Ignore extreme border artifacts (outer 1%) when finding main content bounds
        margin_x_min = max(0, int(np.percentile(content_x, 0.5) - 25))
        margin_x_max = min(w, int(np.percentile(content_x, 99.5) + 35))
        margin_y_min = max(0, int(np.percentile(content_y, 0.5) - 25))
        margin_y_max = min(h, int(np.percentile(content_y, 99.5) + 25))

        # Clean outer margins outside content
        if margin_y_min > 0:
            res[:margin_y_min, :] = 255
        if margin_y_max < h:
            res[margin_y_max:, :] = 255
        if margin_x_min > 0:
            res[:, :margin_x_min] = 255
        if margin_x_max < w:
            res[:, margin_x_max:] = 255

    # 4. Connected-component speckle filtering protecting punctuation and barcodes
    binary_for_cc = (res < 200).astype(np.uint8)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_for_cc, connectivity=8)

    clean_mask = np.ones_like(res, dtype=bool)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        # Only target microscopic speckles
        if area < 12:
            cx, cy = int(centroids[i][0]), int(centroids[i][1])
            x_min, x_max = max(0, cx - 35), min(w, cx + 35)
            y_min, y_max = max(0, cy - 35), min(h, cy + 35)
            # Check neighborhood for other components
            local_cc = binary_for_cc[y_min:y_max, x_min:x_max].copy()
            local_cc[labels[y_min:y_max, x_min:x_max] == i] = 0
            # If completely isolated from letters/words, it is scanner dust
            if np.sum(local_cc) == 0:
                res[labels == i] = 255

    return res


def process_document(
    input_path: str | Path,
    output_dir: str | Path | None = None,
    dpi: int = 300,
    deskew: bool = True,
) -> list[Path]:
    """
    Processes a PDF or image file:
    - Runs idempotency check
    - Renders at specified DPI
    - Restores scanned pages or preserves digital natives
    - Saves high-quality output JPGs
    """
    input_path = Path(input_path).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_files: list[Path] = []
    base_stem = input_path.stem

    if input_path.suffix.lower() == ".pdf":
        doc = fitz.open(str(input_path))
        num_pages = len(doc)
        matrix = fitz.Matrix(dpi / 72.0, dpi / 72.0)

        for page_idx in range(num_pages):
            page = doc[page_idx]
            pix = page.get_pixmap(matrix=matrix)
            img_arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.h, pix.w, pix.n))
            if pix.n == 4:
                img_bgr = cv2.cvtColor(img_arr, cv2.COLOR_RGBA2BGR)
            elif pix.n == 3:
                img_bgr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = cv2.cvtColor(img_arr, cv2.COLOR_GRAY2BGR)

            suffix = "" if num_pages == 1 else f"_page_{page_idx + 1}"
            out_file = output_dir / f"{base_stem}{suffix}.jpg"

            # Check idempotency
            if is_digital_native(doc, page_idx):
                print(f"[Page {page_idx + 1}] Native vector PDF detected. Bypassing raster restoration.")
                cv2.imwrite(str(out_file), img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])
            else:
                print(f"[Page {page_idx + 1}] Physical scan detected. Applying resolution-agnostic restoration.")
                cleaned = restore_scanned_image(img_bgr, deskew=deskew)
                cv2.imwrite(str(out_file), cleaned, [cv2.IMWRITE_JPEG_QUALITY, 98])

            output_files.append(out_file)
            print(f"Saved: {out_file}")
    else:
        # Direct image file
        img_bgr = cv2.imread(str(input_path))
        if img_bgr is None:
            raise ValueError(f"Could not decode image at {input_path}")
        cleaned = restore_scanned_image(img_bgr, deskew=deskew)
        out_file = output_dir / f"{base_stem}_cleaned.jpg"
        cv2.imwrite(str(out_file), cleaned, [cv2.IMWRITE_JPEG_QUALITY, 98])
        output_files.append(out_file)
        print(f"Saved: {out_file}")

    return output_files


def run_tests() -> int:
    """
    Executes regression validation against specified test fixtures:
    1. 20260809_140145.PDF (Dirty scan)
    2. 20260809_140119.PDF (Dirty scan)
    3. digital_native_test.pdf (Clean vector PDF)
    """
    print("=== Running Curo PDF Restoration Test Suite ===")
    test_cases = [
        ("E:/Pipeline/20260809_140145.PDF", False),  # Expected: scanned
        ("E:/Pipeline/20260809_140119.PDF", False),  # Expected: scanned
        ("E:/Pipeline/digital_native_test.pdf", True), # Expected: digital native
    ]

    all_passed = True
    temp_test_dir = Path("E:/Pipeline/test_output")
    temp_test_dir.mkdir(parents=True, exist_ok=True)

    for path_str, expected_native in test_cases:
        p = Path(path_str)
        if not p.exists():
            print(f"ERROR: Fixture {p} does not exist!")
            all_passed = False
            continue

        doc = fitz.open(str(p))
        actual_native = is_digital_native(doc, 0)
        status_str = "PASS" if actual_native == expected_native else "FAIL"
        print(f"[{status_str}] {p.name}: is_digital_native = {actual_native} (expected {expected_native})")
        if actual_native != expected_native:
            all_passed = False

        # Run process_document
        outputs = process_document(p, output_dir=temp_test_dir, dpi=300)
        if not outputs or not outputs[0].exists():
            print(f"ERROR: No output generated for {p.name}")
            all_passed = False
        else:
            # Verify image properties
            out_img = cv2.imread(str(outputs[0]), cv2.IMREAD_GRAYSCALE)
            mean_val = float(np.mean(out_img))
            p99 = float(np.percentile(out_img, 99))
            print(f"       -> Generated: {outputs[0].name} ({out_img.shape[1]}x{out_img.shape[0]}), mean={mean_val:.1f}, p99={p99:.1f}")
            if p99 < 250:
                print("       -> WARNING: Background was not normalized to pure white!")
                all_passed = False

    print("================================================")
    if all_passed:
        print("ALL TESTS PASSED: Document restoration pipeline verified.")
        return 0
    else:
        print("TEST FAILURES OCCURRED.")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic pipeline for scanned PDF restoration.")
    parser.add_argument("--input", "-i", type=str, help="Path to input PDF or image file.")
    parser.add_argument("--output", "-o", type=str, default=None, help="Directory to save output files.")
    parser.add_argument("--dpi", type=int, default=300, help="Rendering DPI (default: 300).")
    parser.add_argument("--no-deskew", action="store_true", help="Disable automatic deskewing.")
    parser.add_argument("--test", action="store_true", help="Run deterministic regression tests on standard fixtures.")

    args = parser.parse_args()

    if args.test:
        return run_tests()

    if not args.input:
        parser.print_help()
        return 1

    process_document(args.input, output_dir=args.output, dpi=args.dpi, deskew=not args.no_deskew)
    return 0


if __name__ == "__main__":
    sys.exit(main())
