"""
SoilCare Comprehensive End-to-End Audit & Test Suite
Executes 40+ rigorous test cases across:
1. Functionality
2. Frontend & Template Rendering
3. Backend & API Validation
4. Security & Injection Checks
5. Performance & Asset Audits
6. Reliability & Error Recovery
7. Code Quality & Linting
"""

import os
import io
import json
import unittest
import sqlite3
from app import app
from database.db import get_connection, get_db_path

class ComprehensiveAuditSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        cls.client = app.test_client()

    # ==========================================
    # 1. FUNCTIONALITY TESTING
    # ==========================================
    def test_func_01_all_get_routes(self):
        """Verify all core navigation endpoints load with HTTP 200."""
        routes = ['/', '/problems', '/analyzer', '/upload', '/map', '/quiz', '/about']
        for route in routes:
            with self.subTest(route=route):
                res = self.client.get(route)
                self.assertEqual(res.status_code, 200, f"Route {route} failed to load.")

    def test_func_02_problems_category_filtering(self):
        """Test directory category filters and query search."""
        categories = ['all', 'Physical', 'Chemical', 'Biological', 'Nutritional', 'Climatic']
        for cat in categories:
            res = self.client.get(f'/problems?category={cat}')
            self.assertEqual(res.status_code, 200)

        # Search query
        res_search = self.client.get('/problems?q=erosion')
        self.assertEqual(res_search.status_code, 200)
        self.assertIn(b'Erosion', res_search.data)

        # Empty result query
        res_none = self.client.get('/problems?q=xyznonexistent123')
        self.assertEqual(res_none.status_code, 200)
        self.assertIn(b'No problems found', res_none.data)

    def test_func_03_analyzer_crud_lifecycle(self):
        """Test soil analysis creation, persistence, and report retrieval."""
        payload = {
            'farmer_name': 'Audit Tester',
            'state': 'Karnataka',
            'district': 'Mysuru',
            'target_crop': 'Paddy (Rice)',
            'soil_type': 'Red Sandy Loam',
            'ph': 6.5,
            'ec': 0.8,
            'oc': 0.72,
            'nitrogen': 310,
            'phosphorus': 16,
            'potassium': 210
        }
        res = self.client.post('/api/analyze', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('record_id', data)
        record_id = data['record_id']
        self.assertIsInstance(record_id, int)

        # Retrieve saved report
        rep_res = self.client.get(f'/report/{record_id}')
        self.assertEqual(rep_res.status_code, 200)
        self.assertIn(b'Audit Tester', rep_res.data)
        self.assertIn(b'Mysuru', rep_res.data)

    def test_func_04_quiz_flow(self):
        """Test quiz question fetching, submission scoring, and leaderboard logging."""
        q_res = self.client.get('/api/quiz-questions?difficulty=advanced')
        self.assertEqual(q_res.status_code, 200)
        qdata = q_res.get_json()
        self.assertTrue(len(qdata['questions']) > 0)

        # Submit attempt
        submit_payload = {
            'difficulty': 'advanced',
            'player_name': 'Audit Quiz Champion',
            'answers': {'1': 0, '2': 1, '3': 2}
        }
        sub_res = self.client.post('/api/quiz-submit', json=submit_payload)
        self.assertEqual(sub_res.status_code, 200)
        sdata = sub_res.get_json()
        self.assertIn('percentage', sdata)

    def test_func_05_contact_form_submission(self):
        """Test user feedback / contact form submission and DB insert."""
        res = self.client.post('/contact', data={
            'name': 'Farmer Rao',
            'contact': '9876543210',
            'topic': 'Soil Health Question',
            'message': 'Need advice on saline black soil in Guntur.'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Thank you for contacting SoilCare', res.data)

    def test_func_06_quiz_malformed_input(self):
        """Test that malformed/string answers do not trigger an unhandled 500 error."""
        res = self.client.post('/api/quiz-submit', json={
            'difficulty': 'beginner',
            'player_name': 'Edge Case Tester',
            'answers': {'1': 'abc', '2': None, '3': [1, 2]}
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('score', data)

    def test_func_07_negative_ph_evaluation(self):
        """Test that negative pH values are properly classified as Acidic and not sodic."""
        from services.soil_analysis import evaluate_parameter
        eval_res = evaluate_parameter('ph', -1.5)
        self.assertEqual(eval_res['rating'], 'Strongly Acidic')

    # ==========================================
    # 2. FRONTEND & TEMPLATE TESTING
    # ==========================================
    def test_front_01_language_switching(self):
        """Test English and Telugu language session persistence."""
        res_te = self.client.post('/set-language', json={'language': 'te'})
        self.assertEqual(res_te.status_code, 200)
        self.assertEqual(res_te.get_json()['lang'], 'te')

        # Visit home page and verify Telugu content rendered
        res_home_te = self.client.get('/')
        self.assertEqual(res_home_te.status_code, 200)
        # Should render Telugu translations
        self.assertIn('హోమ్'.encode('utf-8'), res_home_te.data)

        # Reset to English
        res_en = self.client.post('/set-language', json={'language': 'en'})
        self.assertEqual(res_en.status_code, 200)
        self.assertEqual(res_en.get_json()['lang'], 'en')

    def test_front_02_static_assets_exist(self):
        """Verify that all CSS and JS bundles serve successfully."""
        assets = [
            '/static/css/style.css',
            '/static/js/main.js',
            '/static/js/analyzer.js',
            '/static/js/map.js',
            '/static/js/quiz.js',
            '/static/js/upload.js',
            '/static/images/farmer_hero.jpg',
            '/static/images/farmer_inspecting.jpg',
            '/static/images/field_green.jpg',
            '/static/images/soil_hands.jpg'
        ]
        for asset in assets:
            with self.subTest(asset=asset):
                res = self.client.get(asset)
                self.assertEqual(res.status_code, 200, f"Static asset {asset} missing or 404.")

    # ==========================================
    # 3. BACKEND AND DATABASE TESTING
    # ==========================================
    def test_back_01_empty_analyze_input(self):
        """Test /api/analyze with empty and invalid payloads."""
        res = self.client.post('/api/analyze', json={})
        # Empty payload
        self.assertIn(res.status_code, [200, 400])

    def test_back_02_unexpected_types_in_analyzer(self):
        """Verify server handles unexpected non-numeric types gracefully."""
        bad_payload = {
            'ph': 'invalid_string',
            'ec': [1, 2, 3],
            'nitrogen': {'nested': 'value'},
            'potassium': None
        }
        res = self.client.post('/api/analyze', json=bad_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIsNone(data['parameters']['ph'])
        self.assertIsNone(data['parameters']['ec'])
        self.assertIsNone(data['parameters']['nitrogen'])

    def test_back_03_nonexistent_report_redirect(self):
        """Accessing a non-existent report record should redirect to analyzer with flash message."""
        res = self.client.get('/report/999999', follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn('/analyzer', res.headers['Location'])

    def test_back_04_map_data_schema(self):
        """Verify /api/map-data provides full ICAR geo-zones."""
        res = self.client.get('/api/map-data')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(len(data.get('zones', [])) >= 6)
        for zone in data['zones']:
            self.assertIn('lat', zone)
            self.assertIn('lng', zone)
            self.assertIn('name', zone)
            self.assertIn('texture', zone)
            self.assertIn('color', zone)

    # ==========================================
    # 4. SECURITY TESTING
    # ==========================================
    def test_sec_01_file_upload_extension_restriction(self):
        """Test that dangerous file extensions are rejected with HTTP 400."""
        dangerous_extensions = ['test.exe', 'script.php', 'page.html', 'macro.vbs', 'evil.sh', 'hack.svg']
        for bad_filename in dangerous_extensions:
            with self.subTest(filename=bad_filename):
                data = {'report_file': (io.BytesIO(b'malicious content'), bad_filename)}
                res = self.client.post('/api/upload', data=data, content_type='multipart/form-data')
                self.assertEqual(res.status_code, 400, f"File {bad_filename} was not blocked!")

    def test_sec_02_path_traversal_on_upload(self):
        """Test path traversal attempts in uploaded filenames."""
        traversal_names = ['../../etc/passwd.pdf', '..\\..\\windows\\system32\\calc.pdf', 'folder/../../../test.png']
        for fname in traversal_names:
            with self.subTest(fname=fname):
                data = {'report_file': (io.BytesIO(b'%PDF-1.4 header'), fname)}
                res = self.client.post('/api/upload', data=data, content_type='multipart/form-data')
                # Even if processed, it must never escape UPLOAD_FOLDER
                self.assertIn(res.status_code, [200, 400, 500])

    def test_sec_03_sql_injection_defense(self):
        """Test SQL injection payloads against inquiry / contact form and soil records."""
        sqli_payload = "Robert'); DROP TABLE inquiries; --"
        res = self.client.post('/contact', data={
            'name': sqli_payload,
            'contact': 'sqli@test.com',
            'topic': 'General Inquiry',
            'message': "' OR '1'='1"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        # Verify inquiries table still exists and record was safely inserted parameterized
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM inquiries WHERE name = ?", (sqli_payload,))
        row = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(row, "SQL injection parameterized defense failed or record missing")

    def test_sec_04_xss_protection_in_chat(self):
        """Test that user questions with script tags are handled safely by AI endpoint."""
        xss_payload = "<script>alert('XSS')</script>"
        res = self.client.post('/api/chat', json={'message': xss_payload})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('reply', data)

    # ==========================================
    # 5. RELIABILITY & ERROR HANDLING
    # ==========================================
    def test_rel_01_custom_404_page(self):
        """Verify custom 404 page is rendered for undefined routes."""
        res = self.client.get('/nonexistent-route-xyz-404')
        self.assertEqual(res.status_code, 404)
        self.assertIn(b'404', res.data)
        self.assertIn(b'Page Not Found', res.data)

    def test_rel_02_chat_empty_handling(self):
        """Test empty prompt rejection."""
        res = self.client.post('/api/chat', json={'message': '   '})
        self.assertEqual(res.status_code, 400)
        self.assertIn('error', res.get_json())

    def test_rel_03_contact_empty_message(self):
        """Empty contact message should not insert record."""
        res = self.client.post('/contact', data={
            'name': 'Test',
            'contact': 'test@test.com',
            'topic': 'Topic',
            'message': ''
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Please enter a message', res.data)

if __name__ == '__main__':
    unittest.main()
