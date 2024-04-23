from db import db



# lets declare database table for music categories.
"""
db.Model = used to define table,
table_name = music_categories,
columns---->
1) Id = Primary_key , constraint(Autoincrement)
2) category_name = string type, constraint(nullable,default)
3) category_image = string type, constraint(nullable)
"""
class MusicCategories(db.Model): 
    __tablename__ = "music_categories"  # declaring name of table for music categories.
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    category_name = db.Column(db.String,nullable=False)
    category_image = db.Column(db.String,nullable=False)
    
    songs = db.relationship(
        "Songs",
        back_populates="category",
        cascade = "all,delete"
    )
    
    
    # lets add json serialized function to send data in json format.
    # its actually data we are sending in output format in json so, client can tke data.
    def json(self):
        return {
            "id":self.id,
            "category_name":self.category_name,
            "category_image":self.category_image
        }
        
    # lets perfoem database connection here we need for get,post,put,delete method
    # so when we call class all methods we declare here in this class will be called by name of class and name of methid
    # we are doing this to simplify code in resources.
    # use @classmethod by this we bind methods to class.
    
    @classmethod
    def find_all_categories(cls): # using classmethod so cls comes instead of self.
        return cls.query.all()  # calling all data from this table.
    
    @classmethod
    def find_by_id(cls,id):
        return cls.query.get_or_404(id) # getting data by id
    
    @classmethod
    def find_category_by_name(cls,name):
        return cls.query.filter_by(category_name=name).first() # this will find category by name and fetch first match.
    
    # now lets wriet function to perform database transaction like add,commit,delete
    
    # function to add data and commit
    def add_data(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
        
    # function to delete data and commit
    def delete_data(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()
        