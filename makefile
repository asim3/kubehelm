SHELL=/bin/bash

ACTIVATE=source ./.venv/bin/activate &&


# make test args=my_app
test:
	${ACTIVATE} python3 ./run.py test ${args};


install:
	if [ ! -d ./.venv ]; then python3 -m venv ./.venv; fi;
	${ACTIVATE} pip3 install -r ./requirements.txt


shell:
	${ACTIVATE} python3
