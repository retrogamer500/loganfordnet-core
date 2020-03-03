DOCKER_COMPOSE_ARGS=""
DOWN=0

while getopts ":bd" opt; do
    case ${opt} in
        b ) DOCKER_COMPOSE_ARGS="--build" && echo "Rebuilding docker containers" ;;
        d ) DOWN=1 && echo "Starting from scratch" ;;
        \? ) echo "Usage: cmd [-b]" ;;
    esac
done

CURRENT_DIR=$(echo $(pwd) | sed 's/^\/c\//C:\//g')
export V_ROOT=$CURRENT_DIR/volumes/
export LFN_ROOT=$CURRENT_DIR/loganfordnet

if [ $DOWN -eq "1" ]; then
    docker-compose down
    docker rmi $(docker images -a -q)
    docker system prune --volumes -f
    docker rmi $(docker images -a -q)
    rm -rf ./volumes/
fi

docker-compose up $DOCKER_COMPOSE_ARGS