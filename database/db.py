"""
SoilVision AI SQLite Database Manager
Provides safe connection handling, schema creation, and persistence for:
- Soil test records & interpretations
- Uploaded report tracking
- Saved farm locations & coordinates
- Educational quiz performance metrics
- User feedback/inquiries
- Dashboard aggregation metrics
"""

import sqlite3
import json
import os
from datetime import datetime

DATABASE_NAME = 'soilcare.db'

def get_db_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, DATABASE_NAME)

def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if tables do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Soil analysis records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS soil_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            farmer_name TEXT,
            state TEXT,
            district TEXT,
            target_crop TEXT,
            soil_type TEXT,
            ph REAL,
            ec REAL,
            oc REAL,
            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,
            zinc REAL,
            iron REAL,
            copper REAL,
            manganese REAL,
            boron REAL,
            sulphur REAL,
            moisture REAL,
            temperature REAL,
            health_score INTEGER,
            ratings_json TEXT,
            concerns_json TEXT,
            recommendations_json TEXT,
            notes TEXT
        )
    ''')

    # Saved farm locations on the map
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farm_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            farm_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            soil_type TEXT,
            notes TEXT,
            record_id INTEGER,
            FOREIGN KEY (record_id) REFERENCES soil_records(id) ON DELETE SET NULL
        )
    ''')

    # Uploaded soil reports
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            extracted_json TEXT,
            confirmed_json TEXT,
            status TEXT DEFAULT 'pending_confirmation'
        )
    ''')

    # Educational quiz scores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            player_name TEXT,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL
        )
    ''')

    # Ensure all columns exist (auto-migration for existing database)
    cursor.execute("PRAGMA table_info(soil_records)")
    existing_cols = [row['name'] for row in cursor.fetchall()]
    for col, col_type in [
        ('health_score', 'INTEGER'),
        ('moisture', 'REAL'),
        ('temperature', 'REAL'),
    ]:
        if col not in existing_cols:
            cursor.execute(f"ALTER TABLE soil_records ADD COLUMN {col} {col_type}")

    # Contact / community questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name TEXT NOT NULL,
            email_or_phone TEXT,
            topic TEXT,
            message TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_soil_record(data, analysis_result):
    """Saves a confirmed soil analysis into the database using sanitized parameters."""
    conn = get_connection()
    cursor = conn.cursor()

    clean_params = analysis_result.get('parameters', {}) if isinstance(analysis_result, dict) else {}
    health_score = analysis_result.get('health_index') if isinstance(analysis_result, dict) else None

    farmer_name = str(data.get('farmer_name') or 'Farmer').strip()[:100]
    state = str(data.get('state') or '').strip()[:100]
    district = str(data.get('district') or '').strip()[:100]
    target_crop = str(data.get('target_crop') or 'General').strip()[:100]
    soil_type = str(data.get('soil_type') or 'Unknown').strip()[:100]
    notes = str(data.get('notes') or '').strip()[:500]
    moisture = clean_params.get('moisture')
    temperature = clean_params.get('temperature')

    cursor.execute('''
        INSERT INTO soil_records (
            farmer_name, state, district, target_crop, soil_type,
            ph, ec, oc, nitrogen, phosphorus, potassium,
            zinc, iron, copper, manganese, boron, sulphur,
            moisture, temperature, health_score,
            ratings_json, concerns_json, recommendations_json, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        farmer_name or 'Farmer',
        state,
        district,
        target_crop,
        soil_type,
        clean_params.get('ph'),
        clean_params.get('ec'),
        clean_params.get('oc'),
        clean_params.get('nitrogen'),
        clean_params.get('phosphorus'),
        clean_params.get('potassium'),
        clean_params.get('zinc'),
        clean_params.get('iron'),
        clean_params.get('copper'),
        clean_params.get('manganese'),
        clean_params.get('boron'),
        clean_params.get('sulphur'),
        moisture,
        temperature,
        health_score,
        json.dumps(analysis_result.get('ratings', {})),
        json.dumps(analysis_result.get('concerns', [])),
        json.dumps(analysis_result.get('recommendations', [])),
        notes
    ))

    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id

def delete_soil_record(record_id):
    """Deletes a soil analysis record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM soil_records WHERE id = ?', (record_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_soil_record(record_id):
    """Fetches a specific soil analysis record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM soil_records WHERE id = ?', (record_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        record = dict(row)
        record['ratings'] = json.loads(record.get('ratings_json') or '{}')
        record['concerns'] = json.loads(record.get('concerns_json') or '[]')
        record['recommendations'] = json.loads(record.get('recommendations_json') or '[]')
        return record
    return None

def get_recent_records(limit=6):
    """Fetches the most recent soil analyses."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, created_at, farmer_name, state, district, target_crop, soil_type,
               ph, ec, oc, nitrogen, phosphorus, potassium, health_score
        FROM soil_records ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_soil_records(limit=50):
    """Fetches list of all soil records for My Soil Reports page."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, created_at, farmer_name, state, district, target_crop, soil_type,
               ph, ec, oc, nitrogen, phosphorus, potassium, health_score
        FROM soil_records ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def save_farm_location(farm_name, lat, lng, soil_type='', notes='', record_id=None):
    """Saves a user pinned farm location on the map."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO farm_locations (farm_name, latitude, longitude, soil_type, notes, record_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (farm_name[:100], float(lat), float(lng), soil_type[:100], notes[:300], record_id))
    loc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return loc_id

def get_farm_locations():
    """Retrieves all saved farm locations."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.*, s.target_crop, s.health_score, s.ph
        FROM farm_locations f
        LEFT JOIN soil_records s ON f.record_id = s.id
        ORDER BY f.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_farm_location(loc_id):
    """Deletes a saved farm location."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM farm_locations WHERE id = ?', (loc_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def save_uploaded_report(filename, original_filename, file_type, file_size, extracted_data=None):
    """Logs an uploaded report into uploaded_reports table for auditing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO uploaded_reports (
            filename, original_filename, file_type, file_size, extracted_json, status
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        filename,
        original_filename,
        file_type,
        file_size,
        json.dumps(extracted_data) if extracted_data else None,
        'completed' if extracted_data else 'pending_confirmation'
    ))
    rep_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rep_id

def save_quiz_attempt(player_name, difficulty, score, total_questions):
    """Saves a completed quiz result."""
    conn = get_connection()
    cursor = conn.cursor()
    pct = round((score / total_questions) * 100, 1) if total_questions > 0 else 0
    cursor.execute('''
        INSERT INTO quiz_attempts (player_name, difficulty, score, total_questions, percentage)
        VALUES (?, ?, ?, ?, ?)
    ''', (player_name or 'Soil Friend', difficulty, score, total_questions, pct))
    conn.commit()
    conn.close()
    return pct

def get_quiz_leaderboard(limit=10):
    """Fetches highest quiz scores."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_name, difficulty, score, total_questions, percentage, created_at 
        FROM quiz_attempts 
        ORDER BY score DESC, created_at DESC 
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_dashboard_stats():
    """
    Computes live dashboard statistics from database:
    - Analyzed reports count
    - Average soil health score
    - Detected nutrient issues count
    - Saved farm locations count
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM soil_records')
    total_reports = cursor.fetchone()[0]

    cursor.execute('SELECT AVG(health_score) FROM soil_records WHERE health_score IS NOT NULL')
    avg_score_raw = cursor.fetchone()[0]
    avg_health_score = round(avg_score_raw) if avg_score_raw is not None else 72

    # Nutrient issues count (low nitrogen, low phosphorus, low potassium, or low organic carbon)
    cursor.execute('''
        SELECT COUNT(*) FROM soil_records 
        WHERE (nitrogen IS NOT NULL AND nitrogen < 280)
           OR (phosphorus IS NOT NULL AND phosphorus < 10)
           OR (potassium IS NOT NULL AND potassium < 110)
           OR (oc IS NOT NULL AND oc < 0.50)
           OR (ph IS NOT NULL AND (ph < 5.5 OR ph > 8.5))
    ''')
    nutrient_issues = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM farm_locations')
    saved_locations = cursor.fetchone()[0]

    conn.close()

    return {
        'total_reports': total_reports,
        'avg_health_score': avg_health_score,
        'nutrient_issues': nutrient_issues,
        'saved_locations': saved_locations
    }
