API_ROOT := ./api_service/manage.py
STOCK_ROOT := ./stock_service/manage.py
VENV_ROOT := virtualenv
VENV_ACTIVATE := . $(VENV_ROOT)/bin/activate

install:
	(\
		python -m venv $(VENV_ROOT) && \
		$(VENV_ACTIVATE) && \
		pip install -r requirements.txt; \
	)

setup: install migrate create_user create_superuser

api: 
	(\
		$(VENV_ACTIVATE) && \
		$(API_ROOT) runserver; \
	)

stock: 
	(\
		$(VENV_ACTIVATE) && \
		$(STOCK_ROOT) runserver 127.0.0.1:9000; \
	)

clean:
	rm -rf __pycache__ && \
	rm stock_service/db.sqlite3 && \
	rm api_service/db.sqlite3 && \
	rm -rf virtualenv; \

test_api:
	(\
		$(VENV_ACTIVATE) && \
		$(API_ROOT) test api; \
	)

test_stock:
	(\
		$(VENV_ACTIVATE) && \
		$(STOCK_ROOT) test stocks; \
	)

test: test_api test_stock

migrate:
	(\
		$(VENV_ACTIVATE) && \
		python $(API_ROOT) makemigrations && \
		python $(API_ROOT) migrate; \
	)

create_user:
	(\
		$(VENV_ACTIVATE) && \
		echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('octavio', 'octavio@myproject.com', 'password')" | python $(API_ROOT) shell; \
	)

create_superuser:
	(\
		$(VENV_ACTIVATE) && \
		echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python $(API_ROOT) shell; \
	)
