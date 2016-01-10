Table of Contents
=================

* [Quickstart](#quickstart)
* [Monthly Process To Update Data and Build the Project](#monthly-process-to-update-data-and-build-the-project)
* [Available Fabric Commands](#available-fabric-commands)
* [Building a Mac OS Python dev environment](#building-a-mac-os-python-dev-environment)


Quickstart
==========

* Change into that directory

        cd gauging_rainfall

* Rename ```TEMPLATE_development.yml``` to ```development.yml```

* Run ```fab makesecret``` and add the output on line 5 of ```development.yml```

* Assuming you have MySQL installed, open ```development.yml``` and add ```gauging_rainfall``` as the database name on line 17. Add in any username and password you might have for your MySQL install.

        database:
          host: "127.0.0.1"
          port: 3306
          database: "gauging_rainfall"
          username: "root"
          password: ""

* Assuming you have virtualenv and pip installed run ```fab bootstrap```

    * This attempts to scaffold the project by:
        * Creating virtualenv
        * Activating the virtualenv
        * Installing requirements
        * Creating the database
        * Applyin initial Django migrations
        * Creating the Django superuser
        * Running the Django development server

* Activate your virtualenv which should be named ```gauging_rainfall```

        workon gauging_rainfall

* At this point you should be able to run ```fab run``` and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and see a Django page...

----

Monthly Process To Update Data and Build the Project
====================================================

* Run the tests

        fab test

* Use the Fabric command to fetch the latest batch of data.

        fab ...

----

Available Fabric Commands
=========================

**Data Functions**

**Development Functions**

* ```run```: shortcut for base manage.py function to launch the Django development server

        local("python manage.py runserver")

* ```make```: shortcut for base manage.py function to make Django database migrations to sync the dev database

        local("python manage.py makemigrations")

* ```migrate```: shortcut for base manage.py function to apply Django database migrations

        local("python manage.py migrate")

* ```superuser```: shortcut for base manage.py function to create a superuser

        local("python manage.py createsuperuser")

**Bootstrapping Functions**

* ```requirements```:  shortcut to install requirements from repository's ```requirements.txt```

        local("pip install -r requirements.txt")

* ```create_db```: Creates a database based on DATABASE variables in ```settings_development.py``` file

        connection = None
        db_config = CONFIG["database"]
        logger.debug("Creating %s database for %s django project" % (db_config["database"], env.project_name))
        create_statement = "CREATE DATABASE %s" % (db_config["database"])
        try:
            connection = MySQLdb.connect(
                host = db_config["host"],
                user = db_config["username"],
                passwd = db_config["password"]
            )
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(create_statement)
            connection.commit()
        except MySQLdb.DatabaseError, e:
            print "Error %s" % (e)
            sys.exit(1)
        finally:
            if connection:
                connection.close()

* ```makesecret```: generates secret key for use in [django settings](https://github.com/datadesk/django-project-template/blob/master/fabfile/makesecret.py)

        key = ''.join(random.choice(allowed_chars) for i in range(length))
        print 'SECRET_KEY = "%s"' % key

* ```build```: Activates the django-bakery script to build the views specified in ```settings_development.py```

        local("python manage.py build")

* ```buildserver```: Activates the django-bakery development server

        local("python manage.py buildserver")

* ```move```

        local("python manage.py move_baked_files")

* ```bootstrap```: Attempts to scaffold the project by:
        * Creating virtualenv
        * Activating  the virtualenv
        * Installing requirements
        * Creating the database
        * Applying initial Django migrations
        * Creating the Django superuser
        * Running the Django development server

            with prefix("WORKON_HOME=$HOME/.virtualenvs"):
                with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                    local("mkvirtualenv %s" % (env.project_name))
                    with prefix("workon %s" % (env.project_name)):
                        requirements()
                        time.sleep(2)
                        create_db()
                        time.sleep(2)
                        migrate()
                        time.sleep(2)
                        local("python manage.py createsuperuser")
                        run()

----

Mac OS Python development environment
=====================================

* Assumming homebrew is installed...

    * Install homebrew python

            cd /System/Library/Frameworks/Python.framework/Versions
            sudo rm Current
            brew install python
            brew doctor
            which python
            which pip
            pip install --upgrade setuptools
            pip install --upgrade distribute
            pip install virtualenv
            pip install virtualenvwrapper
            python --version
            source /usr/local/bin/virtualenvwrapper.sh
            sudo ln -s /usr/local/Cellar/python/2.7.8_2 /System/Library/Frameworks/Python.framework/Versions/Current

    * Configure $PATH variables for python, virtualenv

            # homebrew path
            export PATH="/usr/local/bin:$PATH"

            # virtualenvwrapper settings
            export WORKON_HOME=$HOME/.virtualenvs
            export PIP_VIRTUALENV_BASE=$WORKON_HOME
            export PIP_RESPECT_VIRTUALENV=true
            source /usr/local/bin/virtualenvwrapper.sh

    * Install MySQL via homebrew

            brew remove mysql
            brew cleanup
            launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
            rm ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
            sudo rm -rf /usr/local/var/mysql
            brew install mysql
            ln -sfv /usr/local/opt/mysql/*.plist ~/Library/LaunchAgents

    * Getting mysql up and running

            mysql.server start
            mysql_secure_installation
            mysql -u root -p
            SHOW DATABASES;
            SET default_storage_engine=MYISAM;
