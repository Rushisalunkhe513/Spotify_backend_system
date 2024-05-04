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