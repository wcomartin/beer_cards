from flask import Flask, render_template, make_response, request
from weasyprint import HTML, CSS
import os

from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

from models import Beer

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/beers')
def beers():
    beers = Beer.query.all()
    return render_template('beers.html', beers=beers)

@app.route('/beer_print')
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

if __name__ == '__main__':
    app.run(debug=True)
