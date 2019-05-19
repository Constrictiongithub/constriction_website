dependencies:
	sudo apt install python3 python3-dev python3-virtualenv postgresql nodejs npm

virtualenv:
	virtualenv --python=python3 .
	./bin/pip install -r requirements.txt

node:
	cd layout; npm install; cd ..

init: dependencies virtualenv node

migrations:
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py makemigrations --noinput
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py migrate --noinput

translations:
	docker exec -i -t -w /project/constriction/constriction/ constriction_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/constriction/layout/ constriction_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/constriction/investments/ constriction_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/constriction/constriction/ constriction_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/constriction/layout/ constriction_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/constriction/investments/ constriction_django_1 ../../bin/python ../manage.py compilemessages

theme:
	cd layout; npm run build; cd ..
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py collectstatic --noinput

theme_dev:
	cd layout; npm run dev; cd ..
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py collectstatic --noinput -l
	cd layout; npm run watch; cd ..

scrape:
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py scrape --noupdate --delete --limit=10

import:
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py import
