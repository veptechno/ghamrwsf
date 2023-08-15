#FROM python:3.8
FROM docker-hub.just-ai.com/base/nvidia/nemo:22.05

RUN apt-get update && apt-get upgrade -y &&\
    apt-get install -y --no-install-recommends \

RUN pip install pip==21.3.1

ARG MLP_SDK_VERSION

RUN pip install git+https://gitlab.just-ai.com/ml-platform-pub/mlp-python-sdk@$MLP_SDK_VERSION

RUN rm -rf /usr/local/cuda/lib64/stubs

WORKDIR /app

COPY requirements.txt requirements.txt

ENV USE_TORCH=1

RUN pip install -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cu117

COPY . .

ENTRYPOINT ["python", "main.py"]
