# Learnings

## Basics

- Better to separate environments in separate virtual environments
- Creating empty project: `django-admin startproject <project-name>` . Creates scaffolding of empty project
- Each component inside a project is called as app. Intuition is to make reusable components. Run `python manage.py startapp <app-name>`
- Running project: `python manage.py runserver`
- `urls.py` routes paths. Paths inside apps can be appended with `include(...)` method
- `templates` folder is searched in each app. So by convention, add `<app-name>` folder inside `templates` folder.
- In order to locate your blog templates, add `blogs.app.BlogConfig` in project's `settings.py`
- Use `render` to render templates. It takes subdirectory inside `templates` folder as input.
- Accessing shell in django: `python manage.py shell`

## Templating
- Jinja templating engine relatively faster than the native django one
- Templates should be extended to avoid code repetition
- Static files like css should be held under `static/<app-name>` folder
- Static folder is loaded in template with `{% load static %}`
- Static files are loaded with: `{% static <file-path> %}`
- Urls are loaded in template with: `{% url '<url-name> %}`

## Migrations
- To create database migration: `python manage.py makemigration` . This will db specific files.
- To migrate existing database: `python manage.py migrate`
- To create super user: `python manage.py createsuperuser`
- To see sql queries that will be executed: `python manage.py sqlmigrate <app-name> <migration-name>` . Ex: `python manage.py sqlmigrate blog 0001`
- Register your `Post` model with: `admin.site.register(Post)` in `admin.py` file.

## User Registration
- Extend UserCreationForm if want to add more fields to default form
- `django-crispy-forms` to get formatted forms 
- `@login_required` decorator to allow paths only for logged in user

## User Profile
- can be created with signals once a user is created

## Views
- Standard CRUD operations can be performed with standard views that are provided
- Make sure that View is the last parent. Validation classes should be inherited before view otherwise validation won't be triggered.
- pagination can be triggered just by `paginated_by` attribute

## Deploying on server
- Setting hostname: `hostnamectl set-hostname django-server`
- Set route to django-server in `/etc/hosts` . `<ip> django-server`
- (For convenience and security) add a user: `adduser psukalka` 
- Make the user admin: `adduser psukalka sudo`
- Setting up ssh key based authentication:
  - On server, create `~/.ssh` folder
  - On local machine, generate ssh key: `ssh-keygen -b 4096`
  - Transport ssh key to server: `scp ~/.ssh/id_rsa.pub psukalka@<ip>:~/.ssh/authorized_keys`
  - Configure server to disallow root login and login with passwords (since we are using key based authentication)
    - Go to `vim /etc/ssh/sshd_config`
    - `PermitRootLogin no`
    - `PasswordAuthentication no`
    - Restart ssh: `sudo systemctl restart sshd`
- Setting up firewall:
  - `sudo apt-get install ufw`
  - `sudo ufw default allow outgoing`
  - `sudo ufw default deny incoming`
  - `sudo ufw allow ssh` (Otherwise you won't be able to ssh next time)
  - `sudo ufw allow 8000` (Since django runs on this port)
  - `sudo ufw enable` (To enable rules)
- Generate requirements.txt file for your project: `pip freeze > requirements.txt` (after activating virtualenv)
- Copy project to the server (either through git or scp)
- Setting up virtualenv:
    - `sudo apt-get install python3-pip`
    - `sudo apt-get install python3-venv`
    - `python3 -m venv django_project/venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`
- Update `django_project/settings.py` --> `ALLOWED_HOSTS = ['<IP OF SERVER>']`
- In production, static files are handled differently than dev env. 
  - Add `STATIC_ROOT = os.path.join(BASE_DIR, 'static')`
  - `python manage.py collectstatic`
- Run server: `python manage.py runserver 0.0.0.0:8000`
- But that is not best way of running server. Run it with apache/nginx and wsgi:
  - `sudo apt-get install apache2`
  - `sudo apt-get install libapache2-mod-wsgi-py3`
  - `cd /etc/apache2/sites-available/`
  - `sudo cp 000-default.conf django_project.conf`
  - Direct /static to your project's static folder: `Alias /static /home/psukalka/django_project/static`
  - ```
    <Directory /home/psukalka/django_project/static>
        Require all granted
    </Directory>``` 
  - Direct /media to your project's static folder: `Alias /media /home/psukalka/django_project/media`
  - ```
    <Directory /home/psukalka/django_project/media>
        Require all granted
    </Directory>```
  - Grant access to project's wsgi.py file:
    ```
       <Directory /home/psukalka/django_project/django_project>
         <Files wsgi.py>
           Require all granted
         </Files>
       </Directory>
    ```
  - `WSGIScriptAlias / /home/psukalka/django_project/django_project/wsgi.py`
  - `WSGIDaemonProcess django_app python-path=/home/psukalka/django_project python-home=/home/psukalka/django_project/venv`
  - `WSGIProcessGroup django_app`
- Enable site: `cd ~ ; sudo a2ensite django_project`
- Disable default conf: `sudo a2dissite 000-default.conf`
- Give apache permissions to write to db : 
  - `sudo chown :www-data django_project/db.sqlite3`
  - `sudo chmod 664 django_project/db.sqlite3`
  - `sudo chown :www-data django_project/`
  - `sudo chmod 775 django_project/`
  - `sudo chown -R :www-data django_project/media/`
  - `sudo chmod -R 775 django_project/media`
- Store sensitive info in config.json file (Env is also other option but it is bit longer way):
  - `sudo touch /etc/config.json`
  - Add SECRET_KEY, EMAIL_USER, EMAIL_PASS to it
  - In `settings.py` read the config file and populate the respective variables from it.
- Disallow the 8000 port that was used for testing: `sudo ufw delete allow 8000`
- Allow http traffic: `sudo ufw allow http/tcp`
- Start apache : `sudo service apache2 restart`
- Django deployment checklist
- After setting domain, add it in `ALLOWED_HOSTS` of settings.py
- Follow let's encrypt steps to enable HTTPS
- To verify if config is correct: `sudo apachectl configtest`
- Through firewall allow HTTPS traffic: `sudo ufw allow https`
- Renewing certificate after 90 days. Better add this in cron: `sudo certbot renew --quiet` 
  - Dryrun for this : `sudo certbot renew --dry-run`

## How To:
- Revert migration ?
- CRUD operations ?
    - For HTML, standard views are available. They can be consumed for CRUD
- better way for login_required on multiple paths 
    - Views can also be class level like they are functional.
    - When they are class level, LoginRequiredMixin can be used
- logging in django
- tests in django 
- is multi-threaded ?
- async tasks and celery integration ? 
- JS integration 
- architecture ? How do pieces connect ? 
    - Django follows MVC (or if you want to call it MTV architecture)
    - Everything revolves around model and views and templates take care of rendering them in desired format
    - Middlewares are onion layers around view
- migrating from one db to another ? 
    - Standard support is for relational dbs 
    - For no-sql db other side project is there
- Django signals ? 
- API docs ?
- Views in android ? How is django compatible with them ? What changes are required ? 
- Error pages 
