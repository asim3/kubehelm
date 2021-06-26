SHELL=/bin/bash

ACTIVATE=source ./.venv/bin/activate &&


# make args=my_app
main:
	@ ${ACTIVATE} python3 ./run.py ${args};


test: install-minikube verify-ingress-addon run-tests


install-minikube:
	minikube delete
	minikube start
	- minikube addons enable ingress || sleep 12
	minikube addons enable ingress


add-minikube-hosts:
	echo "$$(minikube ip)  django.kube-helm.local" | sudo tee -a /etc/hosts 
	echo "$$(minikube ip)  whoami.kube-helm.local" | sudo tee -a /etc/hosts 
	echo "$$(minikube ip)  mariadb.kube-helm.local" | sudo tee -a /etc/hosts 
	echo "$$(minikube ip)  phpmyadmin.kube-helm.local" | sudo tee -a /etc/hosts 
	echo "$$(minikube ip)  wordpress.kube-helm.local" | sudo tee -a /etc/hosts 
	echo "$$(minikube ip)  osclass.kube-helm.local" | sudo tee -a /etc/hosts 


verify-ingress-addon:
	for i in {2..300}; do  \
		echo $$i; \
		sleep 2; \
		is_ready=$$(kubectl get -n ingress-nginx deployment/ingress-nginx-controller -o jsonpath='{.status.readyReplicas}' || echo $$i ); \
		if [ "$$is_ready" == "1" ]; then break; fi; \
		if [ "$$i" == "300" ]; then exit 111; fi; \
	done;


run-tests:
	${ACTIVATE} python -m unittest discover -s ./tests


install:
	if [ ! -d ./.venv ]; then python3 -m venv ./.venv; fi;
	${ACTIVATE} pip3 install -r ./requirements.txt
	sudo snap install helm  --classic
	./kubehelm/scripts/update_helm_repo.bash


shell:
	${ACTIVATE} python3


# PyPi
py-build:
	${ACTIVATE} pip install --upgrade wheel setuptools
	${ACTIVATE} python setup.py bdist_wheel


py-install: py-clean
	python3 -m venv .t_venv
	. .t_venv/bin/activate && pip install --upgrade wheel setuptools
	. .t_venv/bin/activate && python3 setup.py bdist_wheel
	. .t_venv/bin/activate && pip install dist/$$(ls -rXA ./dist | head -n 1)
	ls -al .t_venv/lib/$$(ls .t_venv/lib/)/site-packages/
	ls -al .t_venv/lib/$$(ls .t_venv/lib/)/site-packages/kubehelm/
	ls -al .t_venv/lib64/$$(ls .t_venv/lib/)/site-packages/kubehelm/


py-test: py-install
	. .t_venv/bin/activate && kubehelm install whoami -n default -a test3
	. .t_venv/bin/activate && kubehelm update  whoami -n default -a test3
	. .t_venv/bin/activate && kubehelm list    whoami -n default -a test3
	. .t_venv/bin/activate && kubehelm delete  whoami -n default -a test3


py-clean:
	- rm -r ./.t_venv 
	- rm -r ./build 
	- rm -r ./dist 
	- rm -r ./kubehelm.egg-info 


py-push: py-build
	${ACTIVATE} pip install --upgrade twine
	${ACTIVATE} python3 -m twine check dist/*
	${ACTIVATE} python3 -m twine upload --non-interactive -u asim3 -p ${PYPI_TOKEN} dist/*


update-version:
	awk -F '.' '{ print $$1"."$$2"."$$3+1 "\"" }' kubehelm/__init__.py > kubehelm/temp.txt
	mv kubehelm/temp.txt kubehelm/__init__.py
