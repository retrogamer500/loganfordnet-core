Start docker:

export V_ROOT="C:/Users/Logan/Documents/loganfordnet/volumes"
docker-compose up --build

Restart everything:

docker-compose down
docker rmi $(docker images -a -q)
docker system prune --volumes