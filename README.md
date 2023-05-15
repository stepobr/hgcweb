## HGCWEB
### A part viewer based and app library for HGCAL 


##### For local development
Just a temporary fork for demonstration

Use venv as you normally do

I use it with python 3.10

```bash
cd hgcweb
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata cassettes/construct/fixtures/cassette.json
python manage.py runserver
```
In browser, open:

http://127.0.0.1:8000/cassettes/construct/
