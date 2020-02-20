currentdir=$(echo $(pwd) | sed 's/^\/c\//C:\//g')
export V_ROOT=$currentdir/volumes/
export LFN_ROOT=$currentdir/loganfordnet
docker-compose up --build