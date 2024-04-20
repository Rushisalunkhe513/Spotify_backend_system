"""
Blueprint class in Flask allows you to organize your Flask application into smaller, 
reusable components. It's particularly useful for structuring larger applications or 
for organizing related routes, views, and resources.
"""
from flask_smorest import Blueprint,abort

# Methodview allows to declare all method related to endpoint in single class.
from flask.views import MethodView 

# calling table from models.
from models import MusicCategories
# we dont need db because opertion we need to perofrm on music_categories are already defined in Musiccategory class.

# for defining error.
from sqlalchemy.exc import SQLAlchemyError 

# we need schema as well
from schema import AddMusicCategory,ShowMusicCategory


"""
music_categories is name of this bluprint,
__name__ name of model,
desription is explaination of work we doing on this blueprint.
added url prefix fpr music_categories bluprint so,whenever we have to acces this endpoints we have to access them through this /music_categories.
"""

blp = Blueprint("music_categories",__name__,description="Operations on Music Categories",url_prefix="/music_categories")


# lets give endpoint

@blp.route("/categories")
class MusicCategory(MethodView):
    # lets write get method with giving output response
    # get method do not need any input
    @blp.response(200,ShowMusicCategory) # schema with status code.
    def get(self):
        categories = MusicCategories.find_all_categories() # this find_all_categories will get all categories from database.
        
        if not categories:
            abort (500, message="categories not found.")
            
        return [category.json() for category in categories] # this will return us jsonify response of all categories.
    
    # post method to add user to database
    # post method needs arguments and response
    @blp.arguments(AddMusicCategory)
    @blp.response(201,ShowMusicCategory)
    def post(self,category_data):
        # lets add data to the catageory table
        # lets check if category with same name exixt or not
        
        category = MusicCategories.find_category_by_name(category_data["category_name"])
        if category:
            abort (500, message = "category with same name exixt.")
            
        add_category = MusicCategories(
            category_name = category_data["category_name"],
            category_image = category_data["category_image"]
        )        
            
            # lets get function from Model class to add data and commit.
        add_category.add_data()
            
        return add_category.json() # single category with json data output
        
        
        
# lets get categiry by its name
@blp.route("/<string:name>") # to access this endpoint we need to use/music_catgory endoint infront of /<string:name> because we have described url_prefix in blueprint.
class MusicCategoryName(MethodView):
    @blp.response(200,ShowMusicCategory)
    def get(self,name):
        category = MusicCategories.find_category_by_name(name)
        
        if not category:
            abort (500, message = f"category with id {id} not found.")
        
        return category.json()
    
    
    # now lets update category by put method.
    @blp.arguments(AddMusicCategory)
    @blp.response(201,ShowMusicCategory)
    def put(self,name,category_data):
        
        # lets see category with id exixt or not
        category = MusicCategories.find_category_by_name(name)
        
        if not category:
            abort (500, message = f"category with name {name} can not be found.")
        
        if category_data:
            category.category_name = category_data["category_name"]  
            category.category_image = category_data["category_image"]
         
         # lets call save_db function to save data
        category.add_data()
        
        return category.json()
    
    # now lets write delete method to delete data from table
    @blp.response(204)
    def delete(self,name):
        # lets find if category exixt or not
        
        category = MusicCategories.find_category_by_name(name)
        
        if not category:
            abort (500, message = f"category with name {name} is not found.")
        
        # lets import function to delete category and commit.
        category.delete_data(name)
        
        return {"status":"success","message":"category has been deleted."}