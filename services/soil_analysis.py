"""
SoilCare Soil Analysis Service
Implements scientific soil parameter validation, rating benchmarks based on
Indian Council of Agricultural Research (ICAR) guidelines, and comprehensive health interpretation.
"""

# Benchmark thresholds as per ICAR / National Soil Health Card (SHC) scheme
THRESHOLDS = {
    'ph': {
        'ranges': [
            (0, 5.5, 'Strongly Acidic', 'warning', 'High risk of Aluminum/Manganese toxicity and Phosphorus fixation.'),
            (5.5, 6.5, 'Moderately Acidic', 'info', 'Acceptable for acid-tolerant crops, but optimal for most cereals when buffered.'),
            (6.5, 7.5, 'Neutral (Ideal)', 'success', 'Optimal nutrient availability and beneficial microbial activity.'),
            (7.5, 8.5, 'Moderately Alkaline', 'info', 'Micronutrients like Zinc and Iron may be fixed into unavailable forms.'),
            (8.5, 14.0, 'Strongly Alkaline / Sodic', 'danger', 'High exchangeable sodium percentage (ESP); risk of soil dispersion and poor aeration.')
        ]
    },
    'ec': {
        'ranges': [
            (0, 1.0, 'Normal (Safe)', 'success', 'Soluble salts are within safe limits for almost all crops.'),
            (1.0, 2.0, 'Slightly Saline', 'info', 'Sensitive crops (pulses, beans, citrus) may show slight germination or yield drop.'),
            (2.0, 4.0, 'Moderately Saline', 'warning', 'Yields of field crops may decline. Proper irrigation leaching is advised.'),
            (4.0, 50.0, 'Highly Saline', 'danger', 'Severe osmotic stress on crops. Only salt-tolerant crops can survive.')
        ]
    },
    'oc': {
        'ranges': [
            (0, 0.50, 'Low (Critical Deficit)', 'danger', 'Poor microbial life, low water retention, and fragile soil structure.'),
            (0.50, 0.75, 'Medium (Moderate)', 'info', 'Fair organic matter reserve; requires regular maintenance with compost/manure.'),
            (0.75, 10.0, 'High (Optimal)', 'success', 'Excellent biological activity, aggregate stability, and moisture capacity.')
        ]
    },
    'nitrogen': {
        'ranges': [
            (0, 280, 'Low', 'warning', 'Plants will exhibit stunted growth and pale yellowing of older leaves.'),
            (280, 560, 'Medium (Optimal)', 'success', 'Adequate vegetative growth and biomass formation.'),
            (560, 5000, 'High', 'info', 'Excess nitrogen risks vegetative overgrowth, pest susceptibility, and lodging.')
        ]
    },
    'phosphorus': {
        'ranges': [
            (0, 10, 'Low', 'warning', 'Poor root establishment, delayed maturity, and purplish leaf discoloration.'),
            (10, 25, 'Medium (Optimal)', 'success', 'Sufficient for strong rooting and energy transfer in plants.'),
            (25, 500, 'High', 'info', 'Abundant reserve; avoid excessive phosphate fertilization to prevent zinc antagonism.')
        ]
    },
    'potassium': {
        'ranges': [
            (0, 110, 'Low', 'warning', 'Weak stems, poor disease resistance, and leaf margin scorching (marginal chlorosis).'),
            (110, 280, 'Medium (Optimal)', 'success', 'Balanced stomatal regulation, disease tolerance, and grain filling.'),
            (280, 2000, 'High', 'info', 'High soil reserve; can reduce supplemental potash applications.')
        ]
    },
    'zinc': {
        'critical': 0.60,
        'unit': 'ppm',
        'low_text': 'Zinc Deficient (Khaira disease risk in paddy; interveinal chlorosis)',
        'ok_text': 'Sufficient Zinc'
    },
    'iron': {
        'critical': 4.50,
        'unit': 'ppm',
        'low_text': 'Iron Deficient (Iron chlorosis in young leaves, particularly in alkaline soils)',
        'ok_text': 'Sufficient Iron'
    },
    'copper': {
        'critical': 0.20,
        'unit': 'ppm',
        'low_text': 'Copper Deficient (Dieback symptoms and pollen sterility)',
        'ok_text': 'Sufficient Copper'
    },
    'manganese': {
        'critical': 2.00,
        'unit': 'ppm',
        'low_text': 'Manganese Deficient (Grey speck in cereals, reduced photosynthesis)',
        'ok_text': 'Sufficient Manganese'
    },
    'boron': {
        'critical': 0.50,
        'unit': 'ppm',
        'low_text': 'Boron Deficient (Poor fruit set, hollow heart, terminal bud death)',
        'ok_text': 'Sufficient Boron'
    },
    'sulphur': {
        'critical': 10.00,
        'unit': 'ppm',
        'low_text': 'Sulphur Deficient (Pale yellowing of younger leaves, reduced oil content in oilseeds)',
        'ok_text': 'Sufficient Sulphur'
    }
}

