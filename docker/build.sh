DIR=$( dirname -- "$0"; )
parentdir="$(dirname "$DIR")"
docker build -f $DIR/Dockerfile -t yourpersonalgod:latest $parentdir 