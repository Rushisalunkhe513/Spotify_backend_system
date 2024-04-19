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
        back_populates="songs"
    )
    
    
    # now lets serialize for
    def json(self):
        return {
            "id":self.id,
            "song_name":self.song_name,
            "category_id":self.category_id
        }