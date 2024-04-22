# now after declaring models lets add schema for data validation

# lets import schem and field from marshmallow

from marshmallow import schema,fields

# lets declare schema for songs

# normal schema for song
class PlainSongSchema(schema):
    song_name = fields.Str(required=True)
    category_id = fields.Int(required=True)
    
# schema for song_details
class PlainSongDetailsSchema(schema):
    song_id = fields.Int(required = True)
    release_date = fields.Str(error_message={"message":"datetime should be in DD-MM-YYYY"})
    artist= fields.Str(required=True)
    lyrics = fields.Str()
    duration = fields.Str()
    
    
# add song to database
class AddSongSchema(PlainSongSchema):
    song_details = fields.List(fields.Nested(PlainSongDetailsSchema))
    
class UpdateSong(schema):
    song_name = fields.Str()
    category_id = fields.Int()

class UpdateSongdetails(schema):
    release_date =fields.Str()
    lyrics = fields.Str()
    artist = fields.Str()
    duration = fields.Str()
    
class UpdateSongandSongDetails(UpdateSong):
    song_details = fields.List(fields.Nested(UpdateSongdetails))
    
    
    
# show songs on board only song name is required.
class SongDetails(schema):
    artist = fields.Str()
    release_date = fields.DateTime()
    lyrics = fields.Str()
    duration = fields.String()
    
class ShowSong(schema):
    song_name = fields.Str()
    song_details = fields.List(fields.Nested(SongDetails()))
    
    

# declare schema for music_catgory

# schema for post request and put request.
class AddMusicCategory(schema):
    id = fields.Int(dump_only=True) # dump_only= need during output not during input data
    category_name = fields.Str(required=True)
    category_image = fields.Str(required=True)
    
    
# schema for get HTTP request.
class ShowMusicCategory(schema):
    id = fields.Int()
    category_name = fields.Str()
    category_image = fields.Str()
    songs = fields.List(fields.Nested(ShowSong))
    
    
    
