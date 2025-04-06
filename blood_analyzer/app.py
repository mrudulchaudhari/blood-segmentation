import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import utils

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For flash messages

# Configure upload settings
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store analysis history (would use a database in production)
analyses = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    # Load model accuracy metrics when the app starts
    model_metrics = utils.get_model_metrics()
    return render_template('index.html', 
                          recent_analyses=analyses[:5],
                          model_metrics=model_metrics)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))
    
    if file and allowed_file(file.filename):
        # Create unique filename to prevent overwrites
        filename = f"{uuid.uuid4()}{os.path.splitext(secure_filename(file.filename))[1]}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze the blood image
        result = utils.analyze_blood_image(filepath)
        
        # Store analysis result
        analysis_id = len(analyses) + 1
        analysis = {
            'id': analysis_id,
            'image_path': filepath,
            'diagnosis': result['diagnosis'],
            'confidence': result['confidence'],
            'details': result['details'],
            'cell_count': result.get('metrics', {}).get('cell_count', 0),
            'cell_irregularity': result.get('metrics', {}).get('cell_irregularity', 0),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        analyses.append(analysis)
        
        return redirect(url_for('results', analysis_id=analysis_id))
    
    flash('File type not allowed')
    return redirect(url_for('home'))

@app.route('/results/<int:analysis_id>')
def results(analysis_id):
    # Find the analysis with the given ID
    analysis = next((a for a in analyses if a['id'] == analysis_id), None)
    if not analysis:
        flash('Analysis not found')
        return redirect(url_for('home'))
    
    # Load model accuracy metrics
    model_metrics = utils.get_model_metrics()
    
    return render_template('results.html', 
                          analysis=analysis, 
                          model_metrics=model_metrics)

@app.route('/history')
def history():
    return render_template('history.html', 
                          analyses=analyses,
                          model_metrics=utils.get_model_metrics())

if __name__ == '__main__':
    app.run(debug=True)