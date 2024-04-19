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
    release_date = fields.DateTime()
    artist= fields.Str(required=True)
    duration = fields.Str()
    
    
# add song to database
class AddSongSchema(PlainSongSchema):
    song_details = fields.List(fields.Nested(PlainSongDetailsSchema),required=True)
    
# show songs on board only song name is required.
class ShowSong(schema):
    song_name = fields.Str()
    
# now show complete song details
# song_details to show

class SongDetails(schema):
    artist = fields.Str()
    release_date = fields.DateTime()
    duration = fields.String()


class ShowSongandDetails(schema):
    song_name = fields.Str()
    song_details = fields.List(fields.Nested(SongDetails))
    

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
    songs = fields.List(fields.Nested(ShowSongandDetails))
    
    
    
