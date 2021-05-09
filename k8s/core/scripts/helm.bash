#!/usr/bin/env bash

set -eu

# Fail on a single failed command in a pipeline
set -o pipefail 


BASE_DIR="${1}"
COMMAND="${2}"
APP_NAME=${3}
NAMESPACE=${4}
CHART_NAME=${5}
ADDITIONAL_ARGS=${6:-}
BASE_DOMAIN="asim.com"


# helm repo update


helm_install() {
  helm install ${APP_NAME} ${CHART_NAME} \
    --namespace ${NAMESPACE} \
    --create-namespace \
    --values ${BASE_DIR}/k8s/templates/${CHART_NAME}.yaml \
    --set ingress.hostname=${APP_NAME}.${BASE_DOMAIN} \
    ${ADDITIONAL_ARGS} \
    --output json
}


helm_update() {
  helm upgrade ${APP_NAME} ${CHART_NAME} \
    --namespace ${NAMESPACE} \
    --values ${BASE_DIR}/k8s/templates/${CHART_NAME}.yaml \
    --set ingress.hostname=${APP_NAME}.${BASE_DOMAIN} \
    ${ADDITIONAL_ARGS} \
    --output json
}


helm_list() {
  helm list \
    --namespace ${NAMESPACE} \
    ${ADDITIONAL_ARGS} \
    --output json
}


case ${COMMAND} in
  "install")
    helm_install
    ;;
  "update" | "upgrade")
    helm_update
    ;;
  "delete")
    helm uninstall ${APP_NAME} -n ${NAMESPACE}
    ;;
  "list")
    helm_list
    ;;
  *)
    exit 4
    ;;
esac
