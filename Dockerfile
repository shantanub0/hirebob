FROM python:3
COPY ./hirebob/ /opt/
WORKDIR /opt/
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8000
#CMD python manage.py runserver 0.0.0.0:8000
ENTRYPOINT python manage.py runserver 0.0.0.0:8000 
