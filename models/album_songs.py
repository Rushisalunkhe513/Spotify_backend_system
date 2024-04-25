# from db import db



# class AlbumSongs(db.Model):
#     __tablename__ = "albumsongs"
    
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     song_name = db.Column(db.String,nullable = False,default = "N/A")
    
#     album_id = db.Column(db.Integer,db.ForeignKey("albums.id"))
#     song_id = db.Column(db.Integer,db.ForeignKey("songs.id"))
    
    
#     album = db.relationship(
#         "AlbumModel",
#         back_populates = "album_songs"
#     )
    
#     songs = db.relationship(
#         "Songs",
#         back_populates = "album_songs",
#         lazy = "joined"
#     )
    
    
#     # lets get all album_songs
#     @classmethod
#     def all_album_songs(cls):
#         return cls.query.all()
    
#     @classmethod
#     def find_album_song_by_name(cls,song_name):
#         return cls.query.filter_by(song_name = song_name).first()
    
    
#     # lets save and close session
#     def save_data(self):
#         db.session.add(self)
#         db.session.commit()
#         db.session.close()
        
#     # lets delete the album songs
#     def delete_data(self):
#         db.session.delete(self)
#         db.session.commit()
#         db.session.close()