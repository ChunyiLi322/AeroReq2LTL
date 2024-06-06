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
Unzip the **node_modules.zip** file to the current file. This file is a third-party library, which has many files that are difficult to upload.
```
/nl2flweb/mysite/blog/static/blog/js/node_modules.zip  
```



