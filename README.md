# codeflix-catalog-admin
Administração de Catálogo – Codeflix - Python

## Running

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
python manage.py startconsumer
python manage.py runserver
``