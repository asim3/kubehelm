#!/bin/bash

# Source: https://github.com/kubernetes/ingress-nginx/releases

BASE_DIR="${1}"

tag_name='controller-v0.46.0'


rm -rf /tmp/ingress-nginx-controller
mkdir  /tmp/ingress-nginx-controller
cd     /tmp/ingress-nginx-controller

curl -LO https://github.com/kubernetes/ingress-nginx/archive/refs/tags/${tag_name}.tar.gz \
  && tar -xzf ${tag_name}.tar.gz \

mv /tmp/ingress-nginx-controller/ingress-nginx-${tag_name}/deploy/static/provider/aws/deploy.yaml \
  ${BASE_DIR}/k8s/templates/ingress/aws.yaml 

mv /tmp/ingress-nginx-controller/ingress-nginx-${tag_name}/deploy/static/provider/baremetal/deploy.yaml \
  ${BASE_DIR}/k8s/templates/ingress/baremetal.yaml

mv /tmp/ingress-nginx-controller/ingress-nginx-${tag_name}/deploy/static/provider/cloud/deploy.yaml \
  ${BASE_DIR}/k8s/templates/ingress/cloud.yaml 

mv /tmp/ingress-nginx-controller/ingress-nginx-${tag_name}/deploy/static/provider/do/deploy.yaml \
  ${BASE_DIR}/k8s/templates/ingress/do.yaml 

mv /tmp/ingress-nginx-controller/ingress-nginx-${tag_name}/deploy/static/provider/kind/deploy.yaml \
  ${BASE_DIR}/k8s/templates/ingress/kind.yaml 

