import streamlit as st
import os
import json
from pathlib import Path
from PyPDF2 import PdfReader
from PIL import Image
import fitz  # PyMuPDF

# -----------------------------
# CONFIGURATION
# -----------------------------
ROOT_DIR = Path(__file__).resolve().parent
DATA_ORIGINAL = ROOT_DIR / "data_original" # original source image file
DATA_VLLM_OCR = ROOT_DIR / "data_vLLM_OCR" # output from ocr
DATA_LLM = ROOT_DIR / "data_LLM" # llm output from studyfact module
LOGS_DIR = ROOT_DIR / "logs"

st.set_page_config(page_title="TRACER Dashboard", layout="wide")

st.title("TRACER Dashboard")
st.caption("Transparent AI Clinical Extraction and Reasoning")

# -----------------------------
# DOCUMENT SELECTION
# -----------------------------
docs = sorted([f.stem for f in DATA_ORIGINAL.glob("*.pdf")])
if not docs:
    st.error("No PDF files found in data_original/")
    st.stop()

doc_id = st.selectbox("Select a document", docs)
ocr_subdir = DATA_VLLM_OCR / doc_id
llm_subdir = DATA_LLM / doc_id

if not ocr_subdir.exists():
    st.warning(f"No OCR output found for {doc_id}")
    st.stop()

pages = sorted([f.stem for f in ocr_subdir.glob("*.txt")])
if not pages:
    st.warning(f"No page-level OCR text files found for {doc_id}")
    st.stop()

page = st.selectbox("Select a page", pages)

ocr_path = ocr_subdir / f"{page}.txt"
json_path = llm_subdir / f"{page}.json"
pdf_path = DATA_ORIGINAL / f"{doc_id}.pdf"

# -----------------------------
# PAGE DISPLAY LAYOUT
# -----------------------------
col1, col2, col3 = st.columns([1.3, 1, 1])

# ----- Original Page -----
with col1:
    st.subheader("📄 Original Page")
    try:
        page_num = int(page.split("_")[-1]) - 1
        pdf_doc = fitz.open(pdf_path)
        pix = pdf_doc[page_num].get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        st.image(img, use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying PDF page: {e}")

# ----- OCR Output -----
with col2:
    st.subheader("📝 OCR Output")
    if ocr_path.exists():
        with open(ocr_path, "r", encoding="utf-8") as f:
            text = f.read()
        st.text_area("OCR Text", text, height=600)
    else:
        st.warning("OCR text not found.")

# ----- LLM Extracted JSON -----
with col3:
    st.subheader("💡 Extracted Clinical Facts")
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        st.json(data, expanded=True)
    else:
        st.warning("No JSON facts file found for this page.")

# -----------------------------
# METADATA SECTION
# -----------------------------
st.markdown("---")
st.markdown("### 📊 Metadata & Traceability")

meta_col1, meta_col2, meta_col3 = st.columns(3)
with meta_col1:
    st.write(f"**Document:** {doc_id}.pdf")
with meta_col2:
    st.write(f"**Current Page:** {page}")
with meta_col3:
    st.write(f"**Folders:** OCR → `{ocr_subdir.name}`, LLM → `{llm_subdir.name}`")

st.info("💾 All data loaded locally — no external API calls or internet required.")
