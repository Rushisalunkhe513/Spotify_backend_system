# now after declaring models lets add schema for data validation

# lets import schem and field from marshmallow

from marshmallow import schema,fields



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
    
    