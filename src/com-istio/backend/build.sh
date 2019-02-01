kubectl delete -f deploy.yml
docker build -t titogarrido/observability-meetup-backend:1.0 .
docker push titogarrido/observability-meetup-backend:1.0
kubectl apply -f deploy.yml
