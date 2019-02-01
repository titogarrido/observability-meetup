# Meetup SRE Brasil #2 - Observability

## Primeiras impressões com o Istio

Este repositório contém os arquivos necessários para reproduzir os testes demonstrados em: https://www.youtube.com/watch?v=kvkdUorLUkY



## Requerimentos

Para fazer os testes abaixo você precisará de um servidor (ou sua próprio PC) com:

* Python (https://realpython.com/installing-python/)
* pip (https://www.makeuseof.com/tag/install-pip-for-python/)
* virtualenv (recomendado) (https://virtualenv.pypa.io/en/latest/installation/)
* Docker (https://docs.docker.com/install/)
  * Uma conta no Docker Hub para upload das imagens dos apps (https://hub.docker.com)
* Kubernetes (para o teste com Istio) (https://kubernetes.io/docs/setup/minikube/) **ou** (https://microk8s.io/)
* Istio habilitado no Kubernetes (https://istio.io/docs/setup/kubernetes/platform-setup/minikube/) **ou**  (https://microk8s.io/)



## Diagrama das aplicações

![](https://raw.githubusercontent.com/titogarrido/observability-meetup/master/images/apps.png)

## Testando o Opentracing e o Jaeger

### Requisitos

Para testar somente o Opentracing e o Jaeger você somente vai precisar ter instalado o:

* Python
* Pip
* Docker

### Instalando Jaeger

Comece inicializando a imagem Docker do Jaeger, chamada de `jaeger-all-in-one`:

```bash
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.9
```

A interface de consulta estará disponível em:

```
http://localhost:16686
```

![](https://raw.githubusercontent.com/titogarrido/observability-meetup/master/images/jaeger.png)



### Instalando o Mongo

```bash
docker run -d --name mongo -p 27017:27017 mongo
```

### Executando a app1, app2 e app3

A aplicação 1 (app1) é o Frontend. 

A aplicação 2 (app2) é o Backend. 

A aplicação 3 (app3) é o Meaning of Life.

1. Abra um terminal para cada aplicação, acesse o diretório de cada aplicação e execute:
   1. ```pip install -r requirements.txt```

#### Para a app1:

```bash
cd src/sem-istio/app1
python app1.py
```



#### Para a app2:

```bash
cd src/sem-istio/app2
python app2.py
```

#### Para a app3:

```bash
cd src/sem-istio/app3
python app3.py
```

Execute todas as aplicações e acesse:

http://localhost:8082

Faça várias requisições e consulte o Jaeger em:

http://localhost:16686

## Testando o Istio

### Requisitos

1. Kubernetes + Istio instalados e seu namespace default configurado para o sidecar Istio ser automaticamente acoplado quando a aplicação subir (istio-injection=enabled).
   1. https://istio.io/docs/setup/kubernetes/quick-start/

### Instalando o Mongo

Execute o kubectl apply no `mongo.yml `que está dentro da pasta *com-istio*:

```bash
kubectl apply -f mongo.yml
```

### Executando os apps no Kubernetes

Modifique os arquivos `build.sh` e `deploy.yml` de cada aplicação (frontend, backend e meaning) trocando o nome do usuário do Docker Hub de *titogarrido* para seu nome de usuário. Esse arquivos são:

```bash
com-istio/frontend/deploy.yml
com-istio/frontend/build.sh
com-istio/backend/deploy.yml
com-istio/backend/build.sh
com-istio/meaning/deploy.yml
com-istio/meaning/build.sh
```

Você pode atualizar com o *sed* utilizando o seguinte comando de dentro do diretório *com-istio*:

```bash
sed -i 's/titogarrido/SEU_USUARIO_DOCKER/g' frontend/*
sed -i 's/titogarrido/SEU_USUARIO_DOCKER/g' backend/*
sed -i 's/titogarrido/SEU_USUARIO_DOCKER/g' meaning/*
```

Depois de modificado para seu usuário Docker podemos fazer o build e deploy utilizando o script `build.sh`de cada aplicação:

```bash
bash com-istio/frontend/build.sh
bash com-istio/backend/build.sh
bash com-istio/meaning/build.sh
```

Depois de executado observe seu dashboard do Kubernetes e confirme que os serviços estão no ar:

![](https://raw.githubusercontent.com/titogarrido/observability-meetup/master/images/kubernetes.png)

Acesse a aplicação *frontend* utilizando seu *ingress*. Para descobrir qual o endereço de seu *ingress* ip e porta siga os passos de:

https://istio.io/docs/tasks/traffic-management/ingress/#determining-the-ingress-ip-and-ports



Para o endereço dos serviços como Jaeger e Grafana utilize o *kubectl*:

`kubectl get all --all-namespaces`

Procure por `service/grafana`e `service/jaeger-query`:

`istio-system   service/grafana                    ClusterIP      10.152.183.114   <none>        3000/TCP`

`istio-system   service/jaeger-query               ClusterIP      10.152.183.113   <none>        16686/TCP`

http://10.152.183.114:3000

e

http://10.152.183.113:16686



Boa sorte! Em caso de dúvidas pode abrir um issue ou entra em contato comigo via Linkedin ou Twitter.