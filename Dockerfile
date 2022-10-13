FROM python:3.8-slim-buster

WORKDIR /opt/apps

ADD . /opt/apps

RUN pip install -r requirements.txt

CMD ["python","mainapp.py"]