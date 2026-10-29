"""
SoilCare Recommendations Service
Generates sustainable soil health recommendations, organic conservation techniques,
and agronomic management advice without prescribing unverified arbitrary chemical doses.
"""

def generate_recommendations(analysis_result):
    """
    Produces actionable, sustainable, and tailored agricultural recommendations
    based on the multi-parameter soil analysis.
    """
    params = analysis_result.get('parameters', {})
    concerns = analysis_result.get('concerns', [])
    ratings = analysis_result.get('ratings', {})
    crop = analysis_result.get('target_crop', 'General Farming')
    soil_type = analysis_result.get('soil_type', '')

    recs = []

    # 1. Soil Reaction (pH) Management
    ph = params.get('ph')
    if ph is not None:
        if ph < 5.5:
            recs.append({
                'category': 'Acidity Correction & Liming',
                'priority': 'High',
                'icon': 'fa-solid fa-flask-vial',
                'title': 'Agricultural Lime Application & Phosphate Management',
                'action': (
                    'Acidic soils require buffering to restore nutrient availability. Apply agricultural limestone (calcium carbonate) '
                    'or dolomite as per buffer-pH test recommendations from your local Krishi Vigyan Kendra (KVK). Avoid applying unbuffered '
                    'water-soluble phosphatic fertilizers directly to acidic soil, as phosphate quickly fixes with free aluminum and iron.'
                ),
                'sustainable_tip': 'Incorporate well-decomposed Farmyard Manure (FYM) or biochar, which buffer soil against extreme pH drops and bind toxic aluminum.'
            })
        elif ph > 8.5:
            recs.append({
                'category': 'Alkalinity & Sodic Soil Reclamation',
                'priority': 'High',
                'icon': 'fa-solid fa-mountain-sun',
                'title': 'Gypsum Application & Leaching Management',
                'action': (
                    'High pH (>8.5) and sodium saturation cause soil slaking and crusting. Incorporate agricultural grade gypsum (calcium sulphate) '
                    'into the upper 10–15 cm of soil, followed by light irrigation and adequate drainage to leach displaced sodium ions away from roots. '
                    'Ensure the field has good sub-surface drainage outlets.'
                ),
                'sustainable_tip': 'Grow salt-tolerant green manure crops like Dhaincha (Sesbania aculeata) and incorporate into soil at 45 days. The root exudates release organic acids that neutralize alkaline carbonates.'
            })

    # 2. Salinity & Electrical Conductivity (EC)
    ec = params.get('ec')
    if ec is not None and ec >= 2.0:
        recs.append({
            'category': 'Salinity Mitigation',
            'priority': 'High',
            'icon': 'fa-solid fa-droplet-slash',
            'title': 'Soluble Salt Leaching & Drip Irrigation',
            'action': (
                'Elevated EC indicates salt accumulation near the root zone. Adopt pressurized drip irrigation with frequent, low-volume water pulses '
                'to maintain a constantly moist, low-salinity wetting bulb around the root zone. Avoid flood irrigation with saline groundwater.'
            ),
            'sustainable_tip': 'Apply straw or organic mulch across crop ridges to suppress capillary rise and surface evaporation of saline water.'
        })

    # 3. Organic Matter & Carbon Building (Universal Soil Health Pillar)
    oc = params.get('oc')
    if oc is not None and oc < 0.75:
        recs.append({
            'category': 'Organic Carbon & Soil Biology',
            'priority': 'High' if oc < 0.50 else 'Medium',
            'icon': 'fa-solid fa-seedling',
            'title': 'Green Manuring & Organic Enrichment',
            'action': (
                f'Soil organic carbon ({oc}%) is low. Rebuilding carbon is the single most effective way to increase moisture holding capacity and nutrient retention. '
                'Practice green manuring by sowing Sunn hemp (Crotalaria juncea) or Dhaincha prior to main season sowing, and ploughing it under at pre-flowering stage.'
            ),
            'sustainable_tip': 'Apply enriched compost, vermicompost, or well-rotted FYM. Avoid burning crop stubble; incorporate residues using a super seeder or rotavator.'
        })

    # 4. Nutrient Balancing (N-P-K)
    if 'nitrogen' in ratings and ratings['nitrogen']['rating'] == 'Low':
        recs.append({
            'category': 'Nitrogen Nutrition',
            'priority': 'Medium',
            'icon': 'fa-solid fa-leaf',
            'title': 'Split Nitrogen & Biofertilizer Inoculation',
            'action': (
                'Available Nitrogen is deficient. Instead of applying large single doses of chemical nitrogen (which leads to volatilization and leaching), '
                'split nitrogen applications into 3-4 stages synchronized with critical crop growth stages (tillering, flowering, grain development).'
            ),
            'sustainable_tip': 'Seed treatment with Azotobacter (for cereals) or Rhizobium (for pulses/legumes) at 200g per 10kg seed provides biological nitrogen fixation.'
        })

    if 'phosphorus' in ratings and ratings['phosphorus']['rating'] == 'Low':
        recs.append({
            'category': 'Phosphorus Nutrition',
            'priority': 'Medium',
            'icon': 'fa-solid fa-plant-wilt',
            'title': 'Phosphorus Solubilizing Bacteria (PSB) & Basal Placement',
            'action': (
                'Phosphorus is deficient. P has very low mobility in soil; place phosphatic fertilizers 5 cm below and 5 cm to the side of the seed during sowing. '
                'Inoculate soil or compost with Phosphorus Solubilizing Bacteria (PSB) or Vesicular Arbuscular Mycorrhiza (VAM) to release locked native phosphates.'
            ),
            'sustainable_tip': 'Combine rock phosphate with organic compost to naturally enhance its availability in acidic or near-neutral soils.'
        })

    if 'potassium' in ratings and ratings['potassium']['rating'] == 'Low':
        recs.append({
            'category': 'Potassium Nutrition',
            'priority': 'Medium',
            'icon': 'fa-solid fa-shield-halved',
            'title': 'Potash Nutrition & Stress Resistance',
            'action': (
                'Available Potassium is low. Potash strengthens cell walls, improves stomatal closure under drought, and increases grain boldness. '
                'Apply Muriate of Potash (MOP) or Sulfate of Potash (SOP) in split doses on sandy or light-textured soils.'
            ),
            'sustainable_tip': 'Mulching with farm crop residues and recycling wood ash supplies natural, slow-release potassium.'
        })

    # 5. Micronutrient Deficiencies
    micro_issues = []
    for micro in ['zinc', 'iron', 'copper', 'manganese', 'boron', 'sulphur']:
        if micro in ratings and ratings[micro]['rating'] == 'Deficient':
            micro_issues.append(micro.capitalize())

    if micro_issues:
        recs.append({
            'category': 'Micronutrient Management',
            'priority': 'Medium',
            'icon': 'fa-solid fa-microchip',
            'title': f"Deficiency Management for: {', '.join(micro_issues)}",
            'action': (
                f"Your soil report flags deficiency in {', '.join(micro_issues)}. "
                "For immediate crop relief, consider 0.5% foliar sprays (e.g. Zinc Sulphate 0.5% with 0.25% lime for zinc deficiency; Ferrous Sulphate 0.5% for iron chlorosis). "
                "For soil application, mix the recommended micronutrient with 100 kg farmyard manure and incubate for 10 days before broadcasting."
            ),
            'sustainable_tip': 'Chelated micronutrient formulations (like Zn-EDTA, Fe-EDDHA) are significantly more effective in alkaline soils (pH > 7.5).'
        })

    # 6. Soil Conservation & Erosion Control
    recs.append({
        'category': 'Soil Conservation & Erosion Prevention',
        'priority': 'General',
        'icon': 'fa-solid fa-water',
        'title': 'Contour Bunding, Cover Cropping & Mulching',
        'action': (
            'Protect fertile topsoil against monsoon water erosion and dry summer wind erosion. Establish contour bunds, vegetative vetiver grass barriers '
            'along slope contours, and maintain 30% soil surface cover with live cover crops (cowpea, horse gram) during fallow periods.'
        ),
        'sustainable_tip': 'Adhere to minimum tillage principles to protect soil pore networks and beneficial earthworm communities.'
    })

    # 7. Official Agricultural Expert Guidance
    recs.append({
        'category': 'Expert Agricultural Verification',
        'priority': 'Important',
        'icon': 'fa-solid fa-user-doctor',
        'title': 'Consult Local Krishi Vigyan Kendra (KVK)',
        'action': (
            f"Because micro-climatic factors, field slope, and groundwater quality vary by village, take your soil analysis card to your nearest "
            f"district Krishi Vigyan Kendra (KVK) or State Agricultural Department extension officer. They provide exact subsidized fertilizer blends "
            f"formulated specifically for {crop} and your local soil type."
        ),
        'sustainable_tip': 'Retest soil every 2–3 years at the same GPS farm location to monitor long-term fertility trends.'
    })

    return recs
