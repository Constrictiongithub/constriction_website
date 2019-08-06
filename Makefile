dependencies:
	sudo apt install python3 python3-dev python3-virtualenv postgresql nodejs npm

node:
	cd layout; npm install; cd ..

init: dependencies node

makemigrations:
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py makemigrations --noinput

migrate:
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py migrate --noinput

makemessages:
	docker exec -i -t -w /project/constriction/constriction/ constriction_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/constriction/layout/ constriction_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/constriction/investments/ constriction_django_1 ../../bin/python ../manage.py makemessages -a

compilemessages:
	docker exec -i -t -w /project/constriction/constriction/ constriction_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/constriction/layout/ constriction_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/constriction/investments/ constriction_django_1 ../../bin/python ../manage.py compilemessages
	docker restart constriction_django_1

theme:
	cd layout; npm run build; cd ..
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py collectstatic --noinput
	docker restart constriction_django_1

theme_dev:
	cd layout; npm run dev; cd ..
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py collectstatic --noinput -l
	cd layout; npm run watch; cd ..

import:
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py import

scrape:
	docker exec -i -t -w /project/constriction/ constriction_django_1 ../bin/python manage.py scrape --noupdate --delete --limit=10
