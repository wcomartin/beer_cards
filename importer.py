import csv
import io # Added import io
from models import Beer

def import_csv(filename_or_file_object):
    from app import db, app
    with app.app_context():
        if isinstance(filename_or_file_object, str):
            f = open(filename_or_file_object, 'r', encoding='utf-8') # Added encoding
        else:
            f = io.TextIOWrapper(filename_or_file_object, encoding='utf-8') # Wrapped in TextIOWrapper

        reader = csv.reader(f)
        next(reader)

        for row in reader:
            beer_id = int(row[0])

            beer = Beer.query.get(beer_id)

            if beer:
                beer.beer_type = row[1]
                beer.style = row[2]
                beer.country = row[3]
                beer.description = row[4]
                beer.ibu = float(row[5]) if row[5] else 0.0
                beer.abv = float(row[6]) if row[6] else 0.0
                beer.card_action = row[7]
                beer.hops = int(float(row[8])) if row[8] else 0
                beer.grains = int(float(row[9])) if row[9] else 0
                beer.yeast = int(float(row[10])) if row[10] else 0
                beer.water = int(float(row[11])) if row[11] else 0
                beer.special = int(float(row[12])) if row[12] else 0
                beer.group_action = row[13]
            else:
                beer = Beer(
                    id=beer_id,
                    beer_type=row[1],
                    style=row[2],
                    country=row[3],
                    description=row[4],
                    ibu=float(row[5]) if row[5] else 0.0,
                    abv=float(row[6]) if row[6] else 0.0,
                    card_action=row[7],
                    hops=int(float(row[8])) if row[8] else 0,
                    grains=int(float(row[9])) if row[9] else 0,
                    yeast=int(float(row[10])) if row[10] else 0,
                    water=int(float(row[11])) if row[11] else 0,
                    special=int(float(row[12])) if row[12] else 0,
                    group_action=row[13]
                )
                db.session.add(beer)
        db.session.commit()

        if isinstance(filename_or_file_object, str):
            f.close()