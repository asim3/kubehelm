#!/usr/bin/env bash

BASE_DIR="$(dirname $(dirname ${BASH_SOURCE[0]}))"

helm repo update

upgrade_template() {
  helm install mmmmmm bitnami/${1} --dry-run  \
    > $BASE_DIR/k8s/templates/apps/${1}.yaml
}

upgrade_template wordpress
