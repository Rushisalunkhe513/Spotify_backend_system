from db import db
from datetime import datetime


# lets create song_details table.
class SongDetails(db.Model):
    __tablename__="song_details"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    release_date = db.Column(db.DateTime,nullable=False,defult=datetime.now())
    artist = db.Column(db.String,nullable=False,default="N/A")
    duration = db.Column(db.String,nullable=False,default="NA")
    song_id = db.Column(db.Integer,db.ForeignKey("songs.id"),nullable=False)
    
    song = db.relationship(
        "Songs",
        back_populates="song_details"
    )
    
    
    # for working with relational table this is how we can get details of both tables.
    def json(self):
        return {
            "id":self.id,
            "release_date":self.release_date,
            "artist":self.artist,
            "duration":self.duration,
            "song_id":self.song_id
        }