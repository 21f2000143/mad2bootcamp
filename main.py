from flask import Flask
from flask_security import Security
from application.models import *
from config import DevelopmentConfig
from application.resources import api
from application.sec import datastore
from application.worker import celery_init_app
import flask_excel as excel
from celery.schedules import crontab
from application.tasks import daily_reminder, create_resource_csv
from flask_security import hash_password
from application.instances import cache
from flask_sse import sse
from celery.result import AsyncResult


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    api.init_app(app)
    excel.init_excel(app)
    app.security = Security(app, datastore)
    with app.app_context():
        app.security.datastore.find_or_create_role(name="admin", description="Admin")
        db.session.commit()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com",
            password=hash_password("password"), roles=["admin"])
        db.session.commit()
    cache.init_app(app)
    with app.app_context():
        import application.views

    return app


app = create_app()
celery_app = celery_init_app(app)
app.config['REDIS_URL'] = 'redis://localhost:6379'
celery_app.conf.update(
    broker_url = 'redis://localhost:6379/0',
    result_backend = 'redis://localhost:6379/1',
    timezone = 'Asia/Kolkata',
    broker_connection_retry_on_startup=True
)
celery_app.conf.timezone = 'Asia/Kolkata' 

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/1'),
        daily_reminder.s(),
    )

app.register_blueprint(sse, url_prefix='/stream')

if __name__ == '__main__':
    app.run(debug=True)
