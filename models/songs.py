from db import db

# lets declare songs table


class Songs(db.Model):
    __tablename__="songs"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_name=db.Column(db.String,nullble=False)
    
    category_id = db.Column(db.Integer,db.ForeignKey("music_categories.id"),nullable=False)
    
    song_details = db.relationship(
        "SongDetails",
        back_populates="song"
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