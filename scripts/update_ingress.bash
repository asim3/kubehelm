#!/bin/bash

# Source: https://github.com/kubernetes/ingress-nginx/releases

BASE_DIR="${1}"

version='0.34.1'


rm -rf /tmp/ingress-nginx-controller
mkdir  /tmp/ingress-nginx-controller
cd     /tmp/ingress-nginx-controller

curl -LO https://github.com/kubernetes/ingress-nginx/archive/refs/tags/controller-v${version}.tar.gz \
  && tar -xzf controller-v${version}.tar.gz \
  && mv /tmp/ingress-nginx-controller/ingress-nginx-controller-v${version}/deploy/static/provider/do/deploy.yaml        ${BASE_DIR}/templates/ingress/do.yaml \
  && mv /tmp/ingress-nginx-controller/ingress-nginx-controller-v${version}/deploy/static/provider/aws/deploy.yaml       ${BASE_DIR}/templates/ingress/aws.yaml \
  && mv /tmp/ingress-nginx-controller/ingress-nginx-controller-v${version}/deploy/static/provider/cloud/deploy.yaml     ${BASE_DIR}/templates/ingress/cloud.yaml \
  && mv /tmp/ingress-nginx-controller/ingress-nginx-controller-v${version}/deploy/static/provider/kind/deploy.yaml      ${BASE_DIR}/templates/ingress/kind.yaml \
  && mv /tmp/ingress-nginx-controller/ingress-nginx-controller-v${version}/deploy/static/provider/scw/deploy.yaml       ${BASE_DIR}/templates/ingress/scw.yaml \
  && mv /tmp/ingress-nginx-controller/ingress-nginx-controller-v${version}/deploy/static/provider/baremetal/deploy.yaml ${BASE_DIR}/templates/ingress/baremetal.yaml
