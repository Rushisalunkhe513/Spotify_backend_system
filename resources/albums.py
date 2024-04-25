from flask_smorest import Blueprint,abort

from flask.views import MethodView

from models.album import AlbumModel

from schema import AddAlbum,ShowAlbum,AddedAlbum,UpdateAlbum,UpdatedAlbum

blp = Blueprint("albums",__name__,description = "Operation on albums",url_prefix = "/albums")


# lets add route to access albums.
@blp.route("/")
class Albums(MethodView):
    # lets write HTTP get method to get all albums.
    @blp.response(200,ShowAlbum)
    def get(self):
        # lets get all albums
        albums = AlbumModel.find_all()
        
        if not albums:
            abort(400,message = "can not find albums.")
        
        return [album.json() for album  in albums]
    
    # lets write post method to add new album
    @blp.arguments(AddAlbum)
    @blp.response(201,AddedAlbum)
    def post(self,album_data):
        # lets check album to same artist is already in database or not.
        
        album = AlbumModel.check_album_artist(album_data["name"],album_data["artist_id"])
        
        if album:
            abort (400,message = "album with same name to same artist already exist.")
            
        new_album = AlbumModel(
            name = album_data["name"],
            artist_id  =album_data["artist_id"]
        )
            
        # lets add album to database
        
        new_album.save_data()
        
        return new_album.json()
    
    
# now lets add endpoint to get artist albums
@blp.route("/<int:artist_id>")
class ArtistAlbum(MethodView):
    # lets get all artist albums
    @blp.response(200,ShowAlbum)
    def get(self,artist_id):
        # lets get album by artist
        
        artist_albums = AlbumModel.find_all_artist_albums(artist_id)
        
        if not artist_albums:
            abort(400, message = f"albums for artist with id {artist_id} do not exist.")
            
        
        return [album.json() for album in artist_albums]
    
    
# lets write endpoint to get albums by name
@blp.route("/<string:album_name>")
class AlbumName(MethodView):
    # lets get album by name
    @blp.response(200,ShowAlbum)
    def get(self,album_name):
        # lets get album by name.
        
        album_name = AlbumModel.find_albums_by_name(album_name)
        
        if not album_name:
            abort(400,message = f"album with name {album_name} is not exist.")
        
        
        return album_name.json()
    
    # lets update the album by put method
    @blp.arguments(UpdateAlbum)
    @blp.response(201,UpdatedAlbum)
    def put(self,name,album_data):
        # lets check album with name exist.
        album = AlbumModel.find_albums_by_name(name)
        
        if not album:
            abort(400,message = f"album with name {name} do not exist.")
            
        if album_data["name"]:
            album.name = album_data["name"]
        
        if album_data["artist_id"]:
            album.artist_id = album_data["artist_id"]
            
        # now lets add updated data to database
        
        album.save_data()
        
        return album.json()
    
    
    # lets write delete method.
    @blp.response(204)
    def delete(self,name):
        # lets get album with same name.
        album = AlbumModel.find_albums_by_name(name)
        
        if not album:
            abort(400,message = f"album with name {name} do not exist.")
        
        album.delete_data()
        
        return {
            "status":"successful",
            "message":f"album with name {name} is deleted."
        },204