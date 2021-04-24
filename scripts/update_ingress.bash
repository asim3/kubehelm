#!/bin/bash

BASE_DIR="${1}"

version='0.34.1'

curl -s -o ${BASE_DIR}/templates/ingress/do_main.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v${version}/deploy/static/provider/do/deploy.yaml

curl -s -o ${BASE_DIR}/templates/ingress/do.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/do/deploy.yaml
curl -s -o ${BASE_DIR}/templates/ingress/aws.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/aws/deploy.yaml
curl -s -o ${BASE_DIR}/templates/ingress/cloud.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/cloud/deploy.yaml

curl -s -o ${BASE_DIR}/templates/ingress/kind.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
curl -s -o ${BASE_DIR}/templates/ingress/scw.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/scw/deploy.yaml

curl -s -o ${BASE_DIR}/templates/ingress/baremetal.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/baremetal/deploy.yaml
