"""
SoilCare Knowledge Data Module
Provides comprehensive datasets for:
- 9 Major Soil Degradation Problems & Scientific Solutions
- Soil Map Layers (Indian Agro-Ecological Soil Zones, ICAR / NBSS&LUP data benchmarks)
- Soil Protection Quizzes (Beginner & Advanced with rationales)
- Sustainable Soil Conservation Challenges & Field Activities
"""

SOIL_PROBLEMS = [
    {
        'id': 'erosion',
        'category': 'Physical Degradation',
        'category_badge': 'badge-physical',
        'name': 'Soil Erosion (Water & Wind)',
        'telugu_name': 'నేల కోత (నీరు & గాలి ద్వారా)',
        'icon': 'fa-solid fa-water',
        'short_desc': 'Detachment and transport of topsoil by torrential rainfall, runoff, or strong dry winds.',
        'causes': [
            'Leaving fields bare without cover crops or mulch during heavy monsoon rains',
            'Excessive or deep conventional tillage pulverizing stable soil aggregates',
            'Cultivating steep slopes without contour terraces or bunding',
            'Overgrazing along field borders that destroys natural vegetative cover'
        ],
        'warning_signs': [
            'Rills, gullies, or sheet wash channels forming after rains',
            'Exposed plant root crowns and muddy sediment accumulating in low spots',
            'Dust clouds rising from fields during dry pre-monsoon winds',
            'Gradual thinning of fertile dark topsoil and exposure of lighter subsoil'
        ],
        'crop_effects': [
            'Loss of topsoil organic matter, which contains up to 70% of available nutrients',
            'Shallowing of root-zone depth, stunting taproots and causing crop lodging',
            'Destruction of soil pore architecture, reducing rainwater infiltration and causing surface crusting'
        ],
        'prevention': [
            'Contour Bunding & Trenching: Construct bunds along equal elevation lines to halt runoff velocity',
            'Cover Cropping: Sow cowpea, green gram, or horse gram during transition months to cushion rainfall impact',
            'Vegetative Barriers: Establish deep-rooted Vetiver grass (Khus) hedgerows across field slopes',
            'Zero or Minimum Tillage: Retain crop stubble on field surface to anchor soil aggregates'
        ],
        'sustainable_tips': 'Adopt Agroforestry: Plant nitrogen-fixing trees (e.g., Subabul, Gliricidia) on boundary bunds as windbreaks.',
        'when_to_seek_advice': 'When gully depth exceeds 15 cm, or when sediment runoff continuously covers drainage channels. Consult local Soil Conservation Officers or KVK watershed engineers.'
    },
    {
        'id': 'salinity',
        'category': 'Chemical Degradation',
        'category_badge': 'badge-chemical',
        'name': 'Soil Salinity & Sodicity',
        'telugu_name': 'నేల లవణీయత & చౌడు సమస్య',
        'icon': 'fa-solid fa-snowflake',
        'short_desc': 'Excessive accumulation of soluble salts (salinity) or sodium ions on clay exchange complexes (sodicity).',
        'causes': [
            'Over-irrigation with canal water in poorly drained lowlands causing rising water tables',
            'Pumping and applying saline or brackish groundwater for irrigation',
            'Arid climate with high evaporation exceeding rainfall, causing capillary salt rise',
            'Imbalanced use of chemical fertilizers without organic carbon buffers'
        ],
        'warning_signs': [
            'White or greyish powdery salt crusts on soil ridges after irrigation dries',
            'Sticky, greasy black crusts during wet spells (characteristic of sodic soils)',
            'Stunted crop emergence, patchy germination, and scorched leaf tips',
            'Poor water infiltration: water stands for days without soaking into subsoil'
        ],
        'crop_effects': [
            'Osmotic shock: roots cannot take up water even when soil is wet ("physiological drought")',
            'Sodium toxicity causing marginal leaf necrosis and premature leaf drop',
            'Dispersion of clay particles, destroying all soil aeration and asphyxiating roots'
        ],
        'prevention': [
            'Sub-surface and Open Drainage: Excavate 1-meter deep drainage ditches to remove salt-laden water',
            'Gypsum Application for Sodic Soils: Apply agricultural gypsum (CaSO4) to replace sodium with calcium',
            'Dhaincha Green Manuring: Incorporate 45-day-old Sesbania aculeata; root respiration produces organic acids',
            'Drip Irrigation: Transition from flood irrigation to drip to maintain a low-salt wetting bulb'
        ],
        'sustainable_tips': 'Cultivate moderately salt-tolerant crop varieties (e.g., CSR-series paddy, Karnal grass, barley, cotton).',
        'when_to_seek_advice': 'If soil EC exceeds 2.0 dS/m or pH exceeds 8.5. Request a laboratory Gypsum Requirement Test (GR Test) before purchasing amendments.'
    },
    {
        'id': 'acidity_alkalinity',
        'category': 'Chemical Degradation',
        'category_badge': 'badge-chemical',
        'name': 'Acidic & Alkaline Soils',
        'telugu_name': 'ఆమ్ల మరియు అధిక క్షార నేలలు',
        'icon': 'fa-solid fa-scale-unbalanced',
        'short_desc': 'Extreme soil reaction (pH < 5.5 or pH > 8.5) locking out essential macro- and micronutrients.',
        'causes': [
            'Heavy leaching of basic cations (Ca, Mg, K) in high-rainfall coastal/hill zones (Acidity)',
            'Continuous long-term use of acid-forming fertilizers like Ammonium Sulphate and Urea',
            'Accumulation of calcium and sodium carbonates in semi-arid plains (Alkalinity)',
            'Low organic matter reserves failing to buffer natural soil pH swings'
        ],
        'warning_signs': [
            'In Acid Soils: Stunted seedling roots, stubby root tips, and purplish leaves (Phosphorus fixation)',
            'In Alkaline Soils: Severe yellowing of young leaves (Iron and Zinc deficiency chlorosis)',
            'Poor response to regular NPK fertilizer doses'
        ],
        'crop_effects': [
            'Soluble Aluminum and Manganese reach toxic levels below pH 5.0, halting cell division',
            'Phosphorus binds irreversibly to iron/aluminum in acid soils, and to calcium in alkaline soils',
            'Beneficial earthworms and nitrogen-fixing bacteria (Rhizobium) die out in extreme pH'
        ],
        'prevention': [
            'For Acid Soils: Apply finely ground agricultural limestone or dolomite based on lime requirement tests',
            'For Alkaline Soils: Apply elemental sulphur, pressmud (sugarcane byproduct), or gypsum',
            'Apply well-rotted FYM or vermicompost (5–10 tonnes/ha) to provide organic humic buffering',
            'Select adapted crops: Tea, pineapple, potato for acid soils; barley, mustard for alkaline soils'
        ],
        'sustainable_tips': 'Use biochar in acidic soils; its alkaline ash and high surface area permanently raise pH while storing carbon.',
        'when_to_seek_advice': 'When soil pH tests outside 6.0–8.0. Professional lab buffer testing is required to calculate the exact metric tonnes of lime or gypsum needed.'
    },
    {
        'id': 'nutrient_deficiency',
        'category': 'Nutritional Degradation',
        'category_badge': 'badge-nutrition',
        'name': 'Nutrient Deficiencies & Latent Hunger',
        'telugu_name': 'పోషక లోపాలు & సూక్ష్మ పోషక కొరత',
        'icon': 'fa-solid fa-seedling',
        'short_desc': 'Depletion of essential primary (N, P, K), secondary (S, Ca, Mg), or micronutrients (Zn, Fe, B).',
        'causes': [
            'Imbalanced fertilizer application (e.g., applying only Urea while ignoring P, K, and micronutrients)',
            'Intensive high-yielding multi-cropping without replenishing micronutrients',
            'Low soil organic matter leading to poor nutrient cation exchange capacity (CEC)',
            'Topsoil erosion sweeping away the nutrient-rich surface layer'
        ],
        'warning_signs': [
            'Nitrogen: Uniform pale yellowing starting on oldest lower leaves',
            'Phosphorus: Dark green foliage with reddish-purple discoloration along leaf stems',
            'Potassium: Scorched and necrotic leaf margins ("firing" effect)',
            'Zinc: Rusty brown patches on rice leaves (Khaira disease) and bleached white bands on maize',
            'Iron: Interveinal chlorosis on the youngest upper leaves'
        ],
        'crop_effects': [
            'Yield drops of 20% to 50% even before visual symptoms appear ("hidden hunger")',
            'Weak stems leading to crop lodging in storms',
            'Increased vulnerability to fungal blights and insect pest attacks'
        ],
        'prevention': [
            'Soil Health Card Based Fertilization: Apply targeted NPK ratios rather than blanket fertilizer habits',
            'Biofertilizers: Inoculate seeds with Azospirillum, Rhizobium, and Phosphate Solubilizing Bacteria (PSB)',
            'Foliar Micronutrient Sprays: Apply 0.5% Zinc Sulphate or Ferrous Sulphate during active vegetative stages',
            'Recycle Crop Residues: Composting straw and stalk returns substantial potassium and silica to soil'
        ],
        'sustainable_tips': 'Apply enriched FYM: Mix micronutrients with cow dung manure 10 days before field application to enhance uptake.',
        'when_to_seek_advice': 'When visual leaf symptoms persist after watering, or when yields drop despite standard fertilizer usage. Submit soil and leaf tissue samples to a testing lab.'
    },
    {
        'id': 'organic_matter_loss',
        'category': 'Biological Degradation',
        'category_badge': 'badge-biological',
        'name': 'Loss of Soil Organic Matter (SOC)',
        'telugu_name': 'సేంద్రీయ కర్బనం క్షీణత',
        'icon': 'fa-solid fa-recycle',
        'short_desc': 'Oxidation and rapid burn-off of soil humus and biological carbon under tropical heat and excessive tillage.',
        'causes': [
            'Burning crop residues (paddy stubble, cotton stalks) instead of returning them to soil',
            'Intensive repetitive rotavator tillage exposing organic carbon to sun and atmospheric oxidation',
            'Monoculture without green manure or legume crop rotation',
            'Tropical climate where high soil temperatures accelerate microbial carbon mineralization'
        ],
        'warning_signs': [
            'Pale, chalky or washed-out soil color (loss of rich dark brown humus tones)',
            'Hard crusting on the surface within hours of rain or irrigation',
            'Absence of earthworms, dung beetles, and beneficial soil fauna',
            'Soil quickly dries out and cracks within 2–3 days after irrigation'
        ],
        'crop_effects': [
            'Drastic drop in moisture holding capacity, causing crops to wilt during brief dry spells',
            'Inefficient fertilizer uptake; chemical fertilizers wash away with runoff',
            'Collapse of natural soil disease-suppressive microbes'
        ],
        'prevention': [
            'Mandatory Green Manuring: Sow Dhaincha or Sunn hemp during pre-monsoon and plough under at flowering',
            'Stop Stubble Burning: Use mulchers, super seeders, or happy seeders to incorporate crop residue',
            'Apply Enriched Farmyard Manure or Vermicompost (5 tonnes per hectare annually)',
            'Crop Rotation with Legumes: Rotate cereals with pulses (chickpea, pigeon pea, green gram)'
        ],
        'sustainable_tips': 'Biochar Integration: Add biochar derived from agricultural waste to lock recalcitrant carbon in the soil for centuries.',
        'when_to_seek_advice': 'If soil organic carbon (SOC) test drops below 0.5%. Seek training from local KVK on on-farm vermicomposting and bio-waste management.'
    },
    {
        'id': 'compaction',
        'category': 'Physical Degradation',
        'category_badge': 'badge-physical',
        'name': 'Soil Compaction & Hardpan Formation',
        'telugu_name': 'నేల గట్టిపడటం & హార్డ్‌పాన్ ఏర్పడటం',
        'icon': 'fa-solid fa-compress',
        'short_desc': 'Densification of soil pores and creation of a dense impermeable hardpan layer at 15–25 cm depth.',
        'causes': [
            'Repeated passes of heavy tractors and harvesting machinery on wet soils',
            'Ploughing to the exact same depth year after year using rotary tillers',
            'Puddling of wetland rice soils creating an intentional but persistent subsoil plow-pan',
            'Depletion of organic matter which acts as a natural shock absorber for soil structure'
        ],
        'warning_signs': [
            'Water stands on the field surface long after rain, yet subsoil remains dry',
            'Taproots bend horizontally at 15–20 cm depth ("J-rooting" or "L-rooting")',
            'Excessive tractor fuel consumption and wheel slippage during primary tillage',
            'Penetration resistance: impossible to push a steel probe or stick into moist soil'
        ],
        'crop_effects': [
            'Roots are physically barred from exploring deeper soil layers for stored moisture',
            'Poor soil aeration causes oxygen deficiency (hypoxia) in the root zone',
            'Substantial crop yield reductions in upland crops like cotton, maize, and pulses following rice'
        ],
        'prevention': [
            'Subsoiling (Chisel Ploughing): Break the subsurface hardpan every 3–4 years to a depth of 40–50 cm',
            'Biological Subsoiling: Grow deep taproot cover crops like Daikon radish (tillage radish) or pigeon pea',
            'Controlled Traffic Farming: Confine heavy tractor tires to designated tramlines',
            'Never operate heavy farm machinery when soil is above its field capacity moisture level'
        ],
        'sustainable_tips': 'Protect earthworm populations: Earthworm burrows create natural vertical drainage pipes that shatter compacted zones.',
        'when_to_seek_advice': 'When roots bend sideways or surface ponding persists. Contact your district agricultural engineering wing for rental chisel ploughs.'
    },
    {
        'id': 'waterlogging',
        'category': 'Physical Degradation',
        'category_badge': 'badge-physical',
        'name': 'Waterlogging & Poor Drainage',
        'telugu_name': 'మురుగునీటి సమస్య & నీరు నిలబడటం',
        'icon': 'fa-solid fa-water-ladder',
        'short_desc': 'Prolonged saturation of the root zone where all air pores are filled with water, suffocating roots.',
        'causes': [
            'Inadequate natural slope and lack of community field drainage channels',
            'Excessive flood irrigation and seepage from unlined irrigation canals',
            'Subsurface clay pans or impervious rock layers near the surface',
            'Flash floods during monsoon combined with heavy clay (vertisol) soils'
        ],
        'warning_signs': [
            'Water standing for more than 48 hours following standard rains',
            'Soil smells foul or like rotten eggs (hydrogen sulfide emissions from anaerobic decay)',
            'Bluish-grey or mottled soil colors (gleying due to reduced iron)',
            'Sudden wilting and yellowing of crop leaves despite saturated ground'
        ],
        'crop_effects': [
            'Roots die from lack of oxygen within 24 to 72 hours for sensitive crops (maize, pulses, cotton)',
            'Denitrification converts applied nitrogen fertilizer into nitrous oxide gas, losing fertility',
            'Prolonged saturation triggers root rot fungi (Phytophthora, Pythium, Rhizoctonia)'
        ],
        'prevention': [
            'Broad Bed and Furrow (BBF) System: Raise crop beds 15 cm high with 30 cm furrows to shed excess rain',
            'Ridge and Furrow Planting: Plant sensitive crops on top of ridges',
            'Surface Drainage Ditches: Excavate periphery drains connected to regional natural streams',
            'Laser Land Leveling: Eliminate undulations and low depressions across the field'
        ],
        'sustainable_tips': 'Intercrop with water-tolerant species along drain margins to pump out excess moisture.',
        'when_to_seek_advice': 'When waterlogging is regional or canal-induced. Coordinate with the state irrigation command authority and local panchayat.'
    },
    {
        'id': 'contamination',
        'category': 'Chemical Degradation',
        'category_badge': 'badge-chemical',
        'name': 'Soil Contamination & Chemical Residues',
        'telugu_name': 'నేల కాలుష్యం & రసాయన అవశేషాలు',
        'icon': 'fa-solid fa-biohazard',
        'short_desc': 'Accumulation of toxic synthetic pesticide residues, industrial heavy metals, or untreated wastewater contaminants.',
        'causes': [
            'Repeated over-spraying of persistent pesticides and synthetic insecticides',
            'Using untreated urban sewage or industrial wastewater for vegetable cultivation',
            'Applying low-quality fertilizers or industrial sludges containing heavy metals (Cadmium, Lead, Arsenic)',
            'Dumping non-biodegradable agricultural plastics and chemical packaging'
        ],
        'warning_signs': [
            'Sudden collapse of beneficial soil insect and microbial activity',
            'Persistent crop phytotoxicity and leaf deformities in succeeding crops',
            'Blackened or necrotic root tips on contact with soil',
            'Laboratory testing flags residues exceeding maximum residue limits (MRLs)'
        ],
        'crop_effects': [
            'Bioaccumulation of heavy metals in edible grains and vegetables, posing human health risks',
            'Sterilization of mycorrhizal fungi that aid in plant phosphorus uptake',
            'Rejection of agricultural produce in export and organic certification markets'
        ],
        'prevention': [
            'Integrated Pest Management (IPM): Transition to biological controls (Trichoderma, Pseudomonas, Neem oil)',
            'Stop Wastewater Irrigation: Use only tested, safe groundwater or canal water for food crops',
            'Phytoremediation: Plant hyper-accumulating plants (sunflowers, mustard) to extract contaminants',
            'Proper Disposal: Triple-rinse and safely dispose of all pesticide containers; never bury in fields'
        ],
        'sustainable_tips': 'Bioremediation with Vermicompost: Rich microbial communities in vermicompost accelerate the breakdown of complex pesticide residues.',
        'when_to_seek_advice': 'When industrial effluents threaten groundwater or crops show unexplained stunting. Contact state pollution control boards and regional university toxicologists.'
    },
    {
        'id': 'drought_degradation',
        'category': 'Climatic Degradation',
        'category_badge': 'badge-climatic',
        'name': 'Drought-Related Soil Degradation',
        'telugu_name': 'కరువు వల్ల నేల క్షీణత',
        'icon': 'fa-solid fa-sun',
        'short_desc': 'Severe structural desiccation, cracking, and biological dormancy caused by extended rainfall deficits.',
        'causes': [
            'Prolonged monsoon dry spells and rising summer temperatures exceeding 42°C',
            'Lack of vegetative cover exposing bare soil to intense solar radiation',
            'Low organic matter soils with poor moisture retention capacity',
            'Depletion of groundwater reserves leading to deep water tables'
        ],
        'warning_signs': [
            'Deep vertical hexagonal cracks (especially in Black Cotton Vertisols) exceeding 50 cm depth',
            'Complete pulverization of dry topsoil into loose dust that blows away with light wind',
            'Total wilting and scorching of crops during 15-day dry intervals'
        ],
        'crop_effects': [
            'Root shearing: deep soil cracks tear apart fibrous crop root systems',
            'Microbial dormancy and death: beneficial mycorrhiza and bacteria perish in desiccated soil',
            'Loss of seed germination viability due to lack of seed-zone moisture'
        ],
        'prevention': [
            'Mulching: Cover entire crop rows with crop straw, dry leaves, or plastic film to cut evaporation by 60%',
            'Farm Ponds (Khet Talab): Dig a 1000 m³ farm pond lined with plastic to store runoff for life-saving supplemental irrigation',
            'Hydrogel Soil Conditioners: Apply biodegradable potassium polyacrylate hydrogels to absorb and slowly release moisture',
            'Drought-Tolerant Crops: Cultivate millets (Ragi, Jowar, Bajra), pigeon pea, or safflower'
        ],
        'sustainable_tips': 'Subsurface Drip Irrigation: Delivers water directly to root depth, minimizing all evaporation losses.',
        'when_to_seek_advice': 'When drought conditions trigger regional groundwater stress. Seek assistance under government schemes (PM Krishi Sinchayee Yojana) for subsidized drip kits.'
    }
]

# Educational Quizzes for Learning Zone
QUIZ_QUESTIONS = {
    'beginner': [
        {
            'id': 1,
            'question': 'What is considered the ideal, near-neutral soil pH range for most agricultural crops?',
            'telugu_question': 'చాలా వ్యవసాయ పంటలకు అనువైన నేల పీహెచ్ (pH) పరిధి ఎంత?',
            'options': [
                'pH 3.0 to 4.5',
                'pH 6.5 to 7.5',
                'pH 8.5 to 10.0',
                'pH 11.0 to 14.0'
            ],
            'answer_index': 1,
            'explanation': 'A neutral pH between 6.5 and 7.5 maximizes the availability of both macronutrients (N, P, K) and micronutrients while supporting healthy earthworms and soil bacteria.'
        },
        {
            'id': 2,
            'question': 'Which green manure crop is famous for fixing nitrogen and tolerating both waterlogging and alkaline conditions?',
            'telugu_question': 'నత్రజనిని స్థిరీకరించడంతో పాటు చౌడు నేలలను సైతం తట్టుకునే పచ్చిరొట్ట పైరు ఏది?',
            'options': [
                'Dhaincha (Sesbania aculeata)',
                'Sugarcane',
                'Tobacco',
                'Eucalyptus'
            ],
            'answer_index': 0,
            'explanation': 'Dhaincha (జీలుగ) produces high biomass, fixes atmospheric nitrogen via stem and root nodules, and releases organic acids that neutralize alkaline carbonates.'
        },
        {
            'id': 3,
            'question': 'Under Indian agro-climatic conditions, what percentage of Soil Organic Carbon (SOC) is considered critically low?',
            'telugu_question': 'భారతదేశ నేలల్లో ఎంత శాతం కంటే తక్కువ సేంద్రీయ కర్బనం (SOC) ఉంటే లోపంగా పరిగణిస్తారు?',
            'options': [
                'Less than 0.50%',
                'Between 1.5% and 2.5%',
                'Above 3.0%',
                'Exactly 5.0%'
            ],
            'answer_index': 0,
            'explanation': 'In tropical Indian soils, Organic Carbon below 0.50% indicates critical deficit, resulting in poor moisture retention and weak microbial activity.'
        },
        {
            'id': 4,
            'question': 'What amendment is scientifically recommended to reclaim sodic (high sodium, pH > 8.5) soils?',
            'telugu_question': 'చౌడు (Sodic, pH > 8.5) నేలల పునరుద్ధరణకు ఏది వాడాలి?',
            'options': [
                'Common Table Salt',
                'Agricultural Gypsum (Calcium Sulphate)',
                'Chemical Urea',
                'Plastic Granules'
            ],
            'answer_index': 1,
            'explanation': 'Agricultural Gypsum supplies soluble calcium ions (Ca²⁺) that displace toxic exchangeable sodium (Na⁺) from clay surfaces, allowing it to be leached out.'
        },
        {
            'id': 5,
            'question': 'Which symptom on rice plants is the classic warning sign of Zinc deficiency?',
            'telugu_question': 'వరి పంటలో జింక్ లోపానికి ప్రధాన సంకేతం ఏది?',
            'options': [
                'Khaira disease (rusty brown spots and patches on leaves)',
                'Black rot on stem',
                'White powder on roots',
                'Giant swollen flowers'
            ],
            'answer_index': 0,
            'explanation': 'Khaira disease appears 2–3 weeks after transplanting in zinc-deficient rice soils, causing rusty bronze or reddish-brown leaf discoloration.'
        }
    ],
    'advanced': [
        {
            'id': 6,
            'question': 'Why should water-soluble phosphatic fertilizers NOT be broadcasted directly onto strongly acidic soils (pH < 5.0)?',
            'telugu_question': 'తీవ్రమైన ఆమ్ల నేలల్లో (pH < 5.0) భాస్వరం ఎరువులను నేరుగా ఎందుకు చల్లకూడదు?',
            'options': [
                'Phosphorus quickly dissolves into toxic chlorine gas',
                'Free Aluminum and Iron ions fix phosphate into insoluble compounds',
                'It causes earthworms to multiply too fast',
                'Phosphorus evaporates into the air within minutes'
            ],
            'answer_index': 1,
            'explanation': 'In strongly acidic soils, active aluminum (Al³⁺) and iron (Fe³⁺) ions chemically bind with orthophosphate anions, forming insoluble precipitates that plant roots cannot absorb.'
        },
        {
            'id': 7,
            'question': 'What is the primary physical benefit of applying vermicompost to heavy clay (vertisol) soils?',
            'telugu_question': 'నల్లరేగడి (క్లే) నేలలకు వర్మీ కంపోస్ట్ వేయడం వల్ల కలిగే ప్రధాన భౌతిక ప్రయోజనం ఏమిటి?',
            'options': [
                'It turns the soil completely white',
                'It forms stable soil aggregates, improving aeration and easing root penetration',
                'It eliminates the need for any rainwater',
                'It instantly vaporizes all weed seeds'
            ],
            'answer_index': 1,
            'explanation': 'Earthworm casts and humic substances act as organic glue, binding fine clay particles into water-stable crumbs. This prevents soil crusting and massive cracking.'
        },
        {
            'id': 8,
            'question': 'How does subsoiling (chisel ploughing to 45 cm) differ from traditional rotary tillage?',
            'telugu_question': 'రోటరీ టిల్లర్ కంటే సబ్‌సాయిలింగ్ (చీసెల్ ప్లౌ) ఏ విధంగా భిన్నమైనది?',
            'options': [
                'Subsoiling shatters the subsurface plough-pan hardpan without inverting the topsoil layer',
                'Subsoiling removes all moisture from the field',
                'Subsoiling only works at midnight',
                'Subsoiling creates a hard glass floor under the soil'
            ],
            'answer_index': 0,
            'explanation': 'Subsoiling lifts and shatters the dense compaction pan created by tractors and rotary tillers at 20 cm depth, restoring deep root penetration and groundwater recharge.'
        },
        {
            'id': 9,
            'question': 'Which biofertilizer forms a symbiotic fungal association with plant roots to expand phosphorus absorption by up to 300%?',
            'telugu_question': 'భాస్వరాన్ని గ్రహించడంలో మొక్కల వేర్లకు సహాయపడే శిలీంధ్ర సంబంధిత బయోఫెర్టిలైజర్ ఏది?',
            'options': [
                'Vesicular Arbuscular Mycorrhiza (VAM)',
                'Urea granules',
                'Copper sulphate',
                'Potassium chloride'
            ],
            'answer_index': 0,
            'explanation': 'VAM (Mycorrhizae) develops extensive fungal hyphae networks extending far beyond root tips, accessing locked soil phosphorus and transporting it back to the host plant.'
        },
        {
            'id': 10,
            'question': 'In the Universal Soil Loss Equation (USLE: A = R × K × LS × C × P), what does factor "C" represent?',
            'telugu_question': 'నేల నష్ట సమీకరణం (USLE) లో "C" దేనిని సూచిస్తుంది?',
            'options': [
                'Cover and Crop Management factor',
                'Cost of tractor fuel',
                'Color of topsoil',
                'Count of farmer family members'
            ],
            'answer_index': 0,
            'explanation': 'Factor C represents Cover and Management. Maintaining vegetative mulch or cover crops reduces the C factor, drastically lowering overall annual soil erosion.'
        }
    ]
}

