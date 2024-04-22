from flask_smorest import Blueprint,abort

from flask.views import MethodView

from models import Songs,SongDetails




blp  = Blueprint("songs",__name__,description="Operation on songs",url_prefix="/songs")




# user will search for song with name or by category_id
