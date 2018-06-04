FROM python:3
COPY . /opt/
WORKDIR /opt/
RUN pip install -r hirebob/requirements.txt
RUN python hirebob/manage.py makemigrations
RUN python hirebob/manage.py migrate
EXPOSE 8000
#CMD python hirebob/manage.py runserver 0.0.0.0:8000
ENTRYPOINT python hirebob/manage.py runserver 0.0.0.0:8000 
