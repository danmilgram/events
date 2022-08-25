# API events - Plataforma.IO pre assessment

API Endpints are RESTFull, 

Create ROOM : POST /rooms/
Delete ROOM : DELETE /rooms/{room_id}/

List Public EVENTS: GET /events/
Create EVENT: POST /events/

Create PARTICIPANT (Join EVENT): POST /participants/
Delete PARTICIPANT (Abandon EVENT): DELETE /participants/ 

-----------------------------------------

# How to INSTALL DEPENDENCIES and RUN

1. # Create a virtual environment 
    python3 -m venv env
2. # Activate virtual environment
    source env/bin/activate  
3. # Install requirements
    pip install django
    pip install djangorestframework
    pip install django_extensions

4. # Create Django Rest Framework superuser
    python manage.py createsuperuser --email admin@example.com --username admin

5. # RUN API
    python manage.py runserver

6. # SEE API DOCS
    go to http://127.0.0.1:8000/ , login with superuser, create users(bussiness or customers) and manually test the endpoints

7. # HAVE FUN :)

-----------------------------------------

# How to RUN UNIT TESTS
    python manage.py test api/tests






