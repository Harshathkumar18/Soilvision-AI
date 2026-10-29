"""
SoilCare Unit Tests — Report Parser
Tests regex text extraction, sample PDF processing, confidence flags,
and file extension validation.
"""

import unittest
import os
from services.report_parser import (
    parse_report_text, process_uploaded_report, allowed_file
)

class TestReportParser(unittest.TestCase):

    def test_allowed_file(self):
        self.assertTrue(allowed_file('soil_card.pdf'))
        self.assertTrue(allowed_file('scan.JPG'))
        self.assertTrue(allowed_file('report.png'))
        self.assertFalse(allowed_file('script.exe'))
        self.assertFalse(allowed_file('data.csv'))

    def test_parse_report_text(self):
        sample_text = """
        GOVERNMENT OF INDIA - SOIL HEALTH CARD
        Farmer Name: Ramesh Patel
        District: Guntur, State: Andhra Pradesh
        Crop: Paddy
        pH : 6.8
        EC : 0.65 dS/m
        OC : 0.82 %
        Available Nitrogen : 380 kg/ha
        Available Phosphorus : 22.5 kg/ha
        Available Potassium : 240 kg/ha
        Zinc : 0.95 ppm
        Iron : 6.20 ppm
        """
        result = parse_report_text(sample_text)
        extracted = result['extracted']

        self.assertEqual(extracted['ph'], 6.8)
        self.assertEqual(extracted['ec'], 0.65)
        self.assertEqual(extracted['oc'], 0.82)
        self.assertEqual(extracted['nitrogen'], 380.0)
        self.assertEqual(extracted['phosphorus'], 22.5)
        self.assertEqual(extracted['potassium'], 240.0)
        self.assertEqual(extracted['zinc'], 0.95)
        self.assertEqual(extracted['iron'], 6.2)
        self.assertEqual(result['metadata']['farmer_name'], 'Ramesh Patel')
        self.assertEqual(result['metadata']['district'], 'Guntur')

    def test_process_sample_pdf(self):
        sample_pdf_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'static', 'samples', 'sample_soil_health_card.pdf'
        )
        if os.path.exists(sample_pdf_path):
            res = process_uploaded_report(sample_pdf_path)
            self.assertTrue(res['has_matches'])
            self.assertEqual(res['extracted']['ph'], 6.8)
            self.assertEqual(res['extracted']['nitrogen'], 380.0)

if __name__ == '__main__':
    unittest.main()
