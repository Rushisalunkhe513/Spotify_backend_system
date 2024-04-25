from db import db
from datetime import datetime


# lets create artist table.
class ArtistModel(db.Model):
    __tablename__  = "artists"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False)
    birth_date = db.Column(db.DateTime,nullable=True)
    description = db.Column(db.String,nullable=False,default="NA")
    
    
    songs = db.relationship(
        "ArtistModel",
        back_populates = "artist_details",
        cascade = "all,delete",
        lazy="joined"
    )
    
    albums = db.relationship(
        "AlbumModel",
        back_populates = "artist",
        cascade = "all,delete",
        lazy = "joined"
    )
    
    
    # lets modify response
    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "birth_data":self.birth_date,
            "artist_description":self.description,
            "songs":[song.json() for song in self.songs],
            "albums":[album.json() for album in self.albums]
        }
        
    # now lets find artist by name
    @classmethod
    def find_artist_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
    
    
    # lets get all list of artists
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    # lets add and commit data to database.
    def add_data(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
        
    # lets delete and commit data
    def delete_data(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()