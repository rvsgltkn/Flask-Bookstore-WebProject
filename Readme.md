#### Python & flask_restx Bookstore WebSite and Services Project


### Installation
- python3 -m venv demo-env
- source demo-env/bin/activate
- pip3 install -r requirements.txt

### to run web project
- python manage.py run

- view on browser url : http://127.0.0.1:5000/
    
### to run test cases
- python manage.py test

### restful services
-   http://127.0.0.1:5000/auth/login
-   http://127.0.0.1:5000/auth/logout
-   (GET)http://127.0.0.1:5000/user/
-   (POST)http://127.0.0.1:5000/user/
-   -   email
    -   username
    -   password
-   (GET)http://127.0.0.1:5000/user/"< user id >"
-   (GET)http://127.0.0.1:5000/user/book/
-   (POST)http://127.0.0.1:5000/book/
-   -   name
    -   author
    -   description
-   (GET)http://127.0.0.1:5000/book/"< book id >"




### heroku deployment url info
- https://flask-bookstore-miniproject.herokuapp.com/