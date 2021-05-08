#!/usr/bin/env bash

BASE_DIR="$(dirname $(dirname ${BASH_SOURCE[0]}))"

replace_app_name='s/aappppnnaammee/{{ app_name }}/'
replace_namespace='s/nnaammeessppaaccee/{{ namespace }}/'
replace_managed_by='s/managed-by: Helm/managed-by: Asim/'
replace_ingress='s/asimcomasimcom/{{ app_name }}.asim.com/'


# helm repo update

upgrade_template() {
  app_name=${1}
  shift
  chart_flags=${@}
  helm install aappppnnaammee bitnami/${app_name} \
    -n nnaammeessppaaccee \
    --dry-run  \
    --set ingress.enabled=true \
    --set ingress.certManager=true \
    --set ingress.tls=true \
    --set ingress.hostname=asimcomasimcom \
    --set service.type=ClusterIP \
    --set persistence.size=1Gi \
    ${chart_flags} \
    | sed -e "$replace_app_name" \
    | sed -e "$replace_namespace" \
    | sed -e "$replace_managed_by" \
    | sed -e "$replace_ingress" \
    > $BASE_DIR/k8s/templates/apps/${app_name}.yaml
}

upgrade_template wordpress --set mariadb.enabled=false
