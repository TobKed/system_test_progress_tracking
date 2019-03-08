.PHONY: all venv test install build up up-d start stop restart down

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3
HOST=127.0.0.1
PORT=8000

help:
	@echo 'Makefile for System Test Progress Tracking                                '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '  Docker:                                                                 '
	@echo '    make build                          build services                    '
	@echo '    make up                             start services                    '
	@echo '    make up-d                           start services detached           '
	@echo '    make start                          start  containers                 '
	@echo '    make stop                           stop running containers           '
	@echo '    make restart                        stop and start containers         '
	@echo '    make down                           stop and remove containers        '
	@echo '                                                                          '
	@echo '  Local:                                                                  '
	@echo '    make venv                           create new virtual environment    '
	@echo '                                              and install dependencies    '
	@echo '    make django-run                     start django server               '
	@echo '    make run-virtual-machine            start virtual testing machine     '
	@echo '    make docker-run                     run docker with redis instance    '
	@echo '    make test                           run tests                         '
	@echo '                                                                          '
	@echo 'Additional:                                                               '
	@echo '    make install                        install dependencies              '
	@echo '                                          they should be installed by venv'
	@echo '                                          but you can install them again  '
	@echo 'Variables:                                                                '
	@echo '    HOST:                                                                 '
	@echo '        host for django server, e.g. make HOST=10.11.12.14 run            '
	@echo '        default HOST=127.0.0.1                                            '
	@echo '    VENV_NAME:                                                            '
	@echo '         virtual environment name                                         '
	@echo '         default VENV_NAME=venv                                           '


build:
	docker-compose build

up:
	docker-compose up

up-d:
	docker-compose up -d

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose stop && docker-compose start

down:
	docker-compose down


venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: requirements.txt
	test -d $(VENV_NAME) || virtualenv --python=python3.6 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

install:
	$(PYTHON) -m pip install -r requirements.txt

docker-run:
	sudo docker run -p 6379:6379 -d redis:2.8

django-run:
ifdef DJANGO_SECRET_KEY
	$(PYTHON) system_test_progress_tracking/manage.py runserver $(HOST):$(PORT)
else
	@echo 'ERROR! set environmental variable DJANGO_SECRET_KEY first'
endif

run-virtual-machine:
	$(PYTHON) virtual_testing_machine/run.py

test:
	$(PYTHON) test.py
