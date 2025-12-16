# -*- coding: utf-8 -*-
"""
Utility: Convert all PDF files in a given folder into per-page PNG images.

Usage:
    python pdf_to_images_util.py --input_dir /path/to/pdfs --output_dir /path/to/output_images
"""

import os
import argparse
from pathlib import Path
from pdf2image import convert_from_path


# ---------------------------------------------------------------------
# Hardcoded folder paths (change as needed)
# ---------------------------------------------------------------------
INPUT_DIR = Path("/workspace/pdfs")        # folder containing PDFs
OUTPUT_DIR = Path("/workspace/page_images") # folder to save PNGs
DPI = 300  # image quality; 300 is standard, 400 for small fonts
# ---------------------------------------------------------------------

def convert_pdf_to_images(pdf_path: Path, output_dir: Path, dpi: int = 300):
    """Convert a single PDF file into multiple PNG images (one per page)."""
    try:
        pages = convert_from_path(pdf_path, dpi=dpi)
        pdf_output_dir = output_dir / pdf_path.stem
        pdf_output_dir.mkdir(parents=True, exist_ok=True)

        for i, page in enumerate(pages, start=1):
            image_path = pdf_output_dir / f"{pdf_path.stem}_page_{i:03}.png"
            page.save(image_path, "PNG")
            print(f"? Saved: {image_path}")

        print(f"? Completed: {pdf_path.name} ({len(pages)} pages)\n")

    except Exception as e:
        print(f"? Error converting {pdf_path.name}: {e}")


def batch_convert_pdfs(input_dir: Path, output_dir: Path, dpi: int = 300):
    """Convert all PDF files found in input_dir."""
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return

    for pdf_path in pdf_files:
        convert_pdf_to_images(pdf_path, output_dir, dpi=dpi)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    batch_convert_pdfs(INPUT_DIR, OUTPUT_DIR, dpi=DPI)
    print("?? PDF-to-Image conversion complete.")
