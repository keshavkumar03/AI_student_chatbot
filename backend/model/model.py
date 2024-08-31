from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    # Define other model fields here