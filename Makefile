API_ROOT = ./api_service/manage.py
STOCK_ROOT = ./stock_service/manage.py

run_api:
	$(API_ROOT) runserver;

run_stock:
	$(STOCK_ROOT) runserver 127.0.0.1:9000;

activate:
	. virtualenv/bin/activate;

clean:
	rm -rf __pycache__; \
	rm -rf virtualenv;

test_api:
	$(API_ROOT) test api

test_stock:
	$(STOCK_ROOT) test stocks

test: test_api test_stock

migrate:
	$(API_ROOT) migrate; 

create_user:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('octavio', 'octavio@myproject.com', 'password')" | python $(API_ROOT) shell

create_superuser:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python $(API_ROOT) shell
