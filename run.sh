DOCKER_COMPOSE_ARGS=""

while getopts ":b" opt; do
    case ${opt} in
        b ) DOCKER_COMPOSE_ARGS="--build" && echo "Rebuilding docker containers" ;;
        \? ) echo "Usage: cmd [-b]" ;;
    esac
done

CURRENT_DIR=$(echo $(pwd) | sed 's/^\/c\//C:\//g')
export V_ROOT=$CURRENT_DIR/volumes/
export LFN_ROOT=$CURRENT_DIR/loganfordnet
docker-compose up $DOCKER_COMPOSE_ARGS