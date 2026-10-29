"""
SoilVision AI — The Future of Smart Soil Analysis
Main Flask Application Server
Connects routes, SQLite persistence, ICAR soil interpretation engine,
report OCR parser, bilingual translations, interactive map APIs, and AI assistant.
"""

import os
import json
import uuid
from flask import (
    Flask, render_template, request, jsonify, redirect, url_for,
    session, send_from_directory, flash
)
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# Internal services and database
from database.db import (
    init_db, save_soil_record, get_soil_record, get_recent_records,
    get_all_soil_records, delete_soil_record, save_farm_location,
    get_farm_locations, delete_farm_location, get_dashboard_stats,
    save_quiz_attempt, get_quiz_leaderboard, get_connection, save_uploaded_report
)
from services.soil_analysis import analyze_soil_health, CROPS_DATA
from services.recommendations import generate_recommendations
from services.report_parser import process_uploaded_report, allowed_file
from services.ai_assistant import get_ai_response
from services.translations import TRANSLATIONS, get_text
from services.knowledge_data import (
    SOIL_PROBLEMS, QUIZ_QUESTIONS, INDIA_SOIL_ZONES, FIELD_ACTIVITIES
)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'soilvision-ai-secret-key-prod-secure')

# Configure upload limits (10 MB max)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database schema on startup
with app.app_context():
    init_db()

@app.before_request
def setup_session_language():
    """Sets default language to 'en' if not already present in session or requested via query."""
    lang_param = request.args.get('lang')
    if lang_param in ['en', 'te']:
        session['lang'] = lang_param
    elif 'lang' not in session:
        session['lang'] = 'en'

@app.context_processor
def inject_global_template_vars():
    """Injects translation dictionary and language into all Jinja templates."""
    current_lang = session.get('lang', 'en')
    return {
        'lang': current_lang,
        't': lambda key: get_text(current_lang, key),
        'translations': TRANSLATIONS.get(current_lang, TRANSLATIONS['en']),
        'crops_list': list(CROPS_DATA.keys())
    }

# ----------------- Navigation Routes -----------------

@app.route('/')
def home():
    """Home landing page with live dashboard summary stats."""
    recent_analyses = get_recent_records(limit=4)
    stats = get_dashboard_stats()
    return render_template(
        'index.html',
        recent_analyses=recent_analyses,
        featured_problems=SOIL_PROBLEMS[:3],
        stats=stats
    )

@app.route('/problems')
def problems():
    """Soil Problems & Solutions directory with category filters."""
    category = request.args.get('category', 'all')
    search_query = request.args.get('q', '').strip().lower()

    filtered_problems = SOIL_PROBLEMS
    if category != 'all':
        filtered_problems = [p for p in filtered_problems if p['category'].lower().startswith(category.lower())]

    if search_query:
        filtered_problems = [
            p for p in filtered_problems
            if search_query in p['name'].lower()
            or search_query in p['short_desc'].lower()
            or any(search_query in c.lower() for c in p['causes'])
        ]

    return render_template(
        'problems.html',
        problems=filtered_problems,
        current_category=category,
        search_query=search_query
    )

