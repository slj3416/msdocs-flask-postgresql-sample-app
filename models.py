from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    red_count = db.Column(db.Integer, nullable=False)
    green_count = db.Column(db.Integer, nullable=False)
    blue_count = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)

    def _repr_(self):
        return f'<ImageData {self.filename}>'