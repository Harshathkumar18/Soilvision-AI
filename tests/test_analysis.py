"""
SoilCare Unit Tests — Soil Analysis Engine
Verifies ICAR benchmark thresholds, multi-dimensional health index,
handling of partial/missing inputs, and agronomic recommendation rules.
"""

import unittest
from services.soil_analysis import (
    analyze_soil_health, evaluate_parameter, clean_float, THRESHOLDS
)
from services.recommendations import generate_recommendations

class TestSoilAnalysis(unittest.TestCase):

    def test_clean_float(self):
        self.assertEqual(clean_float("6.8"), 6.8)
        self.assertEqual(clean_float(7.5), 7.5)
        self.assertIsNone(clean_float(""))
        self.assertIsNone(clean_float(None))
        self.assertIsNone(clean_float("invalid"))

    def test_ph_thresholds(self):
        # Acidic
        eval_acid = evaluate_parameter('ph', 4.8)
        self.assertEqual(eval_acid['rating'], 'Strongly Acidic')
        self.assertEqual(eval_acid['badge'], 'warning')

        # Neutral Ideal
        eval_neutral = evaluate_parameter('ph', 6.8)
        self.assertEqual(eval_neutral['rating'], 'Neutral (Ideal)')
        self.assertEqual(eval_neutral['badge'], 'success')

        # Alkaline/Sodic
        eval_alkaline = evaluate_parameter('ph', 8.9)
        self.assertEqual(eval_alkaline['rating'], 'Strongly Alkaline / Sodic')
        self.assertEqual(eval_alkaline['badge'], 'danger')

    def test_ec_salinity(self):
        eval_safe = evaluate_parameter('ec', 0.6)
        self.assertEqual(eval_safe['rating'], 'Normal (Safe)')

        eval_saline = evaluate_parameter('ec', 3.5)
        self.assertEqual(eval_saline['rating'], 'Moderately Saline')

    def test_organic_carbon(self):
        eval_low = evaluate_parameter('oc', 0.35)
        self.assertEqual(eval_low['rating'], 'Low (Critical Deficit)')

        eval_opt = evaluate_parameter('oc', 0.85)
        self.assertEqual(eval_opt['rating'], 'High (Optimal)')

    def test_multi_factor_index_not_ph_alone(self):
        """
        Verify that soil health index does not solely depend on pH.
        Even if pH is optimal (7.0), severe organic carbon deficit and low NPK
        should lower the overall vitality index.
        """
        balanced_inputs = {
            'ph': 7.0, 'ec': 0.6, 'oc': 0.85,
            'nitrogen': 380, 'phosphorus': 20, 'potassium': 220
        }
        res_balanced = analyze_soil_health(balanced_inputs)
        self.assertGreater(res_balanced['health_index'], 80)

        depleted_inputs = {
            'ph': 7.0, 'ec': 0.6, 'oc': 0.25,
            'nitrogen': 140, 'phosphorus': 5, 'potassium': 60
        }
        res_depleted = analyze_soil_health(depleted_inputs)
        self.assertLess(res_depleted['health_index'], 60)

    def test_recommendations_generation(self):
        sample = {
            'parameters': {'ph': 8.9, 'ec': 2.8, 'oc': 0.35},
            'ratings': {
                'ph': {'rating': 'Strongly Alkaline / Sodic'},
                'nitrogen': {'rating': 'Low'}
            },
            'concerns': [],
            'target_crop': 'Cotton'
        }
        recs = generate_recommendations(sample)
        self.assertTrue(len(recs) >= 3)
        # Sodic soil recommendation should mention Gypsum and Dhaincha
        gypsum_found = any('Gypsum' in r['title'] or 'Gypsum' in r['action'] for r in recs)
        self.assertTrue(gypsum_found)

if __name__ == '__main__':
    unittest.main()
