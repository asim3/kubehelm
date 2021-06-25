#!/usr/bin/env bash

set -eu

# Fail on a single failed command in a pipeline
set -o pipefail 


helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add jetstack      https://charts.jetstack.io
helm repo add bitnami       https://charts.bitnami.com/bitnami


helm repo update