@app.route('/soil-analyzer')
@app.route('/soil-analizer')
@app.route('/analyzer')
def analyzer():
    """Interactive Soil Health Analyzer page."""
    return render_template('analyzer.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """Processes soil health parameters and returns scientific ICAR evaluation."""
    data = request.get_json() if request.is_json else request.form.to_dict()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    analysis = analyze_soil_health(data)
    recommendations = generate_recommendations(analysis)
    analysis['recommendations'] = recommendations

    # Persist record in database
    record_id = save_soil_record(data, analysis)
    analysis['record_id'] = record_id

    return jsonify(analysis)

@app.route('/report/<int:record_id>')
def view_report(record_id):
    """View and print a saved soil analysis card."""
    record = get_soil_record(record_id)
    if not record:
        flash('Requested soil record was not found.', 'danger')
        return redirect(url_for('analyzer'))

    # Build evaluation from stored data
    analysis = analyze_soil_health(record)
    recommendations = generate_recommendations(analysis)
    analysis['recommendations'] = recommendations

    return render_template(
        'report.html',
        record=record,
        analysis=analysis
    )

@app.route('/report/<int:record_id>/delete', methods=['POST'])
def delete_report(record_id):
    """Delete a saved soil analysis record."""
    deleted = delete_soil_record(record_id)
    if deleted:
        flash(f'Soil report #{record_id} has been permanently deleted.', 'success')
    else:
        flash('Report not found or already deleted.', 'warning')
    return redirect(url_for('my_reports'))

@app.route('/reports')
@app.route('/my-reports')
def my_reports():
    """My Soil Reports management page."""
    records = get_all_soil_records(limit=50)
    stats = get_dashboard_stats()
    return render_template('reports.html', records=records, stats=stats)

@app.route('/upload')
def upload_page():
    """Soil Report OCR and Text Extraction page."""
    return render_template('upload.html')

@app.route('/api/upload', methods=['POST'])
def api_upload_report():
    """
    Accepts PDF/JPG/PNG report, extracts candidate parameters,
    and returns editable confirmation payload.
    """
    if 'report_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['report_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file format. Please upload PDF, JPG, or PNG.'}), 400

    # Secure file save
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(saved_path)

    try:
        extraction_result = process_uploaded_report(saved_path)
        extraction_result['filename'] = unique_filename
        file_size = os.path.getsize(saved_path) if os.path.exists(saved_path) else 0
        save_uploaded_report(unique_filename, file.filename, ext, file_size, extraction_result.get('extracted'))
        return jsonify(extraction_result)
    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500

@app.route('/map')
def soil_map():
    """Interactive Leaflet.js Soil Map of India."""
    locations = get_farm_locations()
    return render_template('map.html', saved_locations=locations)

@app.route('/api/map-data')
def api_map_data():
    """Returns verified agro-ecological soil zones of India."""
    return jsonify({
        'status': 'success',
        'source': 'ICAR - National Bureau of Soil Survey & Land Use Planning (NBSS&LUP)',
        'zones': INDIA_SOIL_ZONES,
        'disclaimer': 'Regional agro-ecological soil mapping cannot substitute individual farm-level soil testing.'
    })

@app.route('/api/locations', methods=['GET', 'POST'])
def api_locations():
    """Get all saved farm locations or save a new one."""
    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('farm_name', '').strip()
        lat = data.get('latitude')
        lng = data.get('longitude')
        if not name or lat is None or lng is None:
            return jsonify({'error': 'Farm name, latitude and longitude are required.'}), 400
        
        loc_id = save_farm_location(
            farm_name=name,
            lat=lat,
            lng=lng,
            soil_type=data.get('soil_type', ''),
            notes=data.get('notes', ''),
            record_id=data.get('record_id')
        )
        return jsonify({'status': 'success', 'id': loc_id})
    else:
        return jsonify(get_farm_locations())

@app.route('/api/locations/<int:loc_id>/delete', methods=['POST'])
def api_delete_location(loc_id):
    """Deletes a saved farm location."""
    deleted = delete_farm_location(loc_id)
    return jsonify({'status': 'success' if deleted else 'not_found'})

@app.route('/quiz')
def quiz():
    """Learning Zone and Interactive Quiz."""
    leaderboard = get_quiz_leaderboard(limit=5)
    return render_template(
        'quiz.html',
        activities=FIELD_ACTIVITIES,
        leaderboard=leaderboard
    )

@app.route('/api/quiz-questions')
def api_quiz_questions():
    """Fetches quiz questions for a chosen difficulty level."""
    diff = request.args.get('difficulty', 'beginner').lower()
    questions = QUIZ_QUESTIONS.get(diff, QUIZ_QUESTIONS['beginner'])
    return jsonify({'questions': questions, 'difficulty': diff})

@app.route('/api/quiz-submit', methods=['POST'])
def api_quiz_submit():
    """Evaluates quiz submission, logs score, and returns explanations."""
    payload = request.get_json() or {}
    difficulty = payload.get('difficulty', 'beginner')
    player_name = payload.get('player_name', 'Soil Friend').strip() or 'Soil Friend'
    user_answers = payload.get('answers', {})

    target_questions = QUIZ_QUESTIONS.get(difficulty, QUIZ_QUESTIONS['beginner'])
    score = 0
    feedback = []

    for q in target_questions:
        qid = str(q['id'])
        chosen_idx = user_answers.get(qid)
        try:
            chosen_idx_int = int(chosen_idx) if chosen_idx is not None else None
        except (ValueError, TypeError):
            chosen_idx_int = None

        is_correct = (chosen_idx_int is not None and chosen_idx_int == q['answer_index'])
        if is_correct:
            score += 1

        feedback.append({
            'id': q['id'],
            'question': q['question'],
            'chosen_index': chosen_idx_int,
            'correct_index': q['answer_index'],
            'is_correct': is_correct,
            'explanation': q['explanation']
        })

    total = len(target_questions)
    percentage = save_quiz_attempt(player_name, difficulty, score, total)

    return jsonify({
        'score': score,
        'total': total,
        'percentage': percentage,
        'feedback': feedback
    })

@app.route('/about')
def about():
    """About SoilVision AI, institutional partners, scientific methodology, and disclaimer."""
    return render_template('about.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """AI Assistant endpoint for farmer questions."""
    payload = request.get_json() or {}
    prompt = payload.get('message', '').strip()
    language = session.get('lang', 'en')

    if not prompt:
        return jsonify({'error': 'Empty question'}), 400

    reply = get_ai_response(prompt, language)
    return jsonify({
        'reply': reply,
        'language': language,
        'has_gemini_key': bool(os.environ.get('GEMINI_API_KEY'))
    })

@app.route('/set-language', methods=['POST'])
def set_language():
    """Toggles session language between en and te."""
    data = request.get_json() or {}
    new_lang = data.get('language', 'en')
    if new_lang in ['en', 'te']:
        session['lang'] = new_lang
    return jsonify({'status': 'success', 'lang': session['lang']})

@app.route('/contact', methods=['POST'])
def submit_contact():
    """Saves user feedback or inquiries."""
    name = request.form.get('name', 'Anonymous')
    contact = request.form.get('contact', '')
    topic = request.form.get('topic', 'General Inquiry')
    message = request.form.get('message', '')

    if message:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO inquiries (name, email_or_phone, topic, message) VALUES (?, ?, ?, ?)',
            (name, contact, topic, message)
        )
        conn.commit()
        conn.close()
        flash('Thank you for contacting SoilCare / SoilVision AI! Your message has been safely received.', 'success')
    else:
        flash('Please enter a message before submitting.', 'warning')

    return redirect(url_for('about'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
