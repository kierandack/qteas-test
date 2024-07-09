curl -sfL https://get.k3s.io | sh -
kubectl create -f ./sample-app/.
kubectl create -f ./traefik/traefik-account.yaml
kubectl create -f ./traefik/traefik-role.yaml
kubectl create -f ./traefik/traefik-role-binding.yaml
kubectl create -f ./traefik/traefik-services.yaml
kubectl create -f ./traefik/traefik-ingress.yaml
kubectl create -f ./traefik/traefik.yaml
kubectl create -f ./prometheus/prometheus-config.yaml
kubectl create -f ./prometheus/prometheus-rbac.yaml
kubectl create -f ./prometheus/prometheus.yaml