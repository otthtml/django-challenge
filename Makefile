run_api:
	./api_service/manage.py runserver;

run_stock:
	./stock_service/manage.py runserver;

activate:
	. virtualenv/bin/activate;

clean:
	rm -rf __pycache__; \
	rm -rf virtualenv;

test_api:
	./api_service/manage.py test api

test_stock:
	./stock_service/manage.py test stocks

test: test_api test_stock