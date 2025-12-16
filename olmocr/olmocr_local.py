# -*- coding: utf-8 -*-
"""
Offline local inference script for OCR (no API calls)
"""
"""
OCR batch inference
- Reads all .png images from /workspace/page_images/
- Runs OCR using locally loaded olmOCR model
- Saves each page output to /workspace/ocr_output/

Run:
    python olmocr_local.py
"""
import os
from pathlib import Path
from PIL import Image
import torch
from transformers import PreTrainedTokenizerFast, AutoProcessor, PreTrainedModel, AutoModelForVision2Seq, AutoModelForImageTextToText

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
MODEL_PATH = Path("/model/") # update model path
IMAGE_PATH = Path("/workspace/page_images")
OUTPUT_PATH = Path("/workspace/ocr_output")


# Load processor and model
processor = AutoProcessor.from_pretrained(MODEL_PATH, local_files_only=True, trust_remote_code=True)
model = AutoModelForImageTextToText.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
).to("cuda" if torch.cuda.is_available() else "cpu")


# Loop through all PNGs recursively
image_files = sorted(list(IMAGE_PATH.glob("**/*.png")))
if not image_files:
    print(f"No .png files found in {IMAGE_ROOT}")
    exit()

print(f"?? Found {len(image_files)} image files to process.\n")

for image_path in image_files:
    try:
        image = Image.open(image_path).convert("RGB")
        prompt = (
            "<|vision_start|><|image_pad|><|vision_end|>\n"
            "Extract all text exactly as it appears in the document, including tables and numeric values. "
            "Return plain text only."
        )

        # Prepare model input
        inputs = processor(
            text=[prompt],
            images=[image],
            return_tensors="pt"
        ).to(model.device)


        # Run inference
        with torch.inference_mode():
            output = model.generate(**inputs, max_new_tokens=2048, do_sample=False)
            result = processor.decode(output[0], skip_special_tokens=True)

        # Prepare output file path
        relative_pdf_folder = image_path.parent.name
        output_subdir = OUTPUT_PATH / relative_pdf_folder
        output_subdir.mkdir(parents=True, exist_ok=True)

        output_file = output_subdir / f"{image_path.stem}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.strip())

        print(f"? OCR complete: {output_file}")

    except Exception as e:
        print(f"? Error processing {image_path.name}: {e}")

print("\n?? All pages processed. OCR outputs saved to:", OUTPUT_PATH)



