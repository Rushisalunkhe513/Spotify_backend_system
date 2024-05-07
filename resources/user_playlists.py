from flask.views import MethodView

from flask_smorest import Blueprint,abort

from models.user_playlist import UserPlaylistModel
from models.playlist_songs import PlaylistSongsModel

from schema import ShowUserPlaylists,AddUserPlaylist,UpdatePlaylist,AddPlaylistSongs,ShowPlaylistSongs

from db import db

from flask_jwt_extended import jwt_required,get_jwt

# lets add bluprint for user_playlist

blp = Blueprint("user_playlist",__name__,description="Operation on user playlist",url_prefix="/user_playlist")



# now lets add route for getting all user playlists.
@blp.route("/add_playlist")
class UserPlaylist(MethodView):
    # lets add playlist
    @jwt_required(fresh=True)
    @blp.arguments(AddUserPlaylist)
    @blp.response(201,ShowUserPlaylists)
    def post(self,playlist_data):
        
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
        # lets add new playlist
        # but first lets check playlist with same name exist or not.
        # if exist the error
        
        existing_playlist = UserPlaylistModel.get_playlist_by_name(playlist_data["name"])
        
        if existing_playlist:
            abort(400,message="playlist with same name already exist. choose diff name for playlist!.")
            
        new_playlist = UserPlaylistModel(
            name = playlist_data["name"],
            user_id = playlist_data["user_id"],
        )
        
        # now lets add data to database.
        
        new_playlist.save_data()
        
        # now return output
        
        return new_playlist.json()
    
    
# now lets add get playlist by name,update and delete playlist by name.
@blp.route("/<string:playlist_name>")
class PlaylistName(MethodView):
    # HTTP get method to get playlist by name
    @jwt_required(fresh=True)
    @blp.response(200,ShowUserPlaylists)       
    def get(self,playlist_name):
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
            
        # lets get user playlist by name
        user_playlist = UserPlaylistModel.get_playlist_by_name(playlist_name)
        
        if not user_playlist:
            abort(400,message=f"user playlist with name {playlist_name} can not exist.")
            
        # now lets return playlist
        return user_playlist.json()
    
    
    # now lets write HTTP Method to update playlist data.
    @jwt_required(fresh=True)
    @blp.response(201,ShowUserPlaylists)
    @blp.arguments(UpdatePlaylist)
    def put(self,playlist_name,update_playlist_data):
        
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
            
        # lets check for playlist exist.
        playlist_exist = UserPlaylistModel.get_playlist_by_name(playlist_name)
        
        if not playlist_exist:
            abort(400,message="playlist do not exist.")
        
        if update_playlist_data["name"]:
            playlist_exist.name = update_playlist_data["name"]
        else:
            playlist_exist.name = playlist_exist.name
            
        if update_playlist_data["user_id"]:
            playlist_exist.user_id = update_playlist_data["user_id"]
        else:
            playlist_exist.user_id = playlist_exist.user_id
            
        # now lets add updated playlist to database.
        playlist_exist.save_data()
        
        # lets return update playlist data
        return playlist_exist.json()

    
    # lets write http method to delete playlist by name
    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self,playlist_name):
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
            
        # lets get playlist by name
        existing_playlist = UserPlaylistModel.get_playlist_by_name(playlist_name)
        
        if not existing_playlist:
            abort(400,message=f"playlist with name {playlist_name} do not exist.")
            
        # now lets delete playlist.
        
        existing_playlist.delete_data()
        
        # lets return status and status code with message
        
        return {
            "status":"success",
            "message":f"playlist with name {playlist_name} has been deleted."
        }    
        
    
# lets get all users playlist
@blp.route("/<int:user_id>")
class UserPlaylists(MethodView):
    # lets write HTTP method to get all User Playlists
    @jwt_required(fresh=True)
    @blp.response(200,ShowUserPlaylists)
    def get(self,user_id):
        
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
        # lets get all user playlist by user_id
        user_playlists = UserPlaylistModel.get_all_playlist(user_id)
        
        if not user_playlists:
            abort(400,message="user do not have any playlist.")
            
        # now if playlist exist then return playlists
        return [user_playlist.json() for user_playlist in user_playlists]
    
    
# now we need to add songs to playlist
@blp.route("/add_songs/<string:playlist_name>")
class AddSongs(MethodView):
    @jwt_required(fresh=True)
    @blp.response(201, ShowPlaylistSongs)
    @blp.arguments(AddPlaylistSongs)
    def post(self, playlist_name, add_song_data):
        
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
            
        check_playlist = UserPlaylistModel.get_playlist_by_name(playlist_name)
        
        if not check_playlist:
            abort(400, message=f"Playlist does not exist with name {playlist_name}.")
        
        playlist_id = check_playlist.id
        added_songs = []

        for song_details in add_song_data["songs"]:
            song_name = song_details["song_name"]
            song_id = song_details["song_id"]

            playlist_song = PlaylistSongsModel(
                song_name=song_name,
                song_id=song_id,
                playlist_id=playlist_id
            )
            db.session.add(playlist_song)
            added_songs.append(playlist_song)

        db.session.commit()
        return added_songs, 201
            
            
# now lets add endpoint to remove the songs from playlist
@blp.route("/<int:playlist_id>/<string:song_name>")
class RemoveSongPlaylist(MethodView):
    # now lets remove the song from playlist.
    # lets write delete HTTP Method
    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self,playlist_id,song_name):
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
        
        # now we will delete songs from playlist
        playlist_song = PlaylistSongsModel.query.filter_by(playlist_id=playlist_id, song_name=song_name).first()
        
        if not playlist_song:
            abort(404,message=f"song with name {song_name} don not exist.")
        
        # now we have playlist song from playlistsongs
        
        db.session.delete(playlist_song)
        db.session.commit()
        
        # lets return status and message after song has been deleted.
        return {
            "status":"success",
            "message":f"song with name {song_name} and with playlist_id {playlist_id} has been deleted."
        }
            