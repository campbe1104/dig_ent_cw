from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(2), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
