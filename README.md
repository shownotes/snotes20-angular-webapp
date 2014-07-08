# snotes20

## Setup
```
$ git clone git@github.com:SimonWaldherr/snotes20.git
$ cd snotes20
$ git checkout srv
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ pip install https://www.djangoproject.com/download/1.7c1/tarball/
$ python manage.py migrate
```

## dev server
To start the development server at http://127.0.0.1:8000/ execute:
```
$ . venv/bin/activate
$ python manage.py runserver
```

## reset db
To delete all data and apply a new db-version execute:
```
$ rm db.sqlite3
$ python manage.py migrate
```

## email
You need an SMTP server to send registration-emails. Configure your connection details in `shownotes/settings.py` (`EMAIL_*`).

## etherpad (not yet)
You need a running etherpad instance. Once this is done, configure the API-secret in `shownotes/settings.py`.

```
$ git clone git@github.com:ether/etherpad-lite.git
$ cd etherpad-lite
$ ./bin/run.sh
```

The API-secret can be found in `etherpad-lite/APIKEY.txt`.
