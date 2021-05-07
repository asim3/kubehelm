#!/usr/bin/env bash

# Source: https://github.com/jetstack/cert-manager/releases

BASE_DIR="${1}"

version='1.1.1'

rm -rf /tmp/cert-manager
mkdir  /tmp/cert-manager
cd     /tmp/cert-manager

curl -LO https://github.com/jetstack/cert-manager/releases/download/v${version}/cert-manager.yaml \
  &&  mv /tmp/cert-manager/cert-manager.yaml ${BASE_DIR}/k8s/templates/certificate/cert-manager.yaml
