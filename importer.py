import csv
from app import db, app
from models import Beer

def import_csv(filename='beers.csv'):
    with app.app_context():
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader) # Skip header row
            for row in reader:
                beer = Beer(
                    id=row[0],
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

if __name__ == '__main__':
    import_csv()