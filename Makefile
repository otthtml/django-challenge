API_ROOT := ./api_service/manage.py
STOCK_ROOT := ./stock_service/manage.py
VENV_ROOT := virtualenv
VENV_ACTIVATE := . $(VENV_ROOT)/bin/activate

install_venv:
	(\
		python -m venv virtualenv && \
		$(VENV_ACTIVATE) && \
		pip install -r requirements.txt; \
	)

run_api: 
	(\
		$(VENV_ACTIVATE) && \
		$(API_ROOT) runserver; \
	)

api: install_venv run_api


run_stock: 
	(\
		$(VENV_ACTIVATE) && \
		$(STOCK_ROOT) runserver 127.0.0.1:9000; \
	)

stock: install_venv run_stock

clean:
	rm -rf __pycache__ && \
	rm -rf virtualenv;

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
	$(API_ROOT) migrate; 

create_user:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('octavio', 'octavio@myproject.com', 'password')" | python $(API_ROOT) shell

create_superuser:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python $(API_ROOT) shell
