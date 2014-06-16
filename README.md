## BMAT ##
A BookMarks App Thing!

## Installation ##
Clone the repo:
> git clone https://github.com/RossBrunton/BMAT.git bmat/

Create a virtualenv:
> virtualenv -p /usr/bin/pypy bmat

(You can use /usr/bin/python2.7 if you like, but it may not work)

Enter this directory:
> cd bmat

Activate the virtualenv:
> source ./bin/activate

Install Django and MySQL:
> pip install Django MySQL-python

After this, rename settings.py.sample, to settings.py, and give it a random secret key. Then (if you want to, otherwise
it will use Django's default database) rename db.cnf.sample to db.cnf and fill in database details.

Sync the database:
> manage.py syncdb

Run the server (development only):
> manage.py runserver

For production, set up as you normall would a Django project.

## Super Interesting Legal Stuff ##
This is licensed under the MIT License, see COPYING.txt for details.
Generally, you can do whatever you want with it. I'd appreciate it if you mentioned me, however.
