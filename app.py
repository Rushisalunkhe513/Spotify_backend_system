from flask_smorest import Api

from db import db

from flask import Flask
import os

from dotenv import load_dotenv

from resources.MusicCategory import blp as MusciCategoryBLP
from resources.songs import blp as SongsBLP
from resources.artists import blp as ArtistBLP
from resources.user import blp as UserBLP

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

with app.app_context():
    import models # models defined in modesl file.
    db.create_all() # we are telling our application to create tables we defined in maodels or in applivtion in database.

# now lets register one part of application catgory
api.register_blueprint(MusciCategoryBLP) # we have registered MusicCtegory Blurpint in here,by doing this we can acces MusicCategory routes in application.
api.register_blueprint(SongsBLP) # added Blueprint for Songs.
api.register_blueprint(ArtistBLP) # added Artist Blueprint to app.py
api.register_blueprint(UserBLP)
