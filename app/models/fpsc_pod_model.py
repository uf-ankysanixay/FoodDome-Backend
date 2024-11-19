# app\models\fpsc_pod_model.py

from app.extensions import db

class FpscPOD(db.Model):
    __tablename__ = 'fpsc_pod'

    id = db.Column(db.Integer, primary_key=True)
    storm_id = db.Column(db.String, nullable=False)
    county = db.Column(db.String)
    fpl_accounts = db.Column(db.Integer)
    fpl_out = db.Column(db.Integer)
    fpl_percentage = db.Column(db.Float)
    duke_accounts = db.Column(db.Integer)
    duke_out = db.Column(db.Integer)
    duke_percentage = db.Column(db.Float)
    tampa_accounts = db.Column(db.Integer)
    tampa_out = db.Column(db.Integer)
    tampa_percentage = db.Column(db.Float)
    fpu_accounts = db.Column(db.Integer)
    fpu_out = db.Column(db.Integer)
    fpu_percentage = db.Column(db.Float)
    cooperatives_accounts = db.Column(db.Integer)
    cooperatives_out = db.Column(db.Integer)
    cooperatives_percentage = db.Column(db.Float)
    municipals_accounts = db.Column(db.Integer)
    municipals_out = db.Column(db.Integer)
    municipals_percentage = db.Column(db.Float)

    # Add a unique constraint on the combination of storm_id and county
    __table_args__ = (
        db.UniqueConstraint('storm_id', 'county', name='uix_storm_county'),
    )
