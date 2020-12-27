#import flask - from the package import class
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException


db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
   app=Flask(__name__)  # this is the name of the module/package that is calling this app
   app.debug=True
   app.secret_key='utroutoru'


   # handles any internal error servers such as an invalid route
   # @app.errorhandler(404) 
   # def invalid_route(e): 
   #    return render_template("error_handling.html")

   # @app.errorhandler(Exception)
   # def internal_server_error(e):
   #    return render_template('error_handling.html', e = e)
   
   # set the app configuration data 
   app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///marketplace.sqlite'


   #initialize db & bootstrap with flask app
   db.init_app(app)
   bootstrap = Bootstrap(app)


   # The folder to store images
   UPLOAD_FOLDER = '/static/image'
   app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



   # #initialize the login manager
   login_manager = LoginManager()

   # #set the name of the login function that lets user login
   # # in our case it is auth.login (blueprintname.viewfunction name)
   login_manager.login_view='auth.login'
   login_manager.init_app(app)

   #create a user loader function takes userid and returns User
   from .models import User  # importing here to avoid circular references
   @login_manager.user_loader
   def load_user(user_id):
      return User.query.get(int(user_id))

   # importing views module here to avoid circular references
   # a commonly used practice.
   from . import views
   app.register_blueprint(views.bp)

   from . import auth
   app.register_blueprint(auth.bp)

   from . import listings
   app.register_blueprint(listings.bp)


   return app
   



