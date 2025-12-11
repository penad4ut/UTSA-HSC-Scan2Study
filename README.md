# UTSA-HSC-Scan2Study  
Multimodal OCR–LLM Pipeline for Extracting Structured Facts from Scanned Clinical Documents

## Overview
UTSA-HSC-Scan2Study is a multimodal extraction pipeline that combines optical character recognition (OCR), layout-aware text processing, and large language model (LLM) inference to convert scanned or image-based clinical documents into structured, research-ready data. The system supports oncology-focused workflows such as extracting tumor descriptors, staging information, treatments, and other key clinical facts from legacy PDFs, faxed documents, and external medical records.

Foundational OCR and extraction methods that informed this work were developed within the CTSA and P30 Cancer Center environments at UT San Antonio Health Science Center (UTSA-HSC), where they supported Chromosome 18 research activities. This repository contains a re-engineered and significantly expanded version of that early work, adapted by Dr. Mahanaz Syed to create a generalizable, AI-enabled platform for oncology studies, clinical trial operations, and other research domains requiring structured data from scanned clinical documents.

## Key Features
- **Layout-aware OCR processing** for multi-column and irregular clinical document structures  
- **LLM-driven fact extraction** for oncology-relevant variables (tumor descriptors, staging, treatments, etc.)  
- **Full pipeline orchestration** for multi-page and batch document processing  
- **Configurable prompts, guardrails, and model parameters**  
- **FHIR®-ready JSON outputs** enabling integration with FETCH or downstream data systems  
- **Human-in-the-loop review support through the TRACER Dashboard**  
- **Supports both text-based and image-based PDFs** and image formats (TIFF, PNG, JPEG)  
- **Validated extraction performance** using curated gold-standard subsets  

## The TRACER Dashboard (Transparent AI Clinical Extraction and Reasoning)
Scan2Study integrates with the **TRACER Dashboard**, a transparent human-in-the-loop interface designed to:

- Display OCR and LLM-extracted facts alongside their source text  
- Allow reviewers to accept, edit, or reject extracted fields  
- Provide visual traceability from structured outputs back to original document content  
- Generate correction logs that can be used to update prompts, refine extraction rules, or guide model retraining  
- Support quality assurance for trial abstraction and registry workflows  

TRACER ensures that extracted information is **auditable, correctable, and fully traceable**, reinforcing trustworthiness and enabling continuous system improvement.
