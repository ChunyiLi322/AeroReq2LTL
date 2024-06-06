# Space2LTL web

## About

This is the web project for natural language to logical language. 

It was made using  **Anaconda3**  + **Python** + **Django** and database is **SQLite**.
**Bootstrap** was used for styling.

Install dependencies:
```bash
$ pip install -r requirements.txt
```

## How to run

You can run the application from the command line with manage.py.
Go to the root folder of the application.

First, run migrations:
```bash
$ python manage.py migrate
```
Then, run server on port 8000:
```bash
$ python manage.py runserver 8000
```

Go to the web browser and visit `http://localhost:8000/hello`

## Others
You can also load the project in editors such as Pycharm. The following environment needs to be configured：

``
1. File -> setting -> project -> Python Interpreter -> add local Interpreter 
2. Edit Configurations -> django sever
3. download https://github.com/xerial/sqlite-jdbc/releases/download/3.43.0.0/sqlite-jdbc-3.43.0.0.jar
``


## Web controls
![Image](https://github.com/ChunyiLi322/Space2LTL/blob/master/readme_1_img.png)

