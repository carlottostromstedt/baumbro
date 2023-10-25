from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trees(db.Model):
    __tablename__ = "trees"

    id            = db.Column(db.Integer,      primary_key=True)
    cadastre_id   = db.Column(db.Integer,      nullable=False)
    fk_species_id = db.Column(db.Varchar(255), nullable=False)

    longitude = db.Column(db.Float, nullable=False)
    latitude  = db.Column(db.Float, nullable=False)

def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()
