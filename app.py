from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
