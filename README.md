# 🌱 SoilCare — AI-Powered Soil Protection Website

> **"Protect Our Soil, Protect Our Future"**  
> A modern, responsive, farmer-friendly web platform built for Indian farmers, agronomists, and students to evaluate soil health, diagnose degradation problems, explore regional agro-ecological zones, practice sustainable conservation, and interpret laboratory Soil Health Cards with AI assistance.

---

## 🌟 Key Features

1. **Environmental Design System**
   - Professional palette: Forest green, light sage green, crisp cream/white, and warm earthy soil brown.
   - Fully responsive on mobile phones, tablets, laptops, and desktops.
   - Large, accessible touch-friendly buttons and inputs designed for field usage.
   - **Bilingual Interface**: One-click language switcher between **English** and **తెలుగు (Telugu)**.

2. **Soil Health Analyzer (`/analyzer`)**
   - Farmers enter parameters: pH, Electrical Conductivity (EC), Organic Carbon (OC %), Available Nitrogen (N), Phosphorus (P), Potassium (K), and Micronutrients (Zn, Fe, Cu, Mn, B, S).
   - Multi-parameter evaluation against **Indian Council of Agricultural Research (ICAR)** and National Soil Health Card (SHC) benchmarks.
   - **Parameter Balance Radar Chart**: Powered by Chart.js.
   - **Multi-Factor Soil Vitality Index**: Never relies on pH alone!
   - Crop-specific guidance for Paddy (Rice), Wheat, Cotton, Maize, Pulses, Groundnut, Sugarcane, and Vegetables.
   - Instant sample loaders for testing (*Balanced Loam*, *Sodic/Alkaline Soil*, *Acidic Soil*).

3. **Soil Health Card Report Upload & OCR (`/upload`)**
   - Supports **PDF**, **JPG**, and **PNG** uploads up to 10 MB.
   - Automatic text and parameter extraction using `pypdf` and `pytesseract` / regular-expression pattern matcher.
   - **Two-Step Verification**: Extracted values are presented in an editable confirmation table before analysis. The system analyzes *only confirmed values* and never guesses ambiguous numbers.
   - Downloadable & printable official Soil Health Card format.

4. **Soil Problems & Solutions Directory (`/problems`)**
   - Covers 9 major degradation hazards:
     1. Soil Erosion (Water & Wind)
     2. Soil Salinity and Sodicity
     3. Acidic and Alkaline Soils
     4. Nutrient Deficiencies & Latent Hunger
     5. Loss of Soil Organic Matter (SOC)
     6. Soil Compaction & Hardpan Formation
     7. Waterlogging & Poor Drainage
     8. Soil Contamination & Chemical Residues
     9. Drought-Related Soil Degradation
   - Categorized under *Physical*, *Chemical*, *Biological*, *Nutritional*, and *Climatic* with real-time keyword search.

5. **Interactive Soil Map of India (`/map`)**
   - Built with **Leaflet.js** and **OpenStreetMap**.
   - Verified Indian Agro-Ecological Zones (Alluvial, Black/Regur, Red & Yellow, Laterite, Arid/Desert, Mountain, and Coastal Saline/Sodic).
   - Interactive district & state search, layer legend, degradation risk warnings, and conservation recommendations.

6. **Learning Zone & Quiz (`/quiz`)**
   - Multiple-choice quizzes with **Beginner** and **Advanced** agronomy difficulty levels.
   - Live progress indicator, instant scoring, correct answer feedback, and scientific explanations.
   - SQLite leaderboard recording top performers.
   - Hands-on field activities: *The Jar Texture Test*, *The 100-Day Humus Compost Recipe*, and *The Earthworm Census*.

