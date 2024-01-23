from flask_restful import Resource, Api, reqparse, fields, marshal
from flask_security import auth_required, roles_required, current_user
from flask import jsonify
from sqlalchemy import or_
from .models import *
from .instances import cache


api = Api(prefix='/api')

parser = reqparse.RequestParser()
parser.add_argument('topic', type=str,
                    help='Topic is required should be a string', required=True)
parser.add_argument('description', type=str,
                    help='Description is required and should be a string', required=True)
parser.add_argument('resource_link', type=str,
                    help='Resource Link is required and should be a string', required=True)

album_parser = reqparse.RequestParser()
album_parser.add_argument('title', type=str,
                    help='title is required should be a string', required=True)
album_parser.add_argument('genre', type=str,
                    help='genre is required and should be a string', required=True)


class Creator(fields.Raw):
    def format(self, user):
        return user.email


study_material_fields = {
    'id': fields.Integer,
    'topic':   fields.String,
    'description':  fields.String,
    'resource_link': fields.String,
    'is_approved': fields.Boolean,
    'creator': Creator
}


class StudyMaterial(Resource):
    @auth_required("token")
    @cache.cached(timeout=50)
    def get(self):
        if "inst" in current_user.roles:
            study_resources = StudyResource.query.all()
        else:
            study_resources = StudyResource.query.filter(
                or_(StudyResource.is_approved == True, StudyResource.creator == current_user)).all()
        if len(study_resources) > 0:
            return marshal(study_resources, study_material_fields)
        else:
            return {"message": "No Resourse Found"}, 404

    @auth_required("token")
    @roles_required("stud")
    def post(self):
        args = parser.parse_args()
        study_resource = StudyResource(topic=args.get("topic"), description=args.get(
            "description"), resource_link=args.get("resource_link"), creator_id=current_user.id)
        db.session.add(study_resource)
        db.session.commit()
        return {"message": "Study Resource Created"}
class AllAlbum(Resource):
    @auth_required("token")
    @cache.cached(timeout=50)
    def get(self):
        albums = Album.query.all()
        albums_data = []
        for album in albums:
            album_data = {
                'album_id': album.album_id,
                'title': album.title,
                'genre': album.genre,
                'creator_id': album.creator_id,
                'created': album.created.strftime("%Y-%m-%d %H:%M:%S"),
            }
            albums_data.append(album_data)
        return albums_data, 200
    # @auth_required("token")
    # @roles_required("creator")
    def post(self):
        args = album_parser.parse_args()
        title = args.get('title')
        genre = args.get('genre')
        if not title or not genre:
            return {"message": "Title and Genre are required"}, 400
        if Album.query.filter_by(title=title).first():
            return {"message": "Album with this title already exists"}, 400
        
        album = Album(title=title, genre=genre, creator_id=current_user.id)
        db.session.add(album)
        db.session.commit()
        return {"message": "Album Created"}, 201
    
    # @auth_required("token")
    # @roles_required("creator")
    def put(self, album_id):
        album = Album.query.get(album_id)
        if not album:
            return {"message": "Album not found"}, 404
        else:
            args = album_parser.parse_args()
            title = args.get('title')
            genre = args.get('genre')
            album.title = title
            album.genre = genre
            db.session.commit()
            return {"message": "Album Updated"}, 200
        
    @auth_required("token")
    @roles_required("creator")
    def delete(self, album_id):
        album = Album.query.get(album_id)
        if not album:
            return {"message": "Album not found"}, 404
        else:
            db.session.delete(album)
            db.session.commit()
            return {"message": "Album Deleted"}, 200

api.add_resource(StudyMaterial, '/study_material')
api.add_resource(AllAlbum, '/album', '/album/<int:album_id>')

