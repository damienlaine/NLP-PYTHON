# Start service (mongo-redis) localement (accesible seulement via le docker network (linto-net))
docker-compose -f docker-compose-service.yml up

# LAUNCH 
cd ~/git/linto-platform-nlp-services
docker-compose up


# Start nlp-service
docker-compose build




