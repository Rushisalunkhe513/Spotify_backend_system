from flask_smorest import Blueprint,abort

from flask.views import MethodView

from models import Songs,SongDetails

from schema import ShowSong,AddSongSchema,UpdateSongandSongDetails

from db import db

from datetime import datetime

from flask import request

from flask_jwt_extended import jwt_required,get_jwt



blp  = Blueprint("songs",__name__,description="Operation on songs",url_prefix="/songs")




# lets list all songs
@blp.route("/")
class GetAllSongs(MethodView):
    # lets get proper response
    @blp.response(200,ShowSong)
    def get(self):
        
        # lets get all songs and there song details from table
        songs = Songs.find_all()
        
        if not songs:
            abort(500, message = "songs not found.")
        
        return [song.json() for song in songs] # json formated data
    
    # lets add song and song details
    @jwt_required(fresh=True)
    @blp.arguments(AddSongSchema)
    @blp.response(201,ShowSong)
    def post(self,song_data):
        # lets get jwt_token payload
        jwt_data = get_jwt()
        
        # lets see token is access token and role is admin
        if jwt_data["token_type"] !="access" or jwt_data["role"] != "admin":
            abort(400,message="refresh token can not be used.")
        
        # lets add song,
        
        check_song = Songs.check_song(song_data["song_name"],song_data["artist_name"])
        
        if song_data["song_details"]["lyrics"]:
            lyrics = song_data["song_details"]["lyrics"]
        else:
            lyrics = None
        
        if check_song:
            abort (500, message = f"song with same name and artist already exixt.")
            
        # if not then lets add data to table
        
        song = Songs(
            song_name = song_data["song_name"],
            category_id = song_data["category_id"],
            artist_name = song_data["artist_name"],
            artist_id = song_data["artist_id"]
        )
        db.session.add(song)
        # lets add this song and genrate its id to add in song_details.
        song_details = SongDetails(
            release_date =  datetime.strptime(song_data["song_details"]["release_date"],"%d-%m-%Y"),# we need to add song in DateTime type with %d-%m-%Y format
            lyrics = lyrics,
            duration = song_data["song_details"]["duration"],
            song_id = song.id
        )
        
        
        db.session.add(song_details)
        db.session.commit()
        
        return song.json()
    
# now lets write search endpoint to get all songs with possible like name
@blp.route("/search-songs")
class SearchSong(MethodView):
    # get method with ShowSong Schema
    @blp.response(200,ShowSong)
    def get(self):
        # lets write query to get song by name.
        
        search_query = request.args.get("search_query") # this will help to get query from site address.
        
        search_songs_by_query = Songs.query.filter(Songs.song_name.ilike(f"%{search_query}%")).all()
        
        return [song.json() for song in search_songs_by_query]
    
    

@blp.route("/<string:name>")
class SongByName(MethodView):
    # lets get response
    @blp.response(200,ShowSong)
    def get(self,name):
        # lets get song by name
        song = Songs.find_song_by_name(name)
        
        if not song:
            abort (400,message = f"song with {name} can not be found.")
        
        return song.json()
    
    #lets write put method to update song and its details
    @jwt_required(fresh=True)
    @blp.arguments(UpdateSongandSongDetails)
    @blp.response(201,ShowSong)
    def put(self,name,song_data):
        # lets get jwt_token payload
        jwt_data = get_jwt()
        
        # lets see token is access token and role is admin
        if jwt_data["token_type"] !="access" or jwt_data["role"] != "admin":
            abort(400,message="refresh token can not be used.")
        
        # lets get song by its name.
        song = Songs.find_song_by_name(name)
        
        if not song:
            abort (400,message = f"song with name {name} can not be found")
            
        if song_data:
            song.song_name = song_data["song_name"]
            song.category_id = song_data["category_id"]
            song.artist_id = song_data["artist_id"]
            song.artist_name = song_data["artist_name"]
            
        # now lets get song details from song for updating the data in table
        song_details = song.song_details
        
        for song_details_data in song_data["song_details"]:
            if song_details_data.get("release_date"):
                song_details.release_date = datetime.strptime(song_details_data["release_date"], "%d-%m-%Y")
            if song_details_data.get("lyrics"):
                song_details.lyrics = song_details_data["lyrics"]
            if song_details_data.get("duration"):
                song_details.duration = song_details_data["duration"]
                
            db.session.add(song_details)
            
        db.session.add(song)
        db.session.commit()
        
        return song.json(),201
    
    
    # lets write delete method to delete song with id
    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self,name):
        # lets get jwt_token payload
        jwt_data = get_jwt()
        
        # lets see token is access token and role is admin
        if jwt_data["token_type"] !="access" or jwt_data["role"] != "admin":
            abort(400,message="refresh token can not be used.")
        
        # lets get song by name
        
        song = Songs.find_song_by_name(name)
        
        if not song:
            abort (400, message = f"can not find song with name {name}.")
        
        song.delete_data()
        
        return {"status":"success","message":f"deleted the song with name {name}."},201
            
            
                
        
        
            
        
            
        