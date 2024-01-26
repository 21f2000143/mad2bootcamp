from celery import shared_task
from .models import StudyResource
from .mail_service import send_message
from .models import User, Role
from jinja2 import Template
from flask_sse import sse
import csv

@shared_task(ignore_result=False)
def create_resource_csv():

    header = ["topic", "description"]
    
    with open('test.csv', 'w', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        stud_res = StudyResource.query.with_entities(
            StudyResource.topic, StudyResource.description).all()
        print(stud_res)
        for res in stud_res:
            csvwriter.writerow([
                res.topic,
                res.description
            ])
    return "OK"

@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    sse.publish({"message": "Monthly Report sent"},type='user')
    users = User.query.filter(User.roles.any(Role.name == 'admin')).all()
    for user in users:
        with open('test.html', 'r') as f:
            template = Template(f.read())
            send_message(user.email, subject,
                         template.render(email=user.email))
    return "OK"
