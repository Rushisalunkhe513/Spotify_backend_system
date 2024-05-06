from schema import AddArtistSchema,UpdateArtistDetails,ArtistandSongs


from flask.views import MethodView

from flask_smorest import Blueprint,abort

from models.artist import ArtistModel

from datetime import datetime

from flask_jwt_extended import get_jwt,jwt_required


# lets create blueprint for artist.
blp = Blueprint("Artist",__name__,description="Operation on Artists",url_prefix="/artists")



@blp.route("/")
class Artists(MethodView):
    # lets get artist and there songs
    @blp.response(200,ArtistandSongs)
    def get(self):
        # lets write query to get artist and there songs
        artists = ArtistModel.find_all()
        
        if not artists:
            abort(400, message = "can not find artists")
        
        return [artist.json() for artist in artists]
    
    # now lets add artist to database.
    @jwt_required(fresh=True)
    @blp.response(201,ArtistandSongs)
    @blp.arguments(AddArtistSchema)
    def post(self,artist_data,name):
        
        # lets get jwt_token payload
        jwt_data = get_jwt()
        
        # lets see token is access token and role is admin
        if jwt_data["token_type"] !="access" or jwt_data["role"] != "admin":
            abort(400,message="refresh token can not be used.")
            
        # lets see first if artist with same name exist
        name = artist_data["name"]
        artist = ArtistModel.find_artist_by_name(name)
        
        if artist:
            abort(400,message = f"artist with same {name} already exist.")
            
        artist_details = ArtistModel(
            name = artist_data["name"],
            birth_date = datetime.strptime(artist_data["birth_date"],"%d-%m-%Y"),
            description = artist_data["description"]
        )
        
        artist_details.add_data()
        
        return artist_details.json()
    
    

# now lets get specific
@blp.route("/<string:name>")
class Artist(MethodView):
    # lets get artist by specific name
    @blp.response(200,ArtistandSongs)
    def get(self,name):
        # lets get artist by name
        artist_by_id = ArtistModel.find_artist_by_name(name)
        
        if not artist_by_id:
            abort(400,message=f"can not find artist with {name}.")
            
        return artist_by_id.json()
    
    #lets update rtist_details
    @jwt_required(fresh=True)
    @blp.arguments(UpdateArtistDetails)
    @blp.response(201,ArtistandSongs)
    def put(self,name,artist_data):
        # lets get jwt_token payload
        jwt_data = get_jwt()
        
        # lets see token is access token and role is admin
        if jwt_data["token_type"] !="access" or jwt_data["role"] != "admin":
            abort(400,message="refresh token can not be used.")
        
        # lets see if artist with name exist or not.
        artist = ArtistModel.find_artist_by_name(name)
        
        if not artist:
            abort(400,message = f"artist with {name} do not exist.")
            
        if artist_data["name"]:
            artist.name = artist_data["name"]
            
        if artist_data["birth_date"]:
            artist.birth_date = datetime.strptime(artist_data["birth_date"],"%d-%m-%Y")
            
        if artist_data["description"]:
            artist.description = artist_data["description"]
            

        artist.add_data()
        
        return artist.json()
    

    # HTTP method to delete artist
    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self,name):
        # lets get jwt_token payload
        jwt_data = get_jwt()
        
        # lets see token is access token and role is admin
        if jwt_data["token_type"] !="access" or jwt_data["role"] != "admin":
            abort(400,message="refresh token can not be used.")
            
        # lets get delete query
        artist = ArtistModel.find_artist_by_name(name)
        
        if not artist:
            abort(400,message=f"can not find user with name {name}.")
        
        artist.delete_data()
        
        return {
            "status":"succesful",
            "message":f"deleted artist with name {name}.",
            "status_code":201
        }