#!/usr/bin/env bash

set -eu

# Fail on a single failed command in a pipeline
set -o pipefail 


BASE_DIR="${1}"
COMMAND="${2}"


ingress_install() {
  helm install \
    ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-nginx \
    --create-namespace \
    --set installCRDs=true \
    --output json
}


ingress_update() {
  helm upgrade \
    ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-nginx \
    --create-namespace \
    --set installCRDs=true \
    --output json
}


case ${COMMAND} in
  "install")
    ingress_install
    ;;
  "update" | "upgrade")
    ingress_update
    ;;
  *)
    exit 4
    ;;
esac
