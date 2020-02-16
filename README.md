# library-request
A small flask application to request a book title from a library

# Setup
Create a virtualenv enviroment for python 3.6 for example:
davidg@davidg:~/library-request$ virtualenv -p /usr/bin/python3.6 py36


Enter into the virtualenv and install the requirements from the requirements.txt file
source py36/bin/activate
pip install -r requirements.txt

export FLASK_APP=start.py
flask run

Load the Db structure:
~/library-request/database$ sqlite3 flask_library.db < schema.sql

To run the tests
~/library-request$ pytest
