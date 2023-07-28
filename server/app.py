from flask import request, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from config import app, db, api

from models.user import User


class Users( Resource ):
    def get( self ):
        # This is pulling all of the users from the User model and creates an instance for each user (u).
        return make_response( [ u.to_dict() for u in User.query.all() ] )

    def post( self ):
        data = request.json
        
        # The validation we put in the model causes a situation in which this can break. So when we're doing something we know might cause an error, we use try. Try says if there's no error, keep going but if there is an error we run an exception. The exception is something people will be able to see on the front-end whereas the validation error breaks the back-end and the front-end won't be able to see why
        try:
            user = User( name = data['name'], age = data['age'] )
        except:
            # This is where the other code will go if the User instance breaks
            return make_response({'error' : 'OH NO ALL BAD!'}, 422)
        # You can also put the error from the Validate as the value like this:
        # except: ValueError as v_error:
        #   return make_response({'error' : str(v_error)}, 422)
        # BUT all the ValueErrors will then return the same thing
        
        db.session.add( user )
        db.session.commit()

        return make_response( user.to_dict(), 201 )

api.add_resource( Users, '/users' )



if __name__ == '__main__':
    app.run( port = 5555, debug = True )

