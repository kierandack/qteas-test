kubectl apply -f qteas-crd.yaml
kubectl apply -f qteas.yaml
source qteas/bin/activate
python3 qteas.py