# Crop specific preferences and tolerances
CROPS_DATA = {
    'Paddy (Rice)': {
        'ideal_ph': (5.5, 7.5),
        'salinity_tolerance': 'Medium (up to 3.0 dS/m during vegetative)',
        'key_nutrients': ['Nitrogen', 'Phosphorus', 'Zinc', 'Silicon'],
        'special_notes': 'Submerged paddy soils naturally buffer pH towards neutrality. Zinc deficiency (Khaira disease) is very common in calcareous or prolonged waterlogged soils.'
    },
    'Wheat': {
        'ideal_ph': (6.0, 7.5),
        'salinity_tolerance': 'Medium to Moderate',
        'key_nutrients': ['Nitrogen', 'Phosphorus', 'Potassium', 'Manganese'],
        'special_notes': 'Sensitive to waterlogging and soil compaction. Prefers well-drained loams with balanced organic carbon.'
    },
    'Cotton': {
        'ideal_ph': (6.5, 8.5),
        'salinity_tolerance': 'High (tolerates moderate salinity)',
        'key_nutrients': ['Potassium', 'Nitrogen', 'Boron', 'Magnesium'],
        'special_notes': 'Requires deep rooting medium; susceptible to boll dropping if potassium or boron is deficient.'
    },
    'Maize (Corn)': {
        'ideal_ph': (5.8, 7.2),
        'salinity_tolerance': 'Moderate-low',
        'key_nutrients': ['Nitrogen', 'Zinc', 'Phosphorus'],
        'special_notes': 'Heavy nutrient feeder. Very responsive to organic compost and balanced NPK.'
    },
    'Pulses (Bengal Gram / Red Gram / Green Gram)': {
        'ideal_ph': (6.2, 7.8),
        'salinity_tolerance': 'Low (Very sensitive to salinity and waterlogging)',
        'key_nutrients': ['Phosphorus', 'Sulphur', 'Molybdenum', 'Rhizobium inoculation'],
        'special_notes': 'Legumes fix their own atmospheric nitrogen when Rhizobium nodules are active. They require good available phosphorus and sulphur for root nodules.'
    },
    'Groundnut (Peanut)': {
        'ideal_ph': (5.8, 7.0),
        'salinity_tolerance': 'Low to Medium',
        'key_nutrients': ['Calcium', 'Sulphur', 'Phosphorus', 'Boron'],
        'special_notes': 'Gypsum application at flowering provides essential calcium and sulphur for sound pod development and pop prevention.'
    },
    'Sugarcane': {
        'ideal_ph': (6.5, 7.8),
        'salinity_tolerance': 'Medium',
        'key_nutrients': ['Nitrogen', 'Potassium', 'Phosphorus', 'Iron'],
        'special_notes': 'Long-duration heavy feeder. Trash mulching helps conserve moisture and maintain organic carbon levels.'
    },
    'Vegetables & Chilli': {
        'ideal_ph': (6.0, 7.0),
        'salinity_tolerance': 'Low',
        'key_nutrients': ['Potassium', 'Calcium', 'Boron', 'Nitrogen'],
        'special_notes': 'Requires high organic matter and constant aeration to avoid root rot and blossom-end rot.'
    }
}

