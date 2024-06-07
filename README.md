# AeroReq2LTL web

## About

This is a project for natural language to logical language LTL. 

It was made using  **Anaconda3**  + **Python** + **Django** and database is **SQLite**.
**Bootstrap** was used for styling.

Install dependencies:
```bash
$ pip install -r requirements.txt
```

## How to run

### Default

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

### Others
 
You can also load the project in editors such as Pycharm. The following environment needs to be configured

```
1. File -> setting -> project -> Python Interpreter -> add local Interpreter
2. Edit Configurations -> django sever
3. db.sqlit (Download https://github.com/xerial/sqlite-jdbc/releases/download/3.43.0.0/sqlite-jdbc-3.43.0.0.jar)
```

## Web operation tips
If it cannot be displayed normally, please open the three files readme_1_img.png, readme_2_img.png, and readme_3_img.png in the main directory.
![img1](https://github.com/ChunyiLi322/Space2LTL/blob/master/readme_1_img.png)
![img2](https://github.com/ChunyiLi322/Space2LTL/blob/master/readme_2_img.png)
![img3](https://github.com/ChunyiLi322/Space2LTL/blob/master/readme_3_img.png)
