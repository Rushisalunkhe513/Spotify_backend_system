# now after declaring models lets add schema for data validation

# lets import schem and field from marshmallow

from marshmallow import schema,fields,validate



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
    
    