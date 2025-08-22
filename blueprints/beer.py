from flask import Blueprint, render_template, request, flash, redirect, url_for, session # Added session
from flask_login import login_required # Added this import
from importer import import_csv
from models import Beer # Assuming models are accessible via 'models' package

beer_bp = Blueprint('beer_bp', __name__)

@beer_bp.route('/')
@login_required # Added decorator
def index():
    beers = Beer.query.all()
    return render_template('beers.html', beers=beers)

@beer_bp.route('/beers/print')
@login_required # Added decorator
def beer_print():
    beers = Beer.query.all()
    return render_template('beer_print.html', beers=beers)

@beer_bp.route('/beer/import', methods=['GET', 'POST'])
@login_required # Added decorator
def beer_import():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        csv_file = request.files['csv_file']
        if csv_file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if csv_file and csv_file.filename.endswith('.csv'):
            try:
                import_csv(csv_file.stream)
                flash('CSV imported successfully!', 'success')
                session.modified = True # Added this line
                return redirect(url_for('beer_bp.index')) # Redirect to blueprint's index
            except Exception as e:
                flash(f'Error importing CSV: {e}', 'error')
                session.modified = True # Added this line
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a CSV file.', 'error')
            session.modified = True # Added this line
            return redirect(request.url)
    return render_template('import_beers.html')