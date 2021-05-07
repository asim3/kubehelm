#!/usr/bin/env bash

BASE_DIR="$(dirname $(dirname ${BASH_SOURCE[0]}))"

replace_app_name='s/aappppnnaammee/{{ app_name }}/'
replace_namespace='s/nnaammeessppaaccee/{{ namespace }}/'
replace_managed_by='s/managed-by: Helm/managed-by: Asim/'


# helm repo update

upgrade_template() {
  helm install aappppnnaammee bitnami/${1} \
    -n nnaammeessppaaccee \
    --dry-run  \
    --set mariadb.enabled=false \
    --set persistence.size=1Gi \
    --set service.type=ClusterIP \
    --set ingress.enabled=true \
    --set ingress.certManager=true \
    ${2} \
    | sed -e "$replace_app_name" \
    | sed -e "$replace_namespace" \
    | sed -e "$replace_managed_by" \
    > $BASE_DIR/k8s/templates/apps/${1}.yaml
}

upgrade_template wordpress --set mariadb.enabled=false
