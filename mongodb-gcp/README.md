# mongodb--k8s
kubectl create -f mongodb-secrets.yml
kubectl create -f mongodb-statefulset.yaml
kubectl create -f mongodb-service.yml

kubectl delete -f .


CONNECTION STRING
mongosh --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --host mongo-nodeport-svc --port 27017

GO INTO MONGODB POD AND RUN CONNECTION STRING
TO GET DATA FROM DB
use weather_db
db.weather_data.find()