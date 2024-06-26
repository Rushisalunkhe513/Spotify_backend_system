from db import db

# lets declare songs table
from models.song_details import SongDetails

class Songs(db.Model):
    __tablename__="songs"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_name=db.Column(db.String,nullable=False)
    artist_name = db.Column(db.String,nullable= False,default="N/A")
    
    artist_id = db.Column(db.String,db.ForeignKey("artist.id"),nullable=False)
    
    category_id = db.Column(db.Integer,db.ForeignKey("music_categories.id"),nullable=False)
    
    album_id = db.Column(db.Integer,db.ForeignKey("albums.id"),nullable = False)
    
    song_details = db.relationship(
        "SongDetails",
        back_populates="song",
        cascade = "all,delete",
        lazy='joined'
    )
    
    artist_details = db.relationship(
        "ArtistModel",
        back_populates = "songs"
    )
    
    category = db.relationship(
        "MusicCategories",
        back_populates="songs",
        
    )
    
    # song to user_playlist
    playlist_song = db.relationship(
        "PlaylistSongsModel",
        back_populates="song",
        cascade="all,delete"
    )
    
    albums = db.relationship(
        "AlbumModel",
        back_populates = "songs"
    )
    
    
    # now lets serialize for
    def json(self):
        return {
        "id": self.id,
        "song_name": self.song_name,
        "category_id": self.category_id,
        "song_details": [detail.json() for detail in self.song_details]  # this will get song_details data from song.
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
    def check_song(cls,name,artist_name): # artist is in song_details column so lets check
        return cls.query.filter_by(song_name = name,artist_name = artist_name).first() # here we are joining table of relationa table to see artist with same name with song_name exixt.
    
    
    # lets write function to add data to class
    def add_data(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
        
    # lets delete data from table
    def delete_data(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()