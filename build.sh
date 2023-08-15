#!/bin/bash

ROOT=$(dirname $0)
cd $ROOT

ACTION_NAME=mlp-sd-service
BUILD_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BRANCH_NAME_LOWER=`echo $BUILD_BRANCH | tr '[:upper:]' '[:lower:]'`

IMAGE=docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH_NAME_LOWER

#check that mlp-sdk has the same branch
MLP_SDK_HAS_PARALLEL_BRANCH=$(git ls-remote --heads git@gitlab.just-ai.com:ml-platform-pub/mlp-python-sdk.git $BUILD_BRANCH | wc -l)

echo $MLP_SDK_HAS_PARALLEL_BRANCH
if [ $MLP_SDK_HAS_PARALLEL_BRANCH == '1' ]; then
  MLP_SDK_VERSION=${BRANCH_NAME_LOWER}
else
  MLP_SDK_VERSION=dev
fi

export DOCKER_BUILDKIT=1
docker build . -t $IMAGE --build-arg MLP_SDK_VERSION=$MLP_SDK_VERSION --no-cache
docker push $IMAGE
