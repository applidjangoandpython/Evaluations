SensLarge
=========

Simple form management

Quickstart
----------

.. code-block:: bash
  
  pew new senslarge
  pip install -U -r requirements.txt
  createdb senslarge
  ./manage.py migrate
  ./manage.py loaddata senslarge/fixtures/fixture.json
  ./manage.py createsuperuser
  ./manage.py runserver