7. **AI Soil Assistant (Global Chatbot Widget)**
   - Accessible via the floating robot button on every page.
   - Server-side integration with **Google Gemini API** (`gemini-2.5-flash`).
   - **Intelligent Offline Heuristic Fallback**: Continues working seamlessly with an ICAR agricultural expert engine even when no API key is provided or the device is offline!
   - Communicates uncertainty, advises local KVK testing, and avoids unsupported crop-yield predictions.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+ with [Flask 3.x](https://flask.palletsprojects.com/)
- **Database**: SQLite (Zero configuration, persistent file `soilcare.db`)
- **Frontend**: HTML5, Vanilla CSS3 (Design tokens, glassmorphism, responsive grid), Vanilla JavaScript ES6
- **Mapping**: [Leaflet.js](https://leafletjs.com/) with OpenStreetMap tiles
- **Charts**: [Chart.js 4.x](https://www.chartjs.org/)
- **Document Processing**: `pypdf`, `Pillow`, `pytesseract`
- **AI Integration**: Google Generative AI (Gemini) REST API with offline fallback

---

## 📁 Project Architecture

```
soil protection/
├── app.py                      # Main Flask server with REST routes & template views
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
├── .env                        # Local active environment variables
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLite schema, tables, and CRUD helpers
├── services/
│   ├── __init__.py
│   ├── soil_analysis.py        # ICAR scientific benchmark evaluation rules
│   ├── recommendations.py      # Crop-specific & sustainable conservation advice
│   ├── report_parser.py        # PDF & image OCR regex extraction for Soil Cards
│   ├── ai_assistant.py         # Gemini API + Offline agricultural expert system
│   ├── translations.py         # English and Telugu localization dictionary
│   └── knowledge_data.py       # 9 Soil problems, quizzes, map zones, activities
├── templates/
│   ├── base.html               # Master layout (navbar, Telugu switch, AI drawer, footer)
│   ├── index.html              # Landing page (hero, stats, feature cards, CTA)
│   ├── problems.html           # 9 soil degradation problems with search & filters
│   ├── analyzer.html           # Interactive soil test form, Chart.js radar, results
│   ├── upload.html             # Document upload & editable confirmation workflow
│   ├── map.html                # Leaflet interactive map of Indian soil zones
│   ├── quiz.html               # Educational quizzes, scoring, field activities
│   ├── report.html             # Printable official Soil Health Card #SC-xxxxx
│   ├── about.html              # Mission, KVK directory, disclaimers, contact form
│   └── 404.html                # Custom farmer-friendly 404 error page
├── static/
│   ├── css/
│   │   └── style.css           # Comprehensive theme stylesheet & print media queries
│   ├── js/
│   │   ├── main.js             # Mobile navbar, language switcher, AI drawer, toasts
│   │   ├── analyzer.js         # Analyzer form, Chart.js radar, demo loaders
│   │   ├── upload.js           # Drag-and-drop, simulated OCR, confirmation flow
│   │   ├── map.js              # Leaflet zones, markers, search, details drawer
│   │   └── quiz.js             # Quiz engine, difficulty toggle, scoring, badge
│   └── samples/
│       ├── sample_soil_health_card.txt # Demonstration sample report text
│       └── sample_soil_health_card.pdf # Demonstration sample PDF for upload testing
├── tests/
│   ├── test_analysis.py        # Unit tests for ICAR benchmarks & index
│   ├── test_routes.py          # Unit tests for all Flask routes & APIs
│   ├── test_parser.py          # Unit tests for report parsing and regex
│   └── verify_live_server.py   # Live server HTTP smoke tester
└── README.md                   # Complete documentation
```

---

## 🚀 Quickstart Installation Guide (Windows & VS Code)

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 installed.
- Verify in your terminal:
  ```powershell
  python --version
  ```

### Step 1: Open Terminal in VS Code
Open VS Code in the project folder `c:\Users\Harsha\OneDrive\Desktop\soil protection`.  
Open a terminal in VS Code (`Ctrl + ~`).

### Step 2: Create a Virtual Environment
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
On Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```
*(If script execution is restricted on Windows, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Inside `.env`, you can optionally add your Google Gemini API key:
```ini
FLASK_SECRET_KEY=soilcare-super-secret-key-2026
FLASK_ENV=development
PORT=5000
GEMINI_API_KEY=your_gemini_api_key_here
```
> **Note**: If `GEMINI_API_KEY` is left blank, the website **still works 100% offline** using the built-in Agricultural Expert Engine!

### Step 6: Run the Application
```powershell
python app.py
```

### Step 7: Access the Website
Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🧪 Testing Instructions

Run the automated test suite covering all 21 unit tests:
```powershell
.\venv\Scripts\python -m unittest discover tests
```

You should see:
```
----------------------------------------------------------------------
Ran 21 tests in 0.25s

OK
```

To run the live HTTP endpoint smoke test while the server is running:
```powershell
.\venv\Scripts\python tests/verify_live_server.py
```

---

## 🌾 Sample Test Data for Demonstration

You can test the **Soil Analyzer** immediately using the sample buttons on `/analyzer`:
- **Balanced Loam Sample**:
  - pH: 6.8 | EC: 0.65 dS/m | OC: 0.82% | N: 380 kg/ha | P: 22.5 kg/ha | K: 240 kg/ha
- **Sodic / Alkaline Sample**:
  - pH: 8.9 | EC: 2.8 dS/m | OC: 0.38% | N: 210 kg/ha | P: 8.5 kg/ha | K: 195 kg/ha
- **Acidic Laterite Sample**:
  - pH: 4.8 | EC: 0.40 dS/m | OC: 0.55% | N: 240 kg/ha | P: 6.2 kg/ha | K: 95 kg/ha

To test the **Report Upload** workflow (`/upload`):
- Click **"Simulate Complete Report OCR"** to inspect the editable verification table.
- Or upload the bundled demonstration PDF located at:
  `static/samples/sample_soil_health_card.pdf`.

---

## 🌐 Deployment Instructions

### Production with Gunicorn / Waitress (Windows)
For production deployments on Windows:
```powershell
pip install waitress
waitress-serve --port=5000 app:app
```

### Production with Linux / Docker
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📜 Scientific Methodology & Disclaimers

1. **ICAR Grounded Rules**: Soil reaction and nutrient categories adhere to Indian Council of Agricultural Research (ICAR) guidelines.
2. **Balanced Health Assessment**: As per agronomic standards, overall soil health is never evaluated on pH alone.
3. **No Arbitrary Dosing**: SoilCare does not prescribe unverified arbitrary metric quantities of commercial fertilizers. Farmers are advised to consult their district Krishi Vigyan Kendra (KVK) for farm-specific fertilizer schedules.
4. **Geospatial Limitations**: Regional agro-ecological maps show zonal tendencies and cannot substitute core soil testing from an individual farm.
