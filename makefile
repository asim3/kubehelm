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

py-build:
	${ACTIVATE} pip install --upgrade wheel setuptools twine
	${ACTIVATE} python setup.py bdist_wheel

py-test:
	- rm -r .t_venv
	python3 -m venv .t_venv
	. .t_venv/bin/activate && pip install --upgrade wheel setuptools
	. .t_venv/bin/activate && python3 setup.py bdist_wheel
	. .t_venv/bin/activate && pip install dist/kubehelm-0.0.5-py3-none-any.whl
	ls -al .t_venv/lib64/python3.8/site-packages/k8s/

py-clean:
	- rm -r ./.t_venv 
	- rm -r ./build 
	- rm -r ./dist 
	- rm -r ./kubehelm.egg-info 