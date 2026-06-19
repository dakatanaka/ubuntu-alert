from app import db
from datetime import datetime

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    last_location = db.Column(db.String(200), nullable=False)
    clothing = db.Column(db.String(200))
    medical = db.Column(db.String(200))
    police_case = db.Column(db.String(100))
    vehicle = db.Column(db.String(200))
    reporter_name = db.Column(db.String(100))
    reporter_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Watcher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(100))
    area = db.Column(db.String(200))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

class Sighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)