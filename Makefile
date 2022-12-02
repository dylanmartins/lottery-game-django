docker=docker exec -it django_api

createsuperuser:
	$(docker) python3 manage.py createsuperuser

makemigrations:
	$(docker) python3 manage.py makemigrations

migrate:
	$(docker) python3 manage.py migrate

test:
	$(docker) py.test -vv -xs .

run:
	(cd src && docker-compose up)

stop:
	(cd src && docker-compose down)

docker-shell:
	$(docker) python3 manage.py shell

docker-ssh:
	$(docker) /bin/bash

clean:
	@find ./src -name "*.pyc" -type f -delete -o -name "__pycache__" -delete