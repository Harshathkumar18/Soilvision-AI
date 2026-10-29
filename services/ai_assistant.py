"""
SoilCare AI Assistant Service
Provides bilingual (English & Telugu) agricultural soil health guidance.
Features:
- Google Gemini API integration (via server-side REST requests using GEMINI_API_KEY)
- High-quality offline Agricultural Expert Heuristic Fallback when API key is unset or offline
- Grounded in ICAR sustainable farming practices
- Adheres to safety constraints: communicates uncertainty, avoids guaranteed yields, advises lab verification
"""

import os
import requests
import json

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '').strip()
# Use standard Google Generative Language API endpoint
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

SYSTEM_INSTRUCTION = """
You are 'SoilCare Assistant', an expert agricultural soil scientist and farmer-friendly advisor for Indian agriculture.
Your mission is to help farmers and students understand soil health, prevent erosion, interpret Soil Health Cards, and adopt sustainable soil conservation practices.

Rules you MUST ALWAYS follow:
1. Ground your advice in Indian Council of Agricultural Research (ICAR) principles and sustainable agronomy.
2. Clearly distinguish laboratory-verified parameters from estimates.
3. If soil measurements are incomplete (e.g., missing Organic Carbon or Micronutrients), ask the user for them or suggest testing.
4. Never promise guaranteed crop yield percentages, monetary profits, or absolute outcomes.
5. Emphasize organic carbon building, green manuring (Dhaincha, Sunn hemp), balanced NPK, biofertilizers, and local Krishi Vigyan Kendra (KVK) consultation.
6. Support both simple English and Telugu (or Telugu in English script). If the user writes in Telugu, reply warmly in helpful Telugu.
7. Always communicate uncertainty respectfully and remind farmers to verify exact chemical/amendment dosage with their local agricultural officer.
"""

# Agricultural Knowledge Base for Offline Fallback
KNOWLEDGE_RULES = [
    {
        'keywords': ['ph', 'acid', 'alkali', 'sodic', 'lime', 'gypsum', 'పీహెచ్', 'ఆమ్ల', 'క్షార'],
        'en': (
            "**Soil pH (Reaction) Explained:**\n\n"
            "- **Ideal Range:** 6.5 to 7.5. In this neutral window, nearly all essential plant nutrients remain soluble and available.\n"
            "- **Acidic Soil (pH < 5.5):** Increases toxic soluble aluminum. Fixes phosphorus into insoluble forms. "
            "Remedy: Apply agricultural lime (calcium carbonate) or dolomite as per buffer-pH test, and apply organic compost.\n"
            "- **Alkaline/Sodic Soil (pH > 8.5):** High sodium damages soil structure, creates surface crusting, and locks out Zinc and Iron. "
            "Remedy: Apply gypsum (calcium sulphate) with adequate leaching drainage, and incorporate Dhaincha green manure.\n\n"
            "*Recommendation:* Have your local KVK test the gypsum or lime requirement before application."
        ),
        'te': (
            "**నేల పీహెచ్ (pH - క్షార/ఆమ్ల స్వభావం):**\n\n"
            "- **ఆదర్శవంతమైన స్థాయి:** 6.5 నుండి 7.5. ఈ స్థాయిలో మొక్కలకు పోషకాలు అత్యంత సులభంగా అందుతాయి.\n"
            "- **ఆమ్ల నేలలు (pH < 5.5):** భాస్వరం లభ్యత తగ్గుతుంది. వ్యవసాయ సున్నం (Lime) మరియు పశువుల ఎరువు వాడాలి.\n"
            "- **క్షార/చౌడు నేలలు (pH > 8.5):** నేల గట్టిపడుతుంది. జిప్సం వేసి, నీరు నిలగట్టి బయటకు తీయాలి. జీలుగ (Dhaincha) వంటి పచ్చిరొట్ట ఎరువులను కలియదున్నాలి."
        )
    },
    {
        'keywords': ['organic carbon', 'oc', 'compost', 'humus', 'సేంద్రీయ', 'కర్బనం', 'కంపోస్ట్'],
        'en': (
            "**Soil Organic Carbon (OC) — The Heart of Soil Life:**\n\n"
            "- **Benchmark:** Under Indian tropical conditions, < 0.5% is critically low, 0.5% - 0.75% is medium, and > 0.75% is optimal.\n"
            "- **Why it matters:** Organic carbon feeds billions of beneficial soil microbes, builds crumb-like soil aggregates, and allows soil to hold up to 20 times its weight in water.\n"
            "- **How to increase OC:**\n"
            "  1. Incorporate green manures like Sunn hemp (జనుము) or Sesbania (జీలుగ) at 45 days.\n"
            "  2. Apply well-decomposed FYM (5-10 tonnes/ha) or vermicompost.\n"
            "  3. Stop burning crop stubble; incorporate crop residue into the soil."
        ),
        'te': (
            "**సేంద్రీయ కర్బనం (Organic Carbon):**\n\n"
            "- సేంద్రీయ కర్బనం నేల ప్రాణం వంటిది. ఇది 0.75% కంటే ఎక్కువ ఉంటే నేల సారవంతమైనదిగా భావిస్తారు.\n"
            "- దీనిని పెంచడానికి జీలుగ, జనుము పచ్చిరొట్ట పైర్లను పూత దశలో నేలలో కలియదున్నాలి.\n"
            "- పంట వ్యర్థాలను కాల్చకుండా భూమిలోనే కలపడం ద్వారా తేమ నిల్వ సామర్థ్యం పెరుగుతుంది."
        )
    },
    {
        'keywords': ['erosion', 'wind', 'rain', 'runoff', 'కొట్టుకుపోవడం', 'కోత'],
        'en': (
            "**Soil Erosion Prevention Techniques:**\n\n"
            "1. **Contour Bunding:** Build earthen bunds across slope contours to slow down torrential monsoon runoff.\n"
            "2. **Cover Crops:** Never leave the soil bare under scorching summer sun or heavy rain. Grow pulses like cowpea or horse gram.\n"
            "3. **Vegetative Barriers:** Plant deep-rooted Vetiver grass (ఖస్ ఖస్) along field boundaries.\n"
            "4. **Mulching:** Protect topsoil with crop residues to absorb raindrop impact and prevent splash erosion."
        ),
        'te': (
            "**నేల కోత నివారణ చర్యలు:**\n\n"
            "1. పొలంలో వాలుకు అడ్డంగా గట్లు (Contour Bunds) వేయడం ద్వారా వర్షపు నీటి వేగాన్ని తగ్గించవచ్చు.\n"
            "2. నేలను బీడుగా ఉంచకుండా అలసందలు, ఉలవలు వంటి కవర్ పంటలను సాగు చేయాలి.\n"
            "3. గట్ల వెంట వెటివర్ (వట్టివేరు) గడ్డిని నాటడం ద్వారా మట్టి కొట్టుకుపోకుండా కాపాడవచ్చు."
        )
    },
    {
        'keywords': ['salinity', 'salt', 'ec', 'electrical conductivity', 'ఉప్పు', 'లవణీయత'],
        'en': (
            "**Managing Soil Salinity (Electrical Conductivity - EC):**\n\n"
            "- **EC < 1.0 dS/m:** Normal and safe for all crops.\n"
            "- **EC 2.0 - 4.0 dS/m:** Moderate salinity, affecting sensitive pulses and vegetables.\n"
            "- **Management:** Improve surface and subsurface drainage so salts can be leached below root zones. "
            "Use drip irrigation to maintain a steady freshwater wetting front. Switch to moderately salt-tolerant crops like cotton, barley, or mustard if salinity persists."
        ),
        'te': (
            "**నేల లవణీయత (EC):**\n\n"
            "- EC 1.0 కంటే తక్కువగా ఉంటే నేల సురక్షితమైనది.\n"
            "- లవణాలు ఎక్కువగా ఉన్నప్పుడు డ్రిప్ ఇరిగేషన్ ద్వారా తక్కువ నీటితో తేమను నిరంతరం కాపాడాలి.\n"
            "- పొలంలో మురుగునీటి కాలువలు ఏర్పాటు చేసి అదనపు లవణాలను బయటకు పంపాలి."
        )
    },
    {
        'keywords': ['zinc', 'iron', 'micronutrient', 'జింక్', 'ఇనుము', 'సూక్ష్మ'],
        'en': (
            "**Micronutrient Management (Zinc, Iron, Boron, Sulphur):**\n\n"
            "- **Zinc:** Critical in paddy soils (Khaira disease). Apply 25 kg Zinc Sulphate per hectare to soil or spray 0.5% ZnSO4 with 0.25% lime.\n"
            "- **Iron:** Interveinal chlorosis in young leaves is common in alkaline soils. Spray 0.5% Ferrous Sulphate.\n"
            "- **Tip:** Micronutrients applied along with organic compost are significantly more bio-available to crop roots."
        ),
        'te': (
            "**సూక్ష్మ పోషకాల యాజమాన్యం:**\n\n"
            "- **జింక్ లోపం:** వరిలో ఖైరా తెగులు (ఆకులపై తుప్పు మచ్చలు) కనిపిస్తుంది. ఎకరాకు 10-12 కిలోల జింక్ సల్ఫేట్ వేయాలి లేదా పిచికారీ చేయాలి.\n"
            "- **ఇనుము లోపం:** లేత ఆకులు పాలిపోవడం జరుగుతుంది. 0.5% ఫెర్రస్ సల్ఫేట్ పిచికారీ చేయడం వల్ల త్వరగా నివారించవచ్చు."
        )
    }
]

def query_gemini_api(prompt, language='en'):
    """Sends prompt to Google Gemini REST endpoint if API key is present."""
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not api_key:
        return None

    headers = {'Content-Type': 'application/json'}
    url = f"{GEMINI_ENDPOINT}?key={api_key}"

    lang_note = "Please reply in Telugu language." if language == 'te' else "Please reply in clear, simple English."

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{SYSTEM_INSTRUCTION}\n\nLanguage Preference: {lang_note}\n\nFarmer's Query:\n{prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 800
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        if response.status_code == 200:
            res_data = response.json()
            candidates = res_data.get('candidates', [])
            if candidates:
                text_part = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if text_part:
                    return text_part
    except Exception as e:
        print(f"Gemini API request failed: {e}")

    return None

def fallback_expert_response(prompt, language='en'):
    """High-quality offline agricultural expert system response."""
    lower_p = prompt.lower()

    # Search knowledge rules
    matched_rule = None
    for rule in KNOWLEDGE_RULES:
        if any(kw in lower_p for kw in rule['keywords']):
            matched_rule = rule
            break

    if matched_rule:
        text = matched_rule.get('te' if language == 'te' else 'en', matched_rule['en'])
        footer = "\n\n*(Notice: Generated by SoilCare Agricultural Expert Engine. For farm-specific fertilizer schedules, consult your local KVK.)*"
        return text + footer

    # General fallback
    if language == 'te':
        return (
            "**సాయిల్‌కేర్ మార్గదర్శి:**\n\n"
            "నేల ఆరోగ్యాన్ని కాపాడటానికి మూడు ముఖ్యమైన సూత్రాలు:\n"
            "1. **సేంద్రీయ పదార్థాన్ని పెంచడం:** ఆవు పేడ, వర్మీ కంపోస్ట్ లేదా పచ్చిరొట్ట ఎరువులను క్రమం తప్పకుండా వాడండి.\n"
            "2. **నేల పరీక్ష:** ప్రతి 2-3 సంవత్సరాలకు ఒకసారి మట్టి నమూనా తీసి పరీక్షించండి.\n"
            "3. **నేల కోత నివారణ:** పంట మార్పిడి పద్ధతులను పాటించండి.\n\n"
            "దయచేసి మీ నిర్దిష్ట ప్రశ్న లేదా నేల పరీక్ష పారామితులను (pH, EC, నత్రజని మొదలైనవి) తెలియజేయండి."
        )
    else:
        return (
            "**SoilCare Agricultural Guide:**\n\n"
            "To safeguard soil vitality, adhere to the three foundational pillars of sustainable soil management:\n"
            "1. **Build Organic Matter:** Regularly integrate compost, vermicompost, and leguminous green manure (Sesbania/Sunn hemp).\n"
            "2. **Balance Nutrients:** Avoid excessive single-fertilizer reliance. Supplement with biofertilizers (Azotobacter, PSB, Rhizobium).\n"
            "3. **Erosion Defense:** Keep fields covered with mulch or cover crops during monsoon rains and summer dry spells.\n\n"
            "You can enter your exact soil parameters (such as pH, EC, Organic Carbon, NPK) into our **Soil Analyzer** for a complete report!"
        )

def get_ai_response(prompt, language='en'):
    """
    Main AI routing entry point.
    Attempts Gemini API first; seamlessly falls back to local expert system.
    """
    if not prompt or not prompt.strip():
        return "Please ask a question about soil health, soil testing, or conservation techniques."

    # Try Gemini API if key is available
    gemini_reply = query_gemini_api(prompt, language)
    if gemini_reply:
        return gemini_reply

    # Seamless fallback
    return fallback_expert_response(prompt, language)
