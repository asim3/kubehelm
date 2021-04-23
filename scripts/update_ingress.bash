#!/bin/bash

BASE_DIR="${1}"

version='0.34.1'

curl -s -o ${BASE_DIR}/templates/ingress.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v${version}/deploy/static/provider/do/deploy.yaml
