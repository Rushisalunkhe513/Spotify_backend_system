from db import db



# lets declare table to create user playlist.

class UserPlaylistModel(db.Model):
    __tablename__ = "users_playlists"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) # primary_key of table
    name = db.Column(db.String,nullable=False) # name of playlist
    
    # lets relate user_playlist with user by its id.
    
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    
    user = db.relationship(
        "UserModel",
        back_populates = "user_playlists"
    )
    
    playlist_songs = db.relationship(
        "PlaylistSongsModel",
        back_populates = "playlist",
        lazy="joined",
        cascade="all,delete"
    )
    
    
    # lets serialize playlist_data
    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "user_id":self.user_id,
            "playlist_songs":[playlist_song.json() for playlist_song in self.playlist_songs]
        }
    
    
     # lets write query to get all playlist of user by user_id
    @classmethod
    def get_all_playlist(cls,user_id):
        return cls.query.filter_by(user_id = user_id).all()
    
    # lets get playlist by name
    @classmethod
    def get_playlist_by_name(cls,name):
        return cls.query.filter_by(name = name).first()
    
    # save database to data by add,commit,close
    def save_data(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
        
    # now lets delete data and commit and close session
    def delete_data(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()