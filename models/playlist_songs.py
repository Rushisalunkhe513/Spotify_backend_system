from db import db


# now lets add playlists songs to playlist
class PlaylistSongsModel(db.Model):
    __tablename__ = "playlist_songs"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_name = db.Column(db.String,nullable=False)
    
    # adding song to the respective playlist
    playlist_id = db.Column(db.Integer,db.ForeignKey("users_playlists.id"),nullable=False)
    
    # lets add song_id as foreign key to
    song_id = db.Column(db.Integer,db.ForeignKey("songs.id"),nullable=False)
    
    
    # relationship with songs
    song = db.relationship(
        "SongModel",
        back_populates="playlist_song"
    )
    
    # relationship with playlist
    playlist = db.relationship(
        "UserPlaylistModel",
        back_populates="playlist_songs"
    )
    
    
    
    
    # now lets serialize reply.
    def json(self):
        return  {
            "id":self.id,
            "song_name":self.song_name,
            "song_id":self.song_id
        }
    
    
    
    