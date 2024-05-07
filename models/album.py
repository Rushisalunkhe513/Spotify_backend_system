from db import db


# lets declare album table with name of album and artist_name,image for album with artist id and artist table with song_details.

class AlbumModel(db.Model):
    __tablename__="albums"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False,default="N/A")
    
    
    artist_id = db.Column(db.Integer,db.ForeignKey("artists.id"))
    
    
    artist = db.relationship(
        "ArtistModel",
        back_populates = "albums"
    )
    
    songs = db.relationship(
        "Songs",
        back_populates="albums",
        lazy = "joined"
    )
    
    
    
    def json(self):
        return {
            "id": self.id,
            "name":self.name,
            "artist_id":self.artist_id,
            "songs":[song.json() for song in self.songs]
        }
        
    
    # getting all albums    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    # lets get albums by album name
    @classmethod
    def find_albums_by_name(cls,name):
        return cls.query.filter_by(name = name).all()  
    
    # lets get all albums by artist _id
    @classmethod
    def find_all_artist_albums(cls,artist_id):
        return cls.query.filter_by(artist_id = artist_id).all()
    
    # check album with same name to artist already exist.
    @classmethod
    def check_album_artist(cls,name,artist_id):
        return cls.query.filter_by(name = name,artist_id = artist_id).first()
    
    # now lets add data to the database and close session
    def save_data(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
        
    # lets delete data and close session
    def delete_data(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()