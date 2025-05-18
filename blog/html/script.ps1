docker build -t blog-carolmesqu-app:latest .

docker run -d -p 80:80 blog-carolmesqu-app:latest

az group create --name containerappscarolmesqu --location eastus

az acr login --name blogcarolmesqu

docker tag blog-carolmesqu-app:latest blogcarolmesqu.azurecr.io/blog-carolmesqu-app:latest

docker push blogcarolmesqu.azurecr.io/blog-carolmesqu-app:latest