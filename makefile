SHELL=/bin/bash

ACTIVATE=source ./.venv/bin/activate &&


# make args=my_app
main:
	@ ${ACTIVATE} python3 ./run.py ${args};


# make args='install whoami'
test:
	${ACTIVATE} python -m unittest discover -s ./tests


install:
	if [ ! -d ./.venv ]; then python3 -m venv ./.venv; fi;
	${ACTIVATE} pip3 install -r ./requirements.txt


shell:
	${ACTIVATE} python3


add:
	@ ${ACTIVATE} ./run.py install ${app};


list:
	@ ${ACTIVATE} ./run.py list aaa;


update:
	@ ${ACTIVATE} ./run.py update ${app};


delete:
	@ ${ACTIVATE} ./run.py delete ${app};


# PyPi
py-test: py-install py-clean

py-build:
	${ACTIVATE} pip install --upgrade wheel setuptools
	${ACTIVATE} python setup.py bdist_wheel

py-install:
	- rm -r .t_venv
	python3 -m venv .t_venv
	. .t_venv/bin/activate && pip install --upgrade wheel setuptools
	. .t_venv/bin/activate && python3 setup.py bdist_wheel
	. .t_venv/bin/activate && pip install dist/$$(ls -rXA ./dist | head -n 1)
	ls -al .t_venv/lib/python3.8/site-packages/kubehelm/
	ls -al .t_venv/lib64/python3.8/site-packages/kubehelm/

py-clean:
	- rm -r ./.t_venv 
	- rm -r ./build 
	- rm -r ./dist 
	- rm -r ./kubehelm.egg-info 

py-push: py-build
	${ACTIVATE} pip install --upgrade twine
	${ACTIVATE} python3 -m twine check dist/*
	${ACTIVATE} python3 -m twine upload --non-interactive -u asim3 -p ${PYPI_TOKEN} dist/*
