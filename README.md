## Note-making project
To get started with the project, first clone the repository, and create a virtual environment.
```
python -m virtualenv venv
venv\scripts\activate
```
Once the virtual environment is up and running, install all the requirements
```
pip install -r requirements.txt
```
To add the models to your database,
```
python manage.py makemigrations
python manage.py migrate
```
You can also create a superuser, to see all the models, by-:
```
python manage.py createsuperuser
```
To start the server,

```
python manage.py runserver
```
Navigate to the localhost, where you will find all routes associated with the project.
<br>
<br>
Now, to register a new user, head to /signup, make sure that the media-type is set to application/json, and in the content box paste your details, example -:
```
{
    "username" : "test",
    "email": "test@abc.com",
    "password": "test123"
}
```
To login, head to /login and pass your username and password
<br><br>
For creating a note, head to /notes/create, and in the content box pass your title and content details
```
{
    "title" : "title of your note",
    "content" : "content of the note"
}
```
When a note is created, you will receive its id in the output message, so you can fetch the note again using that id, by heading to /notes/{id}. You can also update the note here.
<br><br>
To share a note, head to /notes/share and along with the title and content, also pass a shared_with field, which is a list containing usernames of all users with which you want to share the note
```
{
    "title" : "title of your note",
    "content" : "content of the note",
    "shared_with" : ['user1']
}
```
To get the version-history of the note, head to /notes/version-history/{id}
