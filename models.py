from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class AgentName(db.Model):
    __tablename__ = 'agentname'
    name_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(13), nullable=False)
    pollingunit_uniqueid = db.Column(db.Integer, nullable=False)


class AnnouncedPUResult(db.Model):
    __tablename__ = 'announced_pu_results'
    result_id = db.Column(db.Integer, primary_key=True)
    polling_unit_uniqueid = db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score = db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_ip_address = db.Column(db.String(50), nullable=False)


class AnnouncedLGAResult(db.Model):
    __tablename__ = 'announced_lga_results'
    result_id = db.Column(db.Integer, primary_key=True)
    lga_name = db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score = db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_ip_address = db.Column(db.String(50), nullable=False)


class AnnouncedStateResult(db.Model):
    __tablename__ = 'announced_state_results'
    result_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score = db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_ip_address = db.Column(db.String(50), nullable=False)


class AnnouncedWardResult(db.Model):
    __tablename__ = 'announced_ward_results'
    result_id = db.Column(db.Integer, primary_key=True)
    ward_name = db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score = db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_ip_address = db.Column(db.String(50), nullable=False)


class LGA(db.Model):
    __tablename__ = 'lga'
    uniqueid = db.Column(db.Integer, primary_key=True)
    lga_id = db.Column(db.Integer, nullable=False)
    lga_name = db.Column(db.String(50), nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    lga_description = db.Column(db.Text)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.DateTime, nullable=False)
    user_ip_address = db.Column(db.String(50), nullable=False)

class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key=True)
    partyid = db.Column(db.String(11), nullable=False)
    partyname = db.Column(db.String(11), nullable=False)


class PollingUnit(db.Model):
    __tablename__ = 'polling_unit'
    uniqueid = db.Column(db.Integer, primary_key=True)
    polling_unit_id = db.Column(db.Integer, nullable=False)
    ward_id = db.Column(db.Integer, nullable=False)
    lga_id = db.Column(db.Integer, nullable=False)
    uniquewardid = db.Column(db.Integer)
    polling_unit_number = db.Column(db.String(50))
    polling_unit_name = db.Column(db.String(50))
    polling_unit_description = db.Column(db.Text)
    lat = db.Column(db.String(255))
    long = db.Column(db.String(255))
    entered_by_user = db.Column(db.String(50))
    date_entered = db.Column(db.DateTime)
    user_ip_address = db.Column(db.String(50))


class State(db.Model):
    __tablename__ = 'states'
    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False)


class Ward(db.Model):
    __tablename__ = 'ward'
    uniqueid = db.Column(db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, nullable=False)
    ward_name = db.Column(db.String(50), nullable=False)
    lga_id = db.Column(db.Integer, nullable=False)
    ward_description = db.Column(db.Text)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.DateTime, nullable=False)
    user_ip_address = db.Column(db.String(50), nullable=False)
