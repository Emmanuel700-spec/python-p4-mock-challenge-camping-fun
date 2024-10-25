from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Camper(db.Model):
    __tablename__ = 'campers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Relationship with Signup
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')

    # Validation method for Camper
    def validate(self):
        errors = []
        if not self.name:
            errors.append("must have a name")
        if not (8 <= self.age <= 18):
            errors.append("age must be between 8 and 18")
        return errors

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    # Relationship with Signup
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')

class Signup(db.Model):
    __tablename__ = 'signups'
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    # Relationships
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    # Validation method for Signup
    def validate(self):
        errors = []
        if not (0 <= self.time <= 23):
            errors.append("time must be between 0 and 23")
        return errors
