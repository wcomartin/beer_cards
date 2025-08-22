from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required
from importer import import_csv
from models import Beer
from database import db # This import should be near the top with other imports

beer_bp = Blueprint('beer_bp', __name__)

@beer_bp.route('/')
@login_required
def index():
    beers = Beer.query.all()
    return render_template('beers.html', beers=beers)

@beer_bp.route('/beers/print')
@login_required
def beer_print():
    beers = Beer.query.all()
    return render_template('beer_print.html', beers=beers)

@beer_bp.route('/beer/import', methods=['GET', 'POST'])
@login_required
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
                session.modified = True
                return redirect(url_for('beer_bp.index'))
            except Exception as e:
                flash(f'Error importing CSV: {e}', 'error')
                session.modified = True
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a CSV file.', 'error')
            session.modified = True
            return redirect(request.url)
    return render_template('import_beers.html')

@beer_bp.route('/beer/<int:beer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_beer(beer_id):
    beer = Beer.query.get_or_404(beer_id)

    if request.method == 'POST':
        beer.beer_type = request.form.get('beer_type')
        beer.style = request.form.get('style')
        beer.country = request.form.get('country')
        beer.description = request.form.get('description')
        beer.ibu = float(request.form.get('ibu')) if request.form.get('ibu') else 0.0
        beer.abv = float(request.form.get('abv')) if request.form.get('abv') else 0.0
        beer.card_action = request.form.get('card_action')
        beer.hops = int(float(request.form.get('hops'))) if request.form.get('hops') else 0
        beer.grains = int(float(request.form.get('grains'))) if request.form.get('grains') else 0
        beer.yeast = int(float(request.form.get('yeast'))) if request.form.get('yeast') else 0
        beer.water = int(float(request.form.get('water'))) if request.form.get('water') else 0
        beer.special = int(float(request.form.get('special'))) if request.form.get('special') else 0
        beer.group_action = request.form.get('group_action')

        try:
            db.session.commit()
            flash('Beer updated successfully!', 'success')
            session.modified = True
            return redirect(url_for('beer_bp.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating beer: {e}', 'error')
            session.modified = True
            return redirect(url_for('beer_bp.edit_beer', beer_id=beer.id))
    
    return render_template('edit_beer.html', beer=beer)