# Soil Map Datasets & Agro-Ecological Zones of India (Based on ICAR & NBSS&LUP data)
INDIA_SOIL_ZONES = [
    {
        'id': 'alluvial',
        'name': 'Alluvial Soils (ఇండస్-గంగా-బ్రహ్మపుత్ర & తీరప్రాంత నేలలు)',
        'lat': 26.8467,
        'lng': 80.9462,
        'coverage': 'Approx. 40% of India’s land area (Indo-Gangetic Plain, Brahmaputra valley, coastal deltas of Mahanadi, Godavari, Krishna, Cauvery)',
        'texture': 'Sandy loam to silty clay',
        'ph_range': '6.5 – 8.2',
        'general_fertility': 'High fertility, rich in Potash and Lime, generally deficient in Nitrogen and Organic Carbon',
        'key_crops': 'Rice, Wheat, Sugarcane, Jute, Oilseeds, Vegetables',
        'major_threats': 'Waterlogging in canal tracts, declining organic matter, micronutrient (Zinc, Boron) depletion',
        'conservation_priority': 'Laser land leveling, balanced NPK with green manure, and precision drip irrigation',
        'color': '#3b82f6'
    },
    {
        'id': 'black',
        'name': 'Black / Regur Soils (నల్లరేగడి నేలలు - డెక్కన్ పీఠభూమి)',
        'lat': 19.7515,
        'lng': 75.7139,
        'coverage': 'Maharashtra, Gujarat, Western Madhya Pradesh, Northern Karnataka, Telangana, parts of Andhra Pradesh',
        'texture': 'Heavy montmorillonitic clay (swell-shrink characteristics)',
        'ph_range': '7.2 – 8.5',
        'general_fertility': 'High moisture retention, rich in Calcium, Magnesium, Potassium; low in Nitrogen, Phosphorus, and Organic Carbon',
        'key_crops': 'Cotton, Soybean, Sorghum (Jowar), Pigeon pea, Wheat, Sunflower',
        'major_threats': 'Severe deep cracking during dry season, surface waterlogging and poor drainage in heavy rains, sheet erosion',
        'conservation_priority': 'Broad Bed and Furrow (BBF) systems, gypsum application in sodic patches, minimum tillage to retain structure',
        'color': '#1f2937'
    },
    {
        'id': 'red_yellow',
        'name': 'Red & Yellow Soils (ఎర్ర నేలలు - దక్షిణ & తూర్పు భారతదేశం)',
        'lat': 15.9129,
        'lng': 79.7400,
        'coverage': 'Andhra Pradesh, Telangana, Tamil Nadu, Karnataka, Odisha, Chota Nagpur plateau, parts of Northeast',
        'texture': 'Loamy sand to sandy loam with iron oxides giving red/yellow tints',
        'ph_range': '5.5 – 7.0',
        'general_fertility': 'Moderate to low fertility; low water retention; deficient in Nitrogen, Phosphorus, Humus, and Lime',
        'key_crops': 'Groundnut, Millets (Ragi, Bajra), Pulses, Tobacco, Castor, Vegetables',
        'major_threats': 'High runoff and splash erosion, fast moisture evaporation during dry spells, acidity in high-rainfall pockets',
        'conservation_priority': 'Contour bunding, continuous mulching with crop straw, regular FYM / vermicompost addition to boost water retention',
        'color': '#ef4444'
    },
    {
        'id': 'laterite',
        'name': 'Laterite Soils (లాటరైట్ నేలలు - పశ్చిమ కనుమలు & ఎత్తైన ప్రాంతాలు)',
        'lat': 11.8745,
        'lng': 75.3704,
        'coverage': 'Western Ghats (Kerala, Coastal Karnataka, Goa), Eastern Ghats (Odisha, Andhra hills), parts of Assam',
        'texture': 'Porous, coarse, gravelly clay rich in iron and aluminum sesquioxides',
        'ph_range': '4.5 – 5.8 (Strongly Acidic)',
        'general_fertility': 'Leached of soluble silica and lime; low available Phosphorus and Potassium; poor organic retention',
        'key_crops': 'Tea, Coffee, Rubber, Cashew nut, Coconut, Pepper, Cardamom',
        'major_threats': 'Extreme tropical leaching, aluminum toxicity, phosphorus fixation',
        'conservation_priority': 'Agricultural liming (CaCO3), heavy organic mulching, terraced contour cultivation, and rock phosphate with mycorrhiza',
        'color': '#d97706'
    },
    {
        'id': 'arid_desert',
        'name': 'Arid & Desert Soils (ఎడారి నేలలు - పశ్చిమ రాజస్థాన్)',
        'lat': 26.9124,
        'lng': 70.9000,
        'coverage': 'Thar Desert (Western Rajasthan, Northern Gujarat, parts of Southwestern Punjab and Haryana)',
        'texture': 'Coarse sand with high permeability and near-zero cohesion',
        'ph_range': '7.8 – 9.0',
        'general_fertility': 'Very low organic carbon (<0.2%), low nitrogen, high soluble salts and phosphates',
        'key_crops': 'Pearl Millet (Bajra), Cluster bean (Guar), Moth bean, Mustard under canal irrigation',
        'major_threats': 'Severe wind erosion, sand dune shifting, rapid moisture evaporation, salinization',
        'conservation_priority': 'Shelterbelts with Khejri (Prosopis cineraria) trees, sand dune stabilization with native grasses (Cenchrus ciliaris), drip irrigation',
        'color': '#eab308'
    },
    {
        'id': 'mountain',
        'name': 'Mountain & Forest Soils (పర్వత & అటవీ నేలలు)',
        'lat': 31.1048,
        'lng': 77.1734,
        'coverage': 'Himalayan region (Jammu & Kashmir, Himachal Pradesh, Uttarakhand, Sikkim, Arunachal Pradesh)',
        'texture': 'Silty loam to gravelly, shallow soil profiles',
        'ph_range': '5.0 – 6.5',
        'general_fertility': 'Rich in surface humus from forest leaf litter, but shallow depth and deficient in available phosphorus and potash',
        'key_crops': 'Apples, Pears, Walnuts, Saffron, Barley, Maize, Mountain potato',
        'major_threats': 'Steep slope land degradation, landslides, intense sheet and gully erosion during monsoon cloudbursts',
        'conservation_priority': 'Inward-sloping bench terracing, vegetative contour hedgerows, stone bunds, and permanent tree-grass horticulture (Silvopasture)',
        'color': '#059669'
    },
    {
        'id': 'saline_alkaline',
        'name': 'Coastal Saline & Inland Sodic Soils (ఉప్పు మరియు చౌడు నేలలు)',
        'lat': 22.3072,
        'lng': 69.8000,
        'coverage': 'Rann of Kutch (Gujarat), Sundarbans (West Bengal), coastal strips of AP & Tamil Nadu, canal-irrigated basins of Haryana & UP',
        'texture': 'Varies from sandy coastal deposits to impervious clay plains',
        'ph_range': '8.2 – 9.8 (High ESP) / EC > 4.0 dS/m',
        'general_fertility': 'Unsuitable for conventional crops without reclamation; excessive sodium, chlorides, and sulphates',
        'key_crops': 'Salt-tolerant rice varieties (Pokkali, CSR-36), Mangrove halophytes, Casuarina',
        'major_threats': 'Osmotic drought, total root asphyxiation, clay deflocculation and impervious hardpans',
        'conservation_priority': 'Subsurface drainage pipelines, gypsum incorporation, cultivation of Sesbania (Dhaincha), and ridge planting',
        'color': '#8b5cf6'
    }
]

