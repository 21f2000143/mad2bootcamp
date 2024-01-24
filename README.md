# study_resource_management
App which helps students to manage study material

# creating venv cmd
python3 -m venv .env

# for listing out frameworks on the requirements.txt
pip freeze > requirements.txt

# to run the app
python3 main.py
# to stop the app
ctrl + c

# starting the redis-server
sudo service redis-server start

# stop the redis-server
sudo service redis-server stop

# to install redis for windows
https://redis.io/docs/install/install-redis/install-redis-on-windows/

# to install mailhog, follow the link
https://github.com/mailhog/MailHog

# for running the mailhog app on wsl, use this command
~/go/bin/MailHog

# to start the celery workers on separate process, run this command
celery -A main.celery_app worker -l info

# to start the celery beat/timer on separate process, run this command
celery -A main.celery_app beat --max-interval 1 -l info