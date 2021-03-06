# SIA App Challenge Backend

Setting Up
----------
1. Clone this repo.
2. Create a virtual environment for this project. To do this, install `virtualenvwrapper` and type `$ mkvirtualenv env` into the terminal.
    To enter the environment, type `$ workon env`
    To exit the environment, type `$ deactivate`
3. Intall the dependencies in `requirements.txt`
    ```
    (env) $ pip install -r requirements.txt
    ```
QED

Database Setup
---------
1. Install `mysql` and start the server.
    (For ubuntu)
    To check MySQL server status: `$ sudo service mysql status`
    To stop MySQL server: `$ sudo service mysql stop`
    To start MySQL server: `$ sudo service mysql start`
2. Open mysql from the client-side
    ```
    $ mysql -u root -p
    ```
3. Create the test database and user. The details (including password) are
defined in `sia_backend/settings.py`, because test, so just paste the following:
    ```
    CREATE DATABASE test_db;
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'SIA_passw0rd';
    GRANT ALL PRIVILEGES ON test_db.* TO 'test'@'localhost';
    FLUSH PRIVILEGES;
    ```
4. Check, sync and migrate the database.
    ```
    (env) $ python manage.py check
    (env) $ python manage.py migrate
    ```
5. Also, set up an admin account.
    ```
    (env) $ python manage.py createsuperuser
    ```
6. Can test if it works with `(env) $ python manage.py test`, but this will
involve creating and deleting a test database, which the `test` user might not
have rights to. If test fails, grant the dude all privileges(including creation
and deletion), using your root account on the mysql client or smth.
    ```
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'test'@'localhost';
    mysql> FLUSH PRIVILEGES;
    ```
7. ggez.

Server Setup
---------
```
(env) $ python manage.py runserver
```

APIs
---------

`GET /users`                    Get all profiles

`GET /user/<id>`                Get planner/supervisor's profile

`GET /defects`                  Get all defects

`GET /techs`                    Get all technicians

`GET/PUT/PATCH /tech/<technician-id>`     Get single technician's profile

`GET/PUT/PATCH/DELETE /defect/<defect-id>`       Get single defect detail

```
GET: For getting single technician or defect
PATCH: For editing same level fields such as `closed`, `priority`, `description` (send through form)
```

`GET /techdefects?id=<id>`      Get defects under technician (identified by id)

`GET /techhistory?id=<id>`      Get last 10 completed defects under technician (identified by id)

`POST /createdefect`            Post new defect
```
Form required fields:
header
classCode
category
plane
```

`PUT/DELETE /techassign/<defect-id>`       Add or delete techs assigned to defect (identified by id)
```
Form:
id  (<tech-id>)
```

`PUT/DELETE /update/<defect-id>`       Add or delete update on defect (identified by id)
```
Form:
(if DELETE)
id  (<update-id>)
(if PUT)
author (<user-id>)
details(message)
```

`PUT/DELETE /addsparetodefect/<defect-id>`       Add or delete spares on defect (identified by id)
```
Form:
(if DELETE)
id (<spareDetail-id>)

(if PUT with new spare in defect)
spare (<part id>)
quantity (quantity needed) [optional, default=1]
drawn (True or False) [optional, default=False]
```