def clean_float(value):
    """Safely converts input string or number to a float, returning None if invalid or empty."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    str_val = str(value).strip().replace(',', '')
    if not str_val:
        return None
    try:
        return float(str_val)
    except ValueError:
        return None

def evaluate_parameter(param_name, val):
    """Evaluates a single parameter against ICAR thresholds."""
    if val is None:
        return None

    if param_name in ['ph', 'ec', 'oc', 'nitrogen', 'phosphorus', 'potassium']:
        cfg = THRESHOLDS.get(param_name)
        first = cfg['ranges'][0]
        if val < first[0]:
            return {'value': round(val, 2), 'rating': first[2], 'badge': first[3], 'explanation': first[4]}

        for min_v, max_v, label, badge, desc in cfg['ranges']:
            if min_v <= val < max_v or (val >= max_v and max_v == cfg['ranges'][-1][1]):
                return {
                    'value': round(val, 2),
                    'rating': label,
                    'badge': badge,
                    'explanation': desc
                }
        # Fallback if beyond limits
        last = cfg['ranges'][-1]
        return {'value': round(val, 2), 'rating': last[2], 'badge': last[3], 'explanation': last[4]}

    elif param_name in ['zinc', 'iron', 'copper', 'manganese', 'boron', 'sulphur']:
        cfg = THRESHOLDS.get(param_name)
        crit = cfg['critical']
        if val < crit:
            return {
                'value': round(val, 2),
                'rating': 'Deficient',
                'badge': 'warning',
                'explanation': f"{cfg['low_text']} (Current: {val} {cfg['unit']}, Critical benchmark: {crit} {cfg['unit']})."
            }
        else:
            return {
                'value': round(val, 2),
                'rating': 'Sufficient',
                'badge': 'success',
                'explanation': f"{cfg['ok_text']} (Current: {val} {cfg['unit']}, meets or exceeds critical level of {crit} {cfg['unit']})."
            }

    return None

def calculate_normalized_radar(parameters):
    """
    Normalizes soil parameters to a 0-100 scale for visual Chart.js radar:
    50 represents the ideal/optimal mid-range, <35 is deficient, >70 is high.
    """
    radar = {}

    # pH: optimal is 6.5 - 7.5 (around 7.0 -> 50)
    ph = parameters.get('ph')
    if ph is not None:
        if ph < 7.0:
            radar['pH Balance'] = max(10, min(90, (ph / 7.0) * 50))
        else:
            diff = ph - 7.0
            radar['pH Balance'] = max(10, min(90, 50 - (diff / 2.5) * 40))

    # EC: optimal is < 1.0 (50 to 90), severe at >4.0
    ec = parameters.get('ec')
    if ec is not None:
        if ec <= 1.0:
            radar['Salinity Safety'] = 85
        elif ec <= 2.0:
            radar['Salinity Safety'] = 60
        elif ec <= 4.0:
            radar['Salinity Safety'] = 35
        else:
            radar['Salinity Safety'] = 15

    # OC: optimal is > 0.75
    oc = parameters.get('oc')
    if oc is not None:
        radar['Organic Carbon'] = min(100, (oc / 0.75) * 60)

    # Nitrogen (ideal: 350-450)
    n = parameters.get('nitrogen')
    if n is not None:
        radar['Nitrogen (N)'] = min(100, (n / 400.0) * 55)

    # Phosphorus (ideal: 15-22)
    p = parameters.get('phosphorus')
    if p is not None:
        radar['Phosphorus (P)'] = min(100, (p / 20.0) * 55)

    # Potassium (ideal: 180-250)
    k = parameters.get('potassium')
    if k is not None:
        radar['Potassium (K)'] = min(100, (k / 220.0) * 55)

    return radar

def analyze_soil_health(raw_inputs):
    """
    Main soil analysis engine:
    - Cleans and validates inputs
    - Evaluates against ICAR benchmarks
    - Identifies multi-dimensional concerns (never relying on pH alone!)
    - Generates crop-specific observations
    - Flags missing measurements
    """
    # Clean numeric parameters
    params = {}
    for key in ['ph', 'ec', 'oc', 'nitrogen', 'phosphorus', 'potassium',
                'zinc', 'iron', 'copper', 'manganese', 'boron', 'sulphur',
                'moisture', 'temperature']:
        params[key] = clean_float(raw_inputs.get(key))

    # Evaluate each valid parameter
    ratings = {}
    for key, val in params.items():
        if val is not None:
            eval_res = evaluate_parameter(key, val)
            if eval_res:
                ratings[key] = eval_res

    # Moisture and Temperature custom evaluations
    if params.get('moisture') is not None:
        m = params['moisture']
        if m < 25:
            ratings['moisture'] = {'value': round(m, 1), 'rating': 'Deficient (<25%)', 'badge': 'warning', 'explanation': 'Soil moisture is critically low. Drought stress likely.'}
        elif m <= 65:
            ratings['moisture'] = {'value': round(m, 1), 'rating': 'Optimal (25-65%)', 'badge': 'success', 'explanation': 'Moisture is within ideal field capacity for root absorption.'}
        else:
            ratings['moisture'] = {'value': round(m, 1), 'rating': 'Excess (>65%)', 'badge': 'info', 'explanation': 'Soil is saturated. Ensure adequate surface drainage.'}

    if params.get('temperature') is not None:
        temp = params['temperature']
        if temp < 15:
            ratings['temperature'] = {'value': round(temp, 1), 'rating': 'Cool (<15°C)', 'badge': 'info', 'explanation': 'Low soil temperature can slow seed emergence and microbial mineralization.'}
        elif temp <= 32:
            ratings['temperature'] = {'value': round(temp, 1), 'rating': 'Optimal (15-32°C)', 'badge': 'success', 'explanation': 'Favorable root-zone temperature for plant enzymes and biology.'}
        else:
            ratings['temperature'] = {'value': round(temp, 1), 'rating': 'Elevated (>32°C)', 'badge': 'warning', 'explanation': 'High soil temperature accelerates moisture loss and organic matter oxidation.'}

    # Check for insufficient data
    evaluated_count = len(ratings)
    has_macronutrients = any(params.get(k) is not None for k in ['nitrogen', 'phosphorus', 'potassium'])
    has_ph_or_ec = params.get('ph') is not None or params.get('ec') is not None
    has_oc = params.get('oc') is not None

    concerns = []
    strengths = []
    testing_gaps = []

    # Identify Soil Health Concerns (Multi-factor)
    ph = params.get('ph')
    ec = params.get('ec')
    oc = params.get('oc')
    n = params.get('nitrogen')
    p = params.get('phosphorus')
    k = params.get('potassium')

    if ph is not None:
        if ph < 5.5:
            concerns.append({
                'title': 'Soil Acidity Risk',
                'severity': 'high',
                'description': f'Soil pH of {ph} is strongly acidic. Aluminum and iron toxicity can restrict root elongation and fix applied phosphate fertilizers into insoluble forms.'
            })
        elif ph > 8.5:
            concerns.append({
                'title': 'Soil Sodicity / High Alkalinity Risk',
                'severity': 'high',
                'description': f'Soil pH of {ph} indicates alkaline or sodic conditions. Soil particles disperse easily, leading to hard crusting, poor drainage, and severe micronutrient lockout.'
            })
        elif 6.5 <= ph <= 7.5:
            strengths.append(f'Soil reaction (pH {ph}) is near-neutral and ideal for maximum plant nutrient availability.')

    if ec is not None:
        if ec >= 2.0:
            concerns.append({
                'title': 'Salinity Hazard',
                'severity': 'high' if ec >= 4.0 else 'medium',
                'description': f'Electrical conductivity of {ec} dS/m indicates elevated soluble salt accumulation, causing osmotic water stress on crop roots.'
            })
        else:
            strengths.append(f'Electrical conductivity ({ec} dS/m) is within the safe range for crop growth.')

    if oc is not None:
        if oc < 0.50:
            concerns.append({
                'title': 'Organic Matter Depletion',
                'severity': 'high',
                'description': f'Organic Carbon is critically low ({oc}%). Tropical soils require regular carbon replenishment to sustain beneficial microbes and retain moisture.'
            })
        elif oc >= 0.75:
            strengths.append(f'Organic Carbon ({oc}%) is in the optimal range, ensuring healthy soil biology.')

    if n is not None and n < 280:
        concerns.append({
            'title': 'Nitrogen Deficiency',
            'severity': 'medium',
            'description': f'Available Nitrogen ({n} kg/ha) is low. Crop vegetative vigor and green leaf chlorophyll will be constrained.'
        })

    if p is not None and p < 10:
        concerns.append({
            'title': 'Phosphorus Deficiency',
            'severity': 'medium',
            'description': f'Available Phosphorus ({p} kg/ha) is low. Root development and early crop vigor may be hampered.'
        })

    if k is not None and k < 110:
        concerns.append({
            'title': 'Potassium Deficiency',
            'severity': 'medium',
            'description': f'Available Potassium ({k} kg/ha) is low. Crop resistance to lodging, heat, drought, and pests will be diminished.'
        })

    # Micronutrient deficiencies
    for micro in ['zinc', 'iron', 'copper', 'manganese', 'boron', 'sulphur']:
        val = params.get(micro)
        if val is not None and micro in THRESHOLDS:
            crit = THRESHOLDS[micro]['critical']
            if val < crit:
                concerns.append({
                    'title': f"{micro.capitalize()} Deficiency",
                    'severity': 'medium',
                    'description': f"Available {micro.capitalize()} ({val} ppm) is below the critical threshold ({crit} ppm)."
                })

    # Identify testing gaps
    if params.get('oc') is None:
        testing_gaps.append('Organic Carbon (OC %) test is missing. OC is vital to assess soil biological activity.')
    if not has_macronutrients:
        testing_gaps.append('Macronutrients (N, P, K) were not entered. These are essential for balancing crop nutrition.')
    if all(params.get(k) is None for k in ['zinc', 'iron', 'copper', 'manganese', 'boron', 'sulphur']):
        testing_gaps.append('Micronutrients (Zn, Fe, Cu, Mn, B, S) are unmeasured. Latent micronutrient hunger often limits crop yields.')

    # Target crop information
    target_crop = raw_inputs.get('target_crop', 'General Farming')
    crop_info = CROPS_DATA.get(target_crop, {
        'ideal_ph': (6.0, 7.5),
        'salinity_tolerance': 'Medium',
        'key_nutrients': ['Nitrogen', 'Phosphorus', 'Potassium'],
        'special_notes': 'Maintain balanced organic inputs and regular soil testing every two crop cycles.'
    })

    # Overall balanced readiness index (never just pH!)
    # A balanced multi-parameter index: 0-100
    score_sum = 0
    weights_sum = 0
    if ph is not None:
        weights_sum += 15
        if 6.2 <= ph <= 7.8:
            score_sum += 15
        elif 5.5 <= ph < 6.2 or 7.8 < ph <= 8.5:
            score_sum += 10
        else:
            score_sum += 4

    if ec is not None:
        weights_sum += 15
        if ec < 1.0:
            score_sum += 15
        elif ec < 2.0:
            score_sum += 10
        elif ec < 4.0:
            score_sum += 5
        else:
            score_sum += 2

    if oc is not None:
        weights_sum += 25
        if oc >= 0.75:
            score_sum += 25
        elif oc >= 0.50:
            score_sum += 16
        else:
            score_sum += 7

    for nut, w in [('nitrogen', 15), ('phosphorus', 15), ('potassium', 15)]:
        val = params.get(nut)
        if val is not None:
            weights_sum += w
            rating = ratings.get(nut, {}).get('rating', '')
            if 'Optimal' in rating or 'Medium' in rating:
                score_sum += w
            elif 'High' in rating:
                score_sum += (w * 0.85)
            else:
                score_sum += (w * 0.45)

    health_index = round((score_sum / weights_sum) * 100) if weights_sum > 0 else None

    # Radar data
    radar_data = calculate_normalized_radar(params)

    return {
        'parameters': params,
        'ratings': ratings,
        'evaluated_count': evaluated_count,
        'has_sufficient_data': evaluated_count >= 3 and has_ph_or_ec,
        'health_index': health_index,
        'concerns': concerns,
        'strengths': strengths,
        'testing_gaps': testing_gaps,
        'crop_info': crop_info,
        'target_crop': target_crop,
        'farmer_name': raw_inputs.get('farmer_name', 'Farmer'),
        'soil_type': raw_inputs.get('soil_type', 'Unspecified'),
        'location': {
            'state': raw_inputs.get('state', ''),
            'district': raw_inputs.get('district', '')
        },
        'radar_data': radar_data
    }
