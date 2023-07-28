from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from config import db

class User( db.Model, SerializerMixin ):
    __tablename__ = 'users'
    serialize_rules = ( '-created_at', '-updated_at' )

    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String )
    age = db.Column( db.Integer )

    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )


    @validates('age')
    #  This happens when you try to create the user
    def check_age(self, key, age_given):
        # If the given age is less than 18, throw a Value error
        if age_given < 18:
            #  ValueError raises an error when the wrong value is given
            raise ValueError('Must be 18 years or older.')
        # If the age is above 18, add the given age to the instance 
        return age_given