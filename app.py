from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from flask_migrate import Migrate # Added this import
import os
from importer import import_csv

from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'a_very_secret_key' # You should change this to a strong, random key in production
db.init_app(app)
migrate = Migrate(app, db) # Added this line

from models import Beer



@app.route('/')
def index():
    beers = Beer.query.all()
    return render_template('beers.html', beers=beers)

@app.route('/beers/print')
def beer_print():
    beers = Beer.query.all()
    return render_template('beer_print.html', beers=beers)



@app.route('/beer/import', methods=['GET', 'POST'])
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
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error importing CSV: {e}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a CSV file.', 'error')
            return redirect(request.url)
    return render_template('import_beers.html')

if __name__ == '__main__':
    app.run(debug=True)
