"""
SoilCare Unit Tests — Flask Application Routes & Endpoints
Verifies that all views, JSON APIs, session language toggles,
quiz scoring, and AI chat endpoints operate correctly.
"""

import unittest
import json
from app import app

class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SoilCare', res.data)
        self.assertIn(b'Protect Our Soil', res.data)

    def test_problems_page(self):
        res = self.client.get('/problems')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Soil Erosion', res.data)
        self.assertIn(b'Soil Salinity', res.data)

    def test_analyzer_page(self):
        res = self.client.get('/analyzer')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Soil Health Analyzer', res.data)

    def test_upload_page(self):
        res = self.client.get('/upload')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Upload Soil Health Card', res.data)

    def test_map_page(self):
        res = self.client.get('/map')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Interactive Soil Map', res.data)

    def test_quiz_page(self):
        res = self.client.get('/quiz')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Learning Zone', res.data)

    def test_about_page(self):
        res = self.client.get('/about')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'About the SoilCare Initiative', res.data)

    def test_api_analyze_endpoint(self):
        payload = {
            'farmer_name': 'Test Farmer',
            'state': 'Telangana',
            'district': 'Nalgonda',
            'target_crop': 'Cotton',
            'ph': '8.8',
            'ec': '2.5',
            'oc': '0.40',
            'nitrogen': '220',
            'phosphorus': '8',
            'potassium': '190'
        }
        res = self.client.post('/api/analyze', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('ratings', data)
        self.assertIn('concerns', data)
        self.assertIn('recommendations', data)
        self.assertIn('record_id', data)
        self.assertTrue(len(data['concerns']) >= 1)

    def test_api_map_data_endpoint(self):
        res = self.client.get('/api/map-data')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['zones']) >= 5)

    def test_api_quiz_workflow(self):
        # 1. Fetch questions
        res = self.client.get('/api/quiz-questions?difficulty=beginner')
        self.assertEqual(res.status_code, 200)
        qdata = res.get_json()
        self.assertEqual(qdata['difficulty'], 'beginner')
        self.assertTrue(len(qdata['questions']) >= 3)

        # 2. Submit quiz attempt
        sub_payload = {
            'difficulty': 'beginner',
            'player_name': 'Test Student',
            'answers': {'1': 1, '2': 0, '3': 0}
        }
        sub_res = self.client.post('/api/quiz-submit', data=json.dumps(sub_payload), content_type='application/json')
        self.assertEqual(sub_res.status_code, 200)
        eval_data = sub_res.get_json()
        self.assertIn('score', eval_data)
        self.assertIn('percentage', eval_data)

    def test_api_chat_endpoint(self):
        chat_payload = {'message': 'How can I fix acidic soil?'}
        res = self.client.post('/api/chat', data=json.dumps(chat_payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('reply', data)
        self.assertTrue(len(data['reply']) > 20)

    def test_language_toggle(self):
        res = self.client.post('/set-language', data=json.dumps({'language': 'te'}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['lang'], 'te')

if __name__ == '__main__':
    unittest.main()
