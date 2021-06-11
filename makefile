SHELL=/bin/bash

ACTIVATE=source ./.venv/bin/activate &&


# make args=my_app
main:
	@ ${ACTIVATE} python3 ./run.py ${args};


# make args='install whoami'
test:
	${ACTIVATE} python3 ./run.py test ${args};


install:
	if [ ! -d ./.venv ]; then python3 -m venv ./.venv; fi;
	${ACTIVATE} pip3 install -r ./requirements.txt


shell:
	${ACTIVATE} python3


add:
	@ ${ACTIVATE} python3 ./run.py install ${app};


list:
	@ ${ACTIVATE} python3 ./run.py list ${app};


update:
	@ ${ACTIVATE} python3 ./run.py update ${app};


delete:
	@ ${ACTIVATE} python3 ./run.py delete ${app};
