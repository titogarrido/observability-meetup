kubectl delete -f deploy.yml
kubectl delete gateway frontend-gateway
docker build -t titogarrido/observability-meetup-frontend:1.0 .
docker push titogarrido/observability-meetup-frontend:1.0
kubectl apply -f deploy.yml && kubectl apply -f gateway.yml
