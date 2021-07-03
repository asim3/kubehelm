# KubeHelm
Deploy a production ready apps to Kubernetes using Helm.


## requirements
- kubernetes cluster 
- helm


## setup Helm
```bash
sudo snap install helm  --classic

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add jetstack      https://charts.jetstack.io
helm repo add bitnami       https://charts.bitnami.com/bitnami

helm repo update
```


## install kubehelm
```bash
python3 -m venv ./.venv2

source ./.venv2/bin/activate

pip install kubehelm
```


## install new app
```bash
kubehelm install whoami
```


## read kubernetes objects
```py
from kubehelm.objects import Namespace, Deployment, Pod


Namespace().list_names()
# ['default', 'ingress-nginx', 'kube-node-lease', 'kube-public', 'kube-system']


Deployment(namespace="ingress-nginx").list_names()
# ['ingress-nginx-controller']


Deployment(namespace="ingress-nginx", name="ingress-nginx-controller").get()
# {
#     'code': 200,
#     'namespace': 'ingress-nginx',
#     'name': 'ingress-nginx-controller',
#     'status': 'Sustained',
# }


Pod(namespace="ingress-nginx").list_names()
# [
#     'ingress-nginx-admission-create-wllqn',
#     'ingress-nginx-admission-patch-xmjs9',
#     'ingress-nginx-controller-5d88495688-8mql5',
# ]
```
