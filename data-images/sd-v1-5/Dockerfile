FROM alpine:3.18.3 as clone

RUN apk update \
    && apk upgrade \
    && apk add build-base git git-lfs \
    && git lfs install \

RUN mkdir ./resources
RUN git clone https://huggingface.co/runwayml/stable-diffusion-v1-5 ./resources

FROM alpine:3.18.3

RUN mkdir ./resources
COPY --from=clone /resources/vae /resources/vae
COPY --from=clone /resources/unet /resources/unet
COPY --from=clone /resources/tokenizer /resources/tokenizer
COPY --from=clone /resources/scheduler /resources/scheduler
COPY --from=clone /resources/text_encoder /resources/text_encoder
COPY --from=clone /resources/safety_checker /resources/safety_checker
COPY --from=clone /resources/feature_extractor /resources/feature_extractor


COPY --from=clone /resources/model_index.json /resources/model_index.json
COPY --from=clone /resources/v1-inference.yaml /resources/v1-inference.yaml

COPY --from=clone /resources/v1-5-pruned.ckpt /resources/v1-5-pruned.ckpt
COPY --from=clone /resources/v1-5-pruned.safetensors /resources/v1-5-pruned.safetensors
COPY --from=clone /resources/v1-5-pruned-emaonly.ckpt /resources/v1-5-pruned-emaonly.ckpt
COPY --from=clone /resources/v1-5-pruned-emaonly.safetensors /resources/v1-5-pruned-emaonly.safetensors
