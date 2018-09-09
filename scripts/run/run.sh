#!/bin/sh
# Run hoox from docker container

set -e

NAME="kirillsulim/hoox"
VERSION="latest"
IMAGE="$NAME:$VERSION"

# Setup volume mounts
if [ "$(pwd)" != '/' ]; then
    VOLUMES="-v $(pwd):$(pwd)"
fi
if [ -n "$HOME" ]; then
    VOLUMES="$VOLUMES -v $HOME:$HOME"
fi

# Allocate tty if any exists
if [ -t 0 ]; then
    if [ -t 1 ]; then
        DOCKER_RUN_OPTIONS="$DOCKER_RUN_OPTIONS -t"
    fi
else
    DOCKER_RUN_OPTIONS="$DOCKER_RUN_OPTIONS -i"
fi

exec docker run --rm $DOCKER_RUN_OPTIONS $VOLUMES -w "$(pwd)" $IMAGE "$@"