# Educational Field Activities for Farmers & Students
FIELD_ACTIVITIES = [
    {
        'title': 'The Jar Test: Determine Your Soil Texture at Home',
        'subtitle': 'Zero cost, simple kitchen science to discover your Sand, Silt, and Clay ratios.',
        'steps': [
            'Take a clear glass jar or plastic water bottle.',
            'Fill 1/3 of the jar with dried soil from your field (dig 15 cm deep, remove stones).',
            'Add clean water until the jar is 80% full, and add 1 teaspoon of liquid dish soap or salt (to disperse clay).',
            'Shake vigorously for 60 seconds, then place on a flat table without disturbing.',
            'Watch the layers settle: Sand settles in 1 minute; Silt settles in 2 hours; Clay stays suspended and takes 24–48 hours to settle.',
            'Measure the thickness of each layer with a ruler to calculate your soil texture percentage.'
        ]
    },
    {
        'title': 'The Simple Organic Compost Recipe (100-Day Humus)',
        'subtitle': 'Turn crop residues and cow dung into dark gold for your soil.',
        'steps': [
            'Layer 1 (Brown Carbon): 15 cm of dry straw, maize stalks, or dry leaves.',
            'Layer 2 (Green Nitrogen): 10 cm of fresh green weeds, pulse crop residues, or kitchen peels.',
            'Layer 3 (Microbial Starter): 5 cm of fresh cow dung slurry mixed with fertile soil.',
            'Moisture: Keep the pile moist like a squeezed sponge (50-60% moisture). Do not over-saturate.',
            'Aeration: Turn the pile every 21 days with a pitchfork to supply oxygen to beneficial aerobic bacteria.',
            'In 90 to 100 days, you will have crumbly, sweet-smelling, dark brown humus ready for field application.'
        ]
    },
    {
        'title': 'The Earthworm Health Census',
        'subtitle': 'Count your underground workforce to assess biological vitality.',
        'steps': [
            'Mark a square area of 30 cm × 30 cm in your moist field during morning hours.',
            'Dig down to a depth of 30 cm and gently place the soil on a tarp or plastic bag.',
            'Carefully crumble the soil by hand and count all active earthworms found.',
            'Interpretation: 0–3 worms = Depleted soil (High chemical impact, low organic carbon); 5–10 worms = Moderately healthy; > 15 worms = Thriving, biologically rich soil.'
        ]
    }
]
