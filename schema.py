# now after declaring models lets add schema for data validation

# lets import schem and field from marshmallow

from marshmallow import schema,fields,validate

# normal schema for song
class PlainSongSchema(schema):
    song_name = fields.Str(required=True)
    category_id = fields.Int(required=True)
    artist_name = fields.Str(required=True)
    artist_id = fields.Int(required = True)
    album_id = fields.Int(required=True)
    
# schema for song_details
class PlainSongDetailsSchema(schema):
    song_id = fields.Int(required = True)
    release_date = fields.Str(error_message={"message":"datetime should be in DD-MM-YYYY"})
    lyrics = fields.Str()
    duration = fields.Str()
    
    
# add song to database
class AddSongSchema(PlainSongSchema):
    song_details = fields.List(fields.Nested(PlainSongDetailsSchema))
    
class UpdateSong(schema):
    song_name = fields.Str()
    category_id = fields.Int()
    artist_name = fields.Str()
    artist_id = fields.Int()
    album_id = fields.Int()

class UpdateSongdetails(schema):
    release_date =fields.Str()
    lyrics = fields.Str()
    duration = fields.Str()
    
class UpdateSongandSongDetails(UpdateSong):
    song_details = fields.List(fields.Nested(UpdateSongdetails))
    
    
    
# show songs on board only song name is required.
class SongDetails(schema):
    release_date = fields.DateTime()
    lyrics = fields.Str()
    duration = fields.String()
    
class ShowSong(schema):
    song_name = fields.Str()
    artist_name = fields.Str()
    song_details = fields.List(fields.Nested(SongDetails()))
    

# lets declare schema for albums and albums_songs
class AddAlbum(schema):
    name = fields.Str(required=True)
    artist_id = fields.Int(required = True)
    
class AddedAlbum(schema):
    id = fields.Int()
    name = fields.Str()
    artist_id = fields.Int()
    
class UpdateAlbum(schema):
    name = fields.Str()
    artist_id = fields.Int()
    
class UpdatedAlbum(schema):
    name = fields.Str()
    artist_id = fields.Int()
    album_songs = fields.List(fields.Nested(ShowSong),many=True)
    
# lets get albums and album songs
class ShowAlbum(schema):
    name = fields.Str()
    songs = fields.List(fields.Nested(ShowSong))  

# declare schema for music_catgory

# schema for post request and put request.
class AddMusicCategory(schema):
    id = fields.Int(dump_only=True) # dump_only= need during output not during input data
    category_name = fields.Str(required=True,validate=validate.Length(max=100),error_messages={"required":"category name is required."}) # telling category_name should not be more than 100 letters.
    category_image = fields.Str(required=True,error_messages={"required":"category image is required."})
    """
    we have added error messages to indicate tht category_name is missing or category_image is missing.
    """
    
    
# schema for get HTTP request.
class ShowMusicCategory(schema):
    id = fields.Int()
    category_name = fields.Str()
    category_image = fields.Str()
    songs = fields.List(fields.Nested(ShowSong))
    
    
    

# lets add artist_details
class AddArtistSchema(schema):
    name = fields.Str(required = True)
    birth_date = fields.Str()
    description = fields.Str()
    
# schema for u[dating artist details.
class UpdateArtistDetails(schema):
    name = fields.Str()
    birth_date = fields.Str()
    description = fields.Str() 
    
# lets now get artist and artist all songs
class ArtistandSongs(schema):
    name = fields.Str()
    artist_birth_date = fields.Str()
    description = fields.Str()
    
    artist_songs = fields.List(fields.Nested(ShowSong),many=True)
    albums = fields.List(fields.Nested(ShowAlbum),many = True)
    
    
# lets add user schema
class RegisterUser(schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    mobile_number=fields.Str(required=True)
    password = fields.Str(required=True)
    
    
# lets reset password
class UpdatePassword(schema):
    email = fields.Str(required=True)
    new_password = fields.Str(required=True)
    re_enter_password = fields.Str(required=True)
    
# lets update user_details
class UpdateUserDetails(schema):
    name = fields.Str()
    email = fields.Str()
    mobile_number = fields.Str()
    
    
# login user schema
class LoginUser(schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    
# now lets when we ask for user we should get user_playlist and playlist_songs.

# we will be needing all songs from playlist
class SongToPlaylist(schema):
    song_id = fields.Int(required=True)
    song_name = fields.Str(required=True)
    
class AddPlaylistSongs(schema):
    songs = fields.List(fields.Nested(SongToPlaylist),required = True)
    playlist_id = fields.Int(required=True)

class ShowSongs(schema):
    song_name = fields.Str()
 
class ShowPlaylistSongs(schema):
    song_list = fields.List(fields.Nested(ShowSongs))
    
class AddUserPlaylist(schema):
    name = fields.Str(required=True)
    user_id = fields.Int(required=True)
    
class UpdatePlaylist(schema):
    name = fields.Str()
    user_id = fields.Int()
    
class ShowUserPlaylists(schema):
    name = fields.Str()
    playlists_songs = fields.List(fields.Nested(ShowPlaylistSongs))
    
    
# lets get all user details including user_playlist and playlist songs.
class ShowUserData(schema):
    name = fields.Str()
    email = fields.Str()
    mobile_number = fields.Str()
    playlists = fields.List(fields.Nested(ShowUserPlaylists))
    
    
    
    
# schema for updating admin details
class UpdateAdminDetails(schema):
    name = fields.Str()
    new_password = fields.Str()
    mobile_number = fields.Str()
    
class ShowAdminDetails(schema):
    name = fields.Str()
    mobile_number = fields.Str()
    
class AdminLogin(schema):
    name = fields.Str(required = True)
    password = fields.Str(required = True)
    
class UpdateAdminPassword(schema):
    name = fields.Str(required=True)
    new_password = fields.Str(required=True)
    verify_password = fields.Str(required=True)
    