from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship('Signup', back_populates='activity')
    # Add serialization rules
    serialize_rules = ('-signups.activity', '-signups.camper')
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship('Signup', back_populates='camper')
    # Add serialization rules
    serialize_rules = ('-signups.camper',)
    # Add validation
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Camper must have a name.")
        return name
    @validates('age')
    def validate_age(self, key, age):
        if not 8 <= age <= 18:
            raise ValueError("Campers must be between 8 and 18 years old.")
        return age
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'
        


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    # Add relationships
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    activity = db.relationship('Activity', back_populates='signups', cascade='delete')

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    camper = db.relationship('Camper', back_populates='signups', cascade='delete')
    # Add serialization rules
    serialize_rules = ('-camper.signup', '-activity.signup')
    # Add validation
    @validates('time')
    def validate_time(self, key, time):
        if not 0 <= time <= 23:
            raise ValueError("Time must be between 0 and 23 hours.")
        return time

    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
