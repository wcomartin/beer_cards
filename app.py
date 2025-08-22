from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from weasyprint import HTML, CSS
import os
from importer import import_csv

from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'a_very_secret_key' # You should change this to a strong, random key in production
db.init_app(app)

from models import Beer

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def index():
    beers = Beer.query.all()
    return render_template('beers.html', beers=beers)

@app.route('/beers/print')
def beer_print():
    beers = Beer.query.all()
    return render_template('beer_print.html', beers=beers)

@app.route('/beers/pdf')
def beers_pdf():
    beers = Beer.query.all()
    rendered_html = render_template('beer_print.html', beers=beers)

    # Read CSS files
    with open('static/css/card.css', 'r') as f:
        card_css = f.read()
    with open('static/css/style.css', 'r') as f:
        style_css = f.read()

    # Create WeasyPrint CSS objects
    weasy_card_css = CSS(string=card_css)
    weasy_style_css = CSS(string=style_css)

    # Create a WeasyPrint HTML object from the rendered HTML
    html = HTML(string=rendered_html, base_url=request.url_root)

    # Generate PDF with styles
    pdf = html.write_pdf(stylesheets=[weasy_card_css, weasy_style_css])

    # Create a Flask response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=beers.pdf'
    return response

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
