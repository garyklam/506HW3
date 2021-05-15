FROM python:slim-buster
MAINTAINER Gary "lam583@uw.edu"
RUN pip install flask flask-wtf email_validator requests flask-login flask-sqlalchemy

COPY hw3 hw3

CMD [ "python", "hw3/hw2.py" ]
