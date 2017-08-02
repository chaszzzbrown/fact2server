This is the repository for the django based back-end for the Factitious 2 project. It uses python 2.7 (already on your mac); some libraries need to be installed using `virtualenv`.

# Setup #

Create a folder called `server`. Clone this project into a subfolder called `fact2server`.

Using FTP, copy the folder:

    /home/django/factitious_project/server/media/

into the local `server` folder as well; so your directory will now look like:

    server/
        fact2server/
        media/

The `media/` folder just contains the images that are used in the individual articles; they get put into a folder separate from the django code, because they will be served directly by the `nginx` web server and not by the django app.

Finally, we need to copy the database file:

    /home/django/factitious_project/server/factitious_app/db.sqlite3

into your local `fact2server` folder.

If the `db.sqlite3` file is large (>10 Megabytes), it is better to `ssh` in to the server, make a local copy of the file into your home directory, and then ftp that down. This is because users may be making changes to the database in real-time; since the `ftp` may take a minute or so, you want to be sure that the file is not changing while you are downloading it.

To do this without going through the whole shelling-in process, you can just do this (assuming your user name is `rahaf`):

    ssh rahaf@augamestudio.com cp /home/django/factitious_project/server/factitious_app/db.sqlite3 ~/db.sqlite3

(You will be asked for your password). This tells the server to copy the file to your home directory on the *remote* server. Then you can use FTP to copy the copy to your machine.

## Initial setup of your virtual environemnt ##

Some external libraries (like, uh, `django`) need to be available here. The best way to do this is use a virtual environment; these are the steps required to initially set this environment up, which you only need to do once. Aftwerwards, you'll need to make sure the environment is active each time you start work; see below.

If you haven't already, install `virtualenv`:

    pip install virtualenv

(Depending on your setup, you may need to use `sudo` here.) Full info on `virtualenv` is just a Google away.

Next, `cd` into your `server` folder, and create a new environment:

    virtualenv env

This will create a folder `env` in the server folder, which will contain the libraries we will be using.

Next, activate the environment:

    source env/bin/activate

There should now be a `(env)` at the end of your command prompt.

We can now install the required libraries:

    pip install -r fact2server/requirements.txt

Voila!

# For Local Testing #

Whenever you start working on the Fact2 app, you'll need to activate the enviroment first.

First, `cd` into the `fact2server` folder (because you'll want to be there anyway). Next, activate the environment:

    source ../env/bin/activate

You will now see the `(env)` at the end of your command prompt.

Next you want to start the server:

    python manage.py runserver

This will start the django development server on port 8000. Now you can switch to a new tab, `cd` into the client side folder, and run `gulp serve`.

If you need to stop or restart the server, use `ctrl-C`. 

You do not need to "re-activate" the enviroment to restart the server as long as `(env)` is at the end of your command prompt; just use `python manage.py runserver` again.

To stop using the environment (for some reason?) just type:

    deactivate

and the environment will stop being used (and the `(env)` will go away from your command prompt).


