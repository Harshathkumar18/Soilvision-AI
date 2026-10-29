"""
SoilCare Live Server HTTP Smoke Tester
Checks that all routes, endpoints, JSON responses, and AI chat respond with HTTP 200.
"""

import requests

BASE_URL = 'http://127.0.0.1:5000'

routes = [
    '/',
    '/problems',
    '/analyzer',
    '/upload',
    '/map',
    '/quiz',
    '/about',
    '/api/map-data',
    '/api/quiz-questions'
]

print("--- Testing GET Routes ---")
for r in routes:
    resp = requests.get(f"{BASE_URL}{r}")
    print(f"GET {r:22} -> HTTP {resp.status_code}")
    assert resp.status_code == 200, f"Failed on {r}"

print("\n--- Testing POST /api/analyze ---")
payload = {
    'farmer_name': 'Ramesh Patel',
    'state': 'Andhra Pradesh',
    'district': 'Guntur',
    'target_crop': 'Paddy (Rice)',
    'ph': 6.8,
    'ec': 0.65,
    'oc': 0.82,
    'nitrogen': 380,
    'phosphorus': 22.5,
    'potassium': 240
}
res = requests.post(f"{BASE_URL}/api/analyze", json=payload)
print(f"POST /api/analyze        -> HTTP {res.status_code}, Health Index: {res.json().get('health_index')} / 100")
assert res.status_code == 200

print("\n--- Testing POST /api/chat ---")
chat_res = requests.post(f"{BASE_URL}/api/chat", json={'message': 'How do I prevent soil erosion during heavy rains?'})
reply = chat_res.json().get('reply', '')
print(f"POST /api/chat           -> HTTP {chat_res.status_code}, Reply snippet: {reply[:80]}...")
assert chat_res.status_code == 200

print("\nALL LIVE ENDPOINTS PASSED WITH FLYING COLORS!")
