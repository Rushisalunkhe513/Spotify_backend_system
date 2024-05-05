from db import db



# lets create admin table

class AdminModel(db.Model):
    __tablename__ = "admins"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False)
    password = db.Column(db.String(12),nullable=False)
    mobile_number = db.Column(db.String,nullable=False)
    
    
    
    # lets get json data
    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "mobile_number":self.mobile_number
        }
        
    # lets write methods to get user by id.
    @classmethod
    def get_admin_data_by_name(cls,name):
        return cls.query.filter_by(name = name).first()
    
    # methid for adding data to database.
    def add_data(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
        
    # methid for deleting data from database.
    def delete_data(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()