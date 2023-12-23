## BMAT ##
A BookMarks App Thing!

This is a small web application that allows you to store and categorise your bookmarks.

## Installation ##
You require virtualenv to be installed to set this up, this lives in the package `python-virtualenv` under Ubuntu.

Clone the repo:
> git clone https://github.com/RossBrunton/BMAT.git bmat/

Create a virtualenv:
> python3 -m venv .venv

Enter this directory:
> cd bmat

Activate the virtualenv:
> source .venv/bin/activate

Install Django and requests:
> pip install -r requirements.txt

After this, rename `settings_local.py.sample`, to `settings_locals.py`, and give it a random secret key.

If you want to use MySQL, install mysqlclient as follows:
> pip install mysqlclient

And then rename `db.cnf.sample` to `db.cnf` and fill in your database details.

If you want to use a sqlite file (or any of Django's database backends) uncomment and possibly edit the relevent section
in `settings_local.py`.

Sync the database:
> manage.py migrate

Create an account:
> manage.py createsuperuser

Run the server (development only):
> manage.py runserver

For production, set up as you normally would a Django project.

## Super Interesting Legal Stuff ##
This is licensed under the MIT License, see COPYING.txt for details.
Generally, you can do whatever you want with it. I'd appreciate it if you mentioned me, however.
