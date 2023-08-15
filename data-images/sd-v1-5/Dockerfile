FROM alpine:3.18.3

RUN apk update \
    && apk upgrade \
    && apk add build-base git git-lfs \
    && git lfs install \

RUN mkdir /resources
RUN git clone https://huggingface.co/runwayml/stable-diffusion-v1-5 /resources
