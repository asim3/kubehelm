# KubeHelm
Deploy a production ready apps to Kubernetes using Helm.


## requirements
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
