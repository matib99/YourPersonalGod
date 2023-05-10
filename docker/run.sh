PORT=${PORT:-8080}
DATA_PATH=/home/matib99/Documents/AIART/YourPersonalGod/data
REPO_PATH=/home/matib99/Documents/AIART/YourPersonalGod/src

docker run --gpus 1 -it --rm -e CUDA_VISIBLE_DEVICES --ipc=host -p $PORT:$PORT -v $DATA_PATH:/app/data -v $REPO_PATH:/app/src yourpersonalgod:latest bash