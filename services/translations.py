"""
SoilCare Translations Module
Provides dual-language support for English (en) and Telugu (te).
Covers navigation, dashboard headers, parameter names, ratings, and common agricultural guidance.
"""

TRANSLATIONS = {
    'en': {
        'brand': 'SoilCare',
        'tagline': 'AI-Powered Soil Health & Sustainable Farming',
        'nav_home': 'Home',
        'nav_problems': 'Soil Problems',
        'nav_analyzer': 'Soil Analyzer',
        'nav_upload': 'Upload Report',
        'nav_map': 'Soil Map',
        'nav_quiz': 'Learning Zone',
        'nav_about': 'About',
        'hero_title': 'Protect Our Soil, Protect Our Future',
        'hero_subtitle': 'Empowering Indian farmers with scientific soil-test analysis, sustainable conservation techniques, erosion defense, and tailored agricultural guidance.',
        'btn_analyze': 'Analyze My Soil',
        'btn_solutions': 'Explore Soil Solutions',
        'btn_upload': 'Upload Soil Test Card',
        'btn_ask_ai': 'Ask AI Assistant',
        'param_ph': 'Soil pH (Reaction)',
        'param_ec': 'Electrical Conductivity (EC, dS/m)',
        'param_oc': 'Organic Carbon (OC, %)',
        'param_n': 'Available Nitrogen (N, kg/ha)',
        'param_p': 'Available Phosphorus (P, kg/ha)',
        'param_k': 'Available Potassium (K, kg/ha)',
        'param_zn': 'Zinc (Zn, ppm)',
        'param_fe': 'Iron (Fe, ppm)',
        'param_cu': 'Copper (Cu, ppm)',
        'param_mn': 'Manganese (Mn, ppm)',
        'param_b': 'Boron (B, ppm)',
        'param_s': 'Sulphur (S, ppm)',
        'status_low': 'Deficient / Low',
        'status_medium': 'Optimal / Medium',
        'status_high': 'High / Abundant',
        'status_critical': 'Critical Alert',
        'footer_desc': 'SoilCare is an open educational and diagnostic initiative aligned with sustainable agricultural science and ICAR benchmarks.',
        'footer_disclaimer': 'Notice: Regional maps and online screening cannot replace certified individual farm soil testing. Always consult local KVK or agricultural officers for precise amendment rates.',
        'lang_switch': 'తెలుగు (Telugu)'
    },
    'te': {
        'brand': 'సాయిల్‌కేర్ (SoilCare)',
        'tagline': 'నేల ఆరోగ్యం & స్థిరమైన వ్యవసాయ వేదిక',
        'nav_home': 'హోమ్',
        'nav_problems': 'నేల సమస్యలు',
        'nav_analyzer': 'నేల విశ్లేషణ',
        'nav_upload': 'రిపోర్ట్ అప్‌లోడ్',
        'nav_map': 'నేల మ్యాప్',
        'nav_quiz': 'నేర్చుకునే విభాగం',
        'nav_about': 'మా గురించి',
        'hero_title': 'మన నేలను కాపాడుకుందాం, మన భవిష్యత్తును రక్షించుకుందాం',
        'hero_subtitle': 'శాస్త్రీయ నేల పరీక్ష విశ్లేషణ, సమతుల్య పోషకాలు, మరియు మెరుగైన దిగుబడి కోసం రైతులకు తోడ్పడే డిజిటల్ మార్గదర్శి.',
        'btn_analyze': 'నా నేలను విశ్లేషించండి',
        'btn_solutions': 'సమస్యల పరిష్కారాలు',
        'btn_upload': 'నేల ఆరోగ్య కార్డు అప్‌లోడ్',
        'btn_ask_ai': 'AI సహాయకుడిని అడగండి',
        'param_ph': 'నేల పీహెచ్ (pH - క్షార/ఆమ్ల స్వభావం)',
        'param_ec': 'విద్యుత్ వాహకత (EC - లవణీయత, dS/m)',
        'param_oc': 'సేంద్రీయ కర్బనం (OC, %)',
        'param_n': 'లభ్య నత్రజని (Nitrogen, kg/ha)',
        'param_p': 'లభ్య భాస్వరం (Phosphorus, kg/ha)',
        'param_k': 'లభ్య పొటాషియం (Potassium, kg/ha)',
        'param_zn': 'జింక్ (Zn, ppm)',
        'param_fe': 'ఇనుము (Fe, ppm)',
        'param_cu': 'రాగి (Cu, ppm)',
        'param_mn': 'మాంగనీస్ (Mn, ppm)',
        'param_b': 'బోరాన్ (B, ppm)',
        'param_s': 'సల్ఫర్ (S, ppm)',
        'status_low': 'లోపం / తక్కువ',
        'status_medium': 'సరిపడా / మధ్యస్థం',
        'status_high': 'అధికం',
        'status_critical': 'తీవ్రమైన హెచ్చరిక',
        'footer_desc': 'సాయిల్‌కేర్ అనేది స్థిరమైన వ్యవసాయం మరియు ICAR ప్రమాణాలకు అనుగుణంగా రూపొందించబడిన విద్యా మరియు విశ్లేషణ వేదిక.',
        'footer_disclaimer': 'గమనిక: ఆన్‌లైన్ విశ్లేషణ అధికారిక ల్యాబ్ పరీక్షకు ప్రత్యామ్నాయం కాదు. ఎరువుల మోతాదుల కోసం స్థానిక కృషి విజ్ఞాన కేంద్రం (KVK) అధికారులను సంప్రదించండి.',
        'lang_switch': 'English'
    }
}

def get_text(lang='en', key='brand'):
    """Returns translated string for a given key."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    return lang_dict.get(key, TRANSLATIONS['en'].get(key, key))
