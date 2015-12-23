home-screen README
==================

Getting Started
---------------
There are two ways to run this application. One is based on Google App Engine for hosting while the second is based on local hosting

Local hosting
-------------
- source environment_name/bin/activate

- cd <directory containing this file>

- $VENV/bin/pip install -r requirements.txt -t lib/ —-update

- $VENV/bin/python setup.py develop

- $VENV/bin/pserve development.ini


Google App Engine Locally
-------------------------
This requires Google App Engine SDK to be installed locally on the computer
- source environment_name/bin/activate

- cd <directory containing this file>

- $VENV/bin/pip install -r requirements.txt -t lib/ -—update

- dev_appserver.py —log_level=debug .

Google App Engine Updating 
--------------------------
This requires Google App Engine SDK to be installed locally on the computer
- source environment_name/bin/activate

- cd <directory containing this file>

- $VENV/bin/pip install -r requirements.txt -t lib/ -—update

- cd ..

- appcfg.py update <directory containing this file>
