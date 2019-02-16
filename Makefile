.PHONY: all test

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3
HOST=127.0.0.1
PORT=8000

help:
	@echo 'Makefile for System Test Progress Tracking                                '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make run-django                     start django server                '
	@echo '   make run-virtual-machine            start virtual testing machine      '
	@echo '   make install                        install dependencies               '
	@echo '   make run-docker                     run docker with redis instance     '
	@echo '   make test                           run tests                          '
	@echo '                                                                          '
	@echo 'Set the HOST variable for django server, e.g. make HOST=10.11.12.14 run   '
	@echo 'Default HOST='$(HOST)
	@echo 'Default VENV_NAME='$(VENV_NAME)
	@echo '                                                                          '


install:
	$(PYTHON) -m pip install -r requirements.txt

run-docker:
	sudo docker run -p 6379:6379 -d redis:2.8

run-django:
ifdef DJANGO_SECRET_KEY
	$(PYTHON) system_test_progress_tracking/manage.py runserver $(HOST):$(PORT)
else
	@echo 'ERROR! set environmental variable DJANGO_SECRET_KEY first'
endif

run-virtual-machine:
	$(PYTHON) virtual_testing_machine/run.py

test:
	$(PYTHON) test.py

