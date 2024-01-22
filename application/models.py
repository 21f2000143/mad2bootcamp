from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    study_resource = db.relationship('StudyResource', backref='creator')
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class StudyResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_link = db.Column(db.String, nullable=False)
    is_approved = db.Column(db.Boolean(), default=False)

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
