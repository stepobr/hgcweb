## HGCWEB
### A part viewer based and app library for HGCAL 


##### For local development
##### Just a temporary fork for demonstration

```bash
  

python venv environment
source environment/bin/activate
git clone
cd hgcweb
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata cassettes/construct/fixtures/cassette.json
python manage.py runserver
```
In browser, open:

http://127.0.0.1:8000/cassettes/construct/
