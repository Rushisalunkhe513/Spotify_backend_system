from db import db

# lets declare songs table
from models.song_details import SongDetails

class Songs(db.Model):
    __tablename__="songs"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_name=db.Column(db.String,nullable=False)
    
    category_id = db.Column(db.Integer,db.ForeignKey("music_categories.id"),nullable=False)
    
    song_details = db.relationship(
        "SongDetails",
        back_populates="song",
        cascade = "all,delete"
    )
    
    category = db.relationship(
        "MusicCategories",
        back_populates="songs",
        # lazy="joined" this will  load parent and child class together whenver parent class is called.
    )
    
    
    # now lets serialize for
    def json(self):
        return {
            "id":self.id,
            "song_name":self.song_name,
            "category_id":self.category_id,
            "song_details":[detail.json() for detail in self.song_details] # this will get ong_details data from song.
        }
        
    # find all songs
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    # get songs by name
    @classmethod
    def find_song_by_name(cls,name):
        return cls.query.filter_by(song_name=name).first()
    
    # lets check if song exist with name and same artist
    @classmethod
    def check_song(cls,name,artist): # artist is in song_details column so lets check
        return cls.query.join(SongDetails).filter_by(SongDetails.artist == artist and cls.song_name == name).first() # here we are joining table of relationa table to see artist with same name with song_name exixt.
    
    
    # lets write function to add data to class
    def add_data(self):
        db.session.add(self)
        db.session.commit()
        
    # lets delete data from table
    def delete_data(self):
        db.session.delete()
        db.session.commit()