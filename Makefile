MANAGE=./manage.py
APP=teachrecovery
FLAKE8=./ve/bin/flake8

jenkins: ./ve/bin/python validate flake8 jshint jscs test

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: ./ve/bin/python
	$(MANAGE) jenkins --pep8-exclude=migrations --enable-coverage --coverage-rcfile=.coveragerc

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) quizblock_random --max-complexity=10 --exclude=migrations

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint media/coin_game/ media/quizblock_random/

jscs: node_modules/jscs/bin/jscs
	./node_modules/jscs/bin/jscs media/coin_game/ media/quizblock_random --config=./jscsrc

node_modules/jscs/bin/jscs:
	npm install jscs --prefix .

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

runserver: ./ve/bin/python validate
	$(MANAGE) runserver

migrate: ./ve/bin/python validate jenkins
	$(MANAGE) migrate

validate: ./ve/bin/python
	$(MANAGE) validate

shell: ./ve/bin/python
	$(MANAGE) shell_plus

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make validate
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make validate
	make test
	make migrate
	make flake8

syncdb: ./ve/bin/python
	$(MANAGE) syncdb

collectstatic: ./ve/bin/python validate
	$(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python validate jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate
