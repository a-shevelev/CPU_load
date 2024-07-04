from datetime import datetime

from app.database.models import db

class CPULoad(db.Model):
    __tablename__ = "cpu_load"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    load = db.Column(db.Float, nullable=True)

class ServerStatus(db.Model):
    __tablename__ = "server_status"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    status = db.Column(db.String, nullable=False)
