# GroceryStore

This is my first django project with simple functionality, which I am going to optimize occaisionally.

GroceryStore deployed on [beget.com](http://beget.com/). 


You could view the deployment at [App domain](http://shilov2z.beget.tech) until April 8.

**!NOTICE! Images could be load incorrectly, but it is because of the server.**

***Usefull urls:***
  * Home page ```'/'```
  * Admin panel ```'admin/'```
  * API ```'api/v1/'```

***How to run?***
  * *Without docker*:
     1. ```python grocerystore/manage.py runserver```
     2. Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
  * *Using docker*:
     1. ```docker-compose up -- build -d```
     2. ```docker exec -ti web poetry run python grocerystore/manage.py migrate```
     3. Go to [http://0.0.0.0:9000/](http://0.0.0.0:9000/)
  
