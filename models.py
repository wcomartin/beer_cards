from database import db

class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beer_type = db.Column(db.String(80), nullable=False)
    style = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ibu = db.Column(db.Float, nullable=False)
    abv = db.Column(db.Float, nullable=False)
    card_action = db.Column(db.Text, nullable=False)
    hops = db.Column(db.Integer, nullable=False)
    grains = db.Column(db.Integer, nullable=False)
    yeast = db.Column(db.Integer, nullable=False)
    water = db.Column(db.Integer, nullable=False)
    special = db.Column(db.Integer, nullable=False)
    group_action = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Beer {self.id}>'