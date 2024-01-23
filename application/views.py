from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
# from werkzeug.security import check_password_hash
from flask_restful import marshal, fields
import flask_excel as excel
from flask_security import login_user, logout_user
from celery.result import AsyncResult
from .tasks import create_resource_csv
from .models import User, db, StudyResource
from .sec import datastore
from flask_security import verify_password
from flask_security import hash_password


@app.post('/user-login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "email not provided"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User Not Found"}), 404
    if verify_password(data.get('password'), user.password):
        login_user(user)
        return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})
    else:
        return jsonify({"message": "Wrong Password"}), 400
@app.get('/user-logout')
def user_logout():
    logout_user()
    return jsonify({"message": "Logged Out"}), 200

@app.get('/')
def home():
    return render_template("index.html")


@app.get('/admin')
@auth_required("token")
@roles_required("admin")
def admin():
    return "Hello Admin"


@app.get('/activate/inst/<int:inst_id>')
@auth_required("token")
@roles_required("admin")
def activate_instructor(inst_id):
    instructor = User.query.get(inst_id)
    if not instructor or "inst" not in instructor.roles:
        return jsonify({"message": "Instructor not found"}), 404

    instructor.active = True
    db.session.commit()
    return jsonify({"message": "User Activated"})


    
@app.post('/user-register')
def user_register():
    data = request.get_json()
    email = data.get('email')
    if app.security.datastore.find_user(email=email):
        return jsonify({'message': 'Email already registered'}), 400

    # Create a new user
    app.security.datastore.find_or_create_role(
        name="stud", description="Stud has some restricted privileges"
    )
    db.session.commit()
    app.security.datastore.create_user(email=email,password=hash_password(data.get('password')), roles=["stud"])
    db.session.commit()
    return jsonify({"message": "User Created"}), 201

@app.post('/user-creator')
def user_creator():
    data = request.get_json()
    email = data.get('email')
    if app.security.datastore.find_user(email=email):
        return jsonify({'message': 'Email already registered'}), 400

    # Create a new user
    app.security.datastore.find_or_create_role(
        name="creator", description="creator is able to add songs"
    )
    db.session.commit()
    app.security.datastore.create_user(email=email,password=hash_password(data.get('password')), roles=["creator"])
    db.session.commit()
    return jsonify({"message": "User Created"}), 201


user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "active": fields.Boolean
}


@app.get('/users')
@auth_required("token")
@roles_required("admin")
def all_users():
    users = User.query.all()
    if len(users) == 0:
        return jsonify({"message": "No User Found"}), 404
    return marshal(users, user_fields)


@app.get('/study-resource/<int:id>/approve')
@auth_required("token")
@roles_required("inst")
def resource(id):
    study_resource = StudyResource.query.get(id)
    if not study_resource:
        return jsonify({"message": "Resource Not found"}), 404
    study_resource.is_approved = True
    db.session.commit()
    return jsonify({"message": "Aproved"})


@app.get('/download-csv')
def download_csv():
    task = create_resource_csv.delay()
    return jsonify({"task-id": task.id})


@app.get('/get-csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 404


