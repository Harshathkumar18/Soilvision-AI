"""
SoilCare Soil Report Parser
Extracts soil test parameters from uploaded digital PDFs and scanned images (JPG/PNG).
Features:
- pypdf for digital PDF text extraction
- pytesseract / Pillow for image OCR (with graceful fallback)
- Regex heuristics tailored for Indian Soil Health Cards (SHC)
- Confidence scoring and confirmation payload generator
"""

import re
import os
from pypdf import PdfReader
from PIL import Image

# Check pytesseract availability
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extracts raw text strings from digital PDF pages."""
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text

def extract_text_from_image(file_path):
    """Applies OCR on an image file if pytesseract is configured."""
    if not PYTESSERACT_AVAILABLE:
        return ""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"OCR image error (tesseract binary may not be in PATH): {e}")
        return ""

# Patterns for extracting soil health metrics
PATTERNS = {
    'ph': [
        r'(?:Soil\s*Reaction|pH|Reaction)\s*[:=-]?\s*([0-9]{1,2}(?:\.[0-9]{1,2})?)',
        r'\bpH\b\s*[:=-]?\s*([0-9]{1,2}(?:\.[0-9]{1,2})?)',
        r'pH\s+([0-9]\.[0-9]{1,2})'
    ],
    'ec': [
        r'(?:Electrical\s*Conductivity|EC)\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*(?:dS/m|mmhos/cm)?',
        r'\bEC\b\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)'
    ],
    'oc': [
        r'(?:Organic\s*Carbon|OC)\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*%?',
        r'\bOC\b\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*%'
    ],
    'nitrogen': [
        r'(?:Available\s*Nitrogen|Nitrogen|Avail\.\s*N|\bN\b)\s*[:=-]?\s*([0-9]{2,4}(?:\.[0-9]{1,2})?)\s*(?:kg/ha|kg\s*/\s*ha)?',
        r'\bNitrogen\b\s*[:=-]?\s*([0-9]{2,4}(?:\.[0-9]{1,2})?)'
    ],
    'phosphorus': [
        r'(?:Available\s*Phosphorus|Phosphorus|Avail\.\s*P|P2O5|\bP\b)\s*[:=-]?\s*([0-9]{1,3}(?:\.[0-9]{1,2})?)\s*(?:kg/ha|kg\s*/\s*ha)?',
        r'\bPhosphorus\b\s*[:=-]?\s*([0-9]{1,3}(?:\.[0-9]{1,2})?)'
    ],
    'potassium': [
        r'(?:Available\s*Potassium|Potassium|Avail\.\s*K|K2O|\bK\b)\s*[:=-]?\s*([0-9]{2,4}(?:\.[0-9]{1,2})?)\s*(?:kg/ha|kg\s*/\s*ha)?',
        r'\bPotassium\b\s*[:=-]?\s*([0-9]{2,4}(?:\.[0-9]{1,2})?)'
    ],
    'zinc': [
        r'(?:Available\s*Zinc|Zinc|\bZn\b)\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*(?:ppm|mg/kg)?'
    ],
    'iron': [
        r'(?:Available\s*Iron|Iron|\bFe\b)\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*(?:ppm|mg/kg)?'
    ],
    'copper': [
        r'(?:Available\s*Copper|Copper|\bCu\b)\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*(?:ppm|mg/kg)?'
    ],
    'manganese': [
        r'(?:Available\s*Manganese|Manganese|\bMn\b)\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*(?:ppm|mg/kg)?'
    ],
    'boron': [
        r'(?:Available\s*Boron|Boron|\bB\b)\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*(?:ppm|mg/kg)?'
    ],
    'sulphur': [
        r'(?:Available\s*Sulphur|Sulphur|Sulfur|\bS\b)\s*[:=-]?\s*([0-9]+(?:\.[0-9]{1,3})?)\s*(?:ppm|mg/kg)?'
    ]
}

# Metadata patterns
METADATA_PATTERNS = {
    'farmer_name': r'(?:Farmer\s*Name|Name\s*of\s*Farmer|Farmer)\s*[:=-]?\s*([A-Za-z\s\.]+)(?:\n|$|\t)',
    'district': r'(?:District|Dist\.?)\s*[:=-]?\s*([A-Za-z\s]+)(?:\n|$|,)',
    'state': r'(?:State)\s*[:=-]?\s*([A-Za-z\s]+)(?:\n|$|,)'
}

def parse_report_text(raw_text):
    """
    Parses raw extracted text from a soil health card,
    returning candidate values with confidence and unit notes.
    """
    extracted = {}
    confidence_flags = {}

    for param, patterns_list in PATTERNS.items():
        found = False
        for pat in patterns_list:
            match = re.search(pat, raw_text, re.IGNORECASE)
            if match:
                try:
                    val = float(match.group(1))
                    # Sanity check ranges
                    if param == 'ph' and (val < 2.0 or val > 12.0):
                        continue
                    if param == 'oc' and val > 15.0:
                        continue
                    extracted[param] = val
                    confidence_flags[param] = 'High'
                    found = True
                    break
                except ValueError:
                    pass
        if not found:
            extracted[param] = None
            confidence_flags[param] = 'Not Found'

    # Extract metadata if available
    metadata = {}
    for meta_key, pattern in METADATA_PATTERNS.items():
        m = re.search(pattern, raw_text, re.IGNORECASE)
        if m:
            val = m.group(1).strip()
            if len(val) > 1 and len(val) < 50:
                metadata[meta_key] = val

    return {
        'extracted': extracted,
        'confidence': confidence_flags,
        'metadata': metadata,
        'has_matches': any(v is not None for v in extracted.values()),
        'raw_snippet': raw_text[:800] if raw_text else ''
    }

def process_uploaded_report(file_path):
    """
    Main processor for uploaded soil reports.
    Extracts text, parses soil parameters, and prepares the editable confirmation form payload.
    """
    ext = file_path.rsplit('.', 1)[1].lower() if '.' in file_path else ''
    raw_text = ""

    if ext == 'pdf':
        raw_text = extract_text_from_pdf(file_path)
    elif ext in ['jpg', 'jpeg', 'png']:
        raw_text = extract_text_from_image(file_path)

    # If OCR didn't find text or returned minimal characters, check for sample fallback or flag
    parse_result = parse_report_text(raw_text)

    # Standard unit dictionary
    units = {
        'ph': 'pH Scale (0-14)',
        'ec': 'dS/m',
        'oc': '%',
        'nitrogen': 'kg/ha',
        'phosphorus': 'kg/ha',
        'potassium': 'kg/ha',
        'zinc': 'ppm',
        'iron': 'ppm',
        'copper': 'ppm',
        'manganese': 'ppm',
        'boron': 'ppm',
        'sulphur': 'ppm'
    }

    return {
        'extracted': parse_result['extracted'],
        'confidence': parse_result['confidence'],
        'metadata': parse_result['metadata'],
        'units': units,
        'has_matches': parse_result['has_matches'],
        'ocr_available': PYTESSERACT_AVAILABLE,
        'raw_text_length': len(raw_text)
    }
