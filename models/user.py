from db import db


# lets create user model

class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.column(db.String,nullable=False)
    password = db.Column(db.String,nullable = False)
    email = db.Column(db.String,nullable=False,default="N/A")
    mobile_number = db.Column(db.String,nullable=False,default="N/A")
    
    user_playlists = db.relationship(
        "UserPlaylistModel",
        back_populates = "user",
        lazy = "joined",
        cascade = "all,delete"
    )
    
    
    
    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "mobile_number":self.mobile_number,
            "email":self.email,
            "user_playlists":[user_playlist.json() for user_playlist in self.user_playlists]
        }
        
    # lets get all user
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    # lets get user by name 
    @classmethod
    def find_user_by_email(cls,email):
        return cls.query.filter_by(email = email).first()
    
    # lets find user by its mobile number
    @classmethod
    def get_user_by_mobile_number(cls,mobile_number):
        return cls.query.filter_by(mobile_number = mobile_number).first()
    
    # now add data to database
    def save_data(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
        
    # lets write the methid to delete data
    def delete_data(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()