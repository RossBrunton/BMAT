## BMAT ##
A BookMarks App Thing!

## Installation ##
Clone the repo:
> git clone https://github.com/RossBrunton/BMAT.git bmat/

Create a virtualenv:
> virtualenv -p /usr/bin/python2.7 bmat

Enter this directory:
> cd bmat

Activate the virtualenv:
> source ./bin/activate

Install Django, MySQL and requests:
> pip install Django mysqlclient six requests

After this, rename settings_local.py.sample, to settings_locas.py, and give it a random secret key. Then (if you want
to, otherwise it will use Django's default database) rename db.cnf.sample to db.cnf and fill in database details.

Sync the database:
> manage.py migrate

Run the server (development only):
> manage.py runserver

For production, set up as you normally would a Django project.

## Super Interesting Legal Stuff ##
This is licensed under the MIT License, see COPYING.txt for details.
Generally, you can do whatever you want with it. I'd appreciate it if you mentioned me, however.
