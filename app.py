from flask_smorest import Api

from db import db

from flask import Flask
import os

from datetime import datetime,timedelta

from models.admin import AdminModel

from flask_jwt_extended import JWTManager  # used for Authorization and Authentication process in aoolication.

from dotenv import load_dotenv

from passlib.hash import pbkdf2_sha256

from resources.MusicCategory import blp as MusciCategoryBLP
from resources.songs import blp as SongsBLP
from resources.artists import blp as ArtistBLP
from resources.user import blp as UserBLP
from resources.user_playlists import blp as PlaylistAndPlaylistSongsBLP
from resources.admin import blp as AdminBluePrint

load_dotenv()

app = Flask(__name__) # passed Flask() to app to initialize new application.
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

# now lets start working with database as application starts, by initializing database
db.init_app(app)

# now we need to unite/combine small application or blueprint of app together, so we need to do this
api=Api(app)

# lets give our application a secret key to encode jwt token and decode jwt token.
"""
Secret key is important in creating the jwt token and decrypting a jwt token. 
It is must need parametrer in any application. it adds security to the application.
"""
app.config["JWT_SECRET_KEY"] = os.getenv["jwt_key"] 

# lets get JWTManager in instance
jwt = JWTManager(app) 
"""
we are binding our application to the jwt manager. 
by this our application will get jwtmanager functionalities.
This will allow to use jwt features in our application.
"""

# lets implement various jwt error method. like invalid jwt token, token expiration time and more.


with app.app_context():
    import models # models defined in modesl file.
    db.create_all() # we are telling our application to create tables we defined in maodels or in applivtion in database.
    
    # creating default admin data in admin table. default admin added to database.
    default_admin = AdminModel(id = os.getenv("admin_id"),name = os.getenv("admin_name"),password = pbkdf2_sha256.hash(os.getenv("admoin_password")),mobile_number = os.getenv("admin_mobile_number"))
    db.session.add(default_admin)
    db.session.commit()
    
    
# now lets register one part of application catgory
api.register_blueprint(MusciCategoryBLP) # we have registered MusicCtegory Blurpint in here,by doing this we can acces MusicCategory routes in application.
api.register_blueprint(SongsBLP) # added Blueprint for Songs.
api.register_blueprint(ArtistBLP) # added Artist Blueprint to app.py
api.register_blueprint(UserBLP) # user and his playlist
api.register_blueprint(PlaylistAndPlaylistSongsBLP) # user playlist and playlist songs.
api.register_blueprint(AdminBluePrint) # added admin part of application.
