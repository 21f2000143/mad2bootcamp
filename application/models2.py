from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db=SQLAlchemy()
# def CreateDBApp(app):
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#     return db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    isblocked = db.Column(db.Integer)
    playlists = db.relationship('Playlist', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    songs = db.relationship('Song', backref='creator', lazy=True)
    albums = db.relationship('Album', backref='creator', lazy=True)
    flagged_contents = db.relationship('FlaggedContent', backref='user', lazy=True)

class Playlist(db.Model):
    __tablename__ = 'playlist'
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.TIMESTAMP,
        server_default=db.text("(CURRENT_TIMESTAMP)"),
        nullable=False
    )
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    playlist_songs = db.relationship('Song', secondary='playlistsong')

class PlaylistSong(db.Model):
    __tablename__ = 'playlistsong'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.playlist_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'))

class Song(db.Model):
    __tablename__ = 'song'
    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    created = db.Column(
        db.TIMESTAMP,
        server_default=db.text("(CURRENT_TIMESTAMP)"),
        nullable=False
    )
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String, nullable=False)
    audio_data = db.Column(db.BLOB)
    audio_type = db.Column(db.String)
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))
    lyrics = db.Column(db.TEXT)
    likes = db.relationship('Like', backref='song', lazy=True)
    comments = db.relationship('Comment', backref='song', lazy=True)
    flagged_contents = db.relationship('FlaggedContent', backref='song', lazy=True)

class Album(db.Model):
    __tablename__ = 'album'
    album_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(
        db.TIMESTAMP,
        server_default=db.text("(CURRENT_TIMESTAMP)"),
        nullable=False
    )
    songs = db.relationship('Song', backref='album', lazy=True)

class Like(db.Model):
    __tablename__ = 'like'
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'))
    rate = db.Column(db.Integer)

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'))
    content = db.Column(db.TEXT)

class FlaggedContent(db.Model):
    __tablename__ = 'flaggedcontent'
    flag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'))
    type = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reason = db.Column(db.TEXT)
