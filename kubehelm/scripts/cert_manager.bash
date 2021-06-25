#!/usr/bin/env bash

set -eu

# Fail on a single failed command in a pipeline
set -o pipefail 


BASE_DIR="${1}"
COMMAND="${2}"


cert_install() {
  helm install \
    cert-manager jetstack/cert-manager \
    --namespace cert-manager \
    --create-namespace \
    --set installCRDs=true \
    --output json
}


cert_update() {
  helm upgrade \
    cert-manager jetstack/cert-manager \
    --namespace cert-manager \
    --create-namespace \
    --set installCRDs=true \
    --output json
}


case ${COMMAND} in
  "install")
    cert_install
    ;;
  "update" | "upgrade")
    cert_update
    ;;
  *)
    exit 4
    ;;
esac
