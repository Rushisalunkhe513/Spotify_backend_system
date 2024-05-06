from flask_smorest import Api

from db import db

from flask import Flask,jsonify
import os

from datetime import datetime,timedelta

from models.admin import AdminModel

"""
CORS is a mechanism that allows a web server to specify who can access its resources from a web page served by a different domain.
this is CROSS-ORIGINAL-RESOURCE-SHARING which used to direct trafffic from one address to another.
"""
from flask_cors import CORS 

from flask_jwt_extended import JWTManager  # used for Authorization and Authentication process in aoolication.

from dotenv import load_dotenv

from confg_utils.config import ProductionConfig,DevelopmentConfig

from blocklist import Blocklist

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
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

if os.getenv("PRODUCTION")==True:
    config_db = ProductionConfig()
    app.config["SQLALCHEMY_DATABASE_URI"] = config_db.db_url
else:
    config_db = DevelopmentConfig()
    app.config["SQLALCHEMY_DATABASE_URI"] = config_db.db_url
    
"""
# Replace 'your_ip_address' with your actual IP address
CORS(app, resources={r"/api/*": {"origins": "http://your_ip_address"}})

# we can multiple ip addresses as well
CORS(app, resources={r"/api/*": {"origins": "http://ip1, http://ip2, http://ip3"}})
"""

# app means our flask application
# r"/ means all request that have / in it
# origins means from any domain/ip request can be accespted.
CORS(app, resources={r"/*": {"origins": "*"}})

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

# lets add some jwt methods

"""
This all jwt methods will look for jwt authentic token and token being used.
"""

# this @jwt.token_in_blocklist_loader will look for token is in blocklist or not.
@jwt.token_in_blocklist_loader 
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in Blocklist

# now lets check if token is expired or still active
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

# lets check if token is real and authentic one with respect to there signature key.
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

# added functionality for give error when token is missing.
@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )
    
# will ask for fresh token
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )

# token that is in blocklist is used.
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )
# lets implement various jwt error method. like invalid jwt token, token expiration time and more.


with app.app_context():
    import models # models defined in modesl file.
    db.create_all() # we are telling our application to create tables we defined in maodels or in applivtion in database.
    
    # creating default admin data in admin table. default admin added to database.
    default_admin = AdminModel(id = os.getenv("admin_id"),name = os.getenv("admin_name"),password = pbkdf2_sha256.hash(os.getenv("admin_password")),mobile_number = os.getenv("admin_mobile_number"))
    db.session.add(default_admin)
    db.session.commit()
    
    
# now lets register one part of application catgory
api.register_blueprint(MusciCategoryBLP) # we have registered MusicCtegory Blurpint in here,by doing this we can acces MusicCategory routes in application.
api.register_blueprint(SongsBLP) # added Blueprint for Songs.
api.register_blueprint(ArtistBLP) # added Artist Blueprint to app.py
api.register_blueprint(UserBLP) # user and his playlist
api.register_blueprint(PlaylistAndPlaylistSongsBLP) # user playlist and playlist songs.
api.register_blueprint(AdminBluePrint) # added admin part of application.
