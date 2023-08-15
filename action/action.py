import base64
from io import BytesIO

import logging
import sys
from threading import Lock
from typing import List

from diffusers import DiffusionPipeline
from mlp_sdk.abstract import Task
from mlp_sdk.grpc import mlp_grpc_pb2
from mlp_sdk.log.setup_logging import get_logger
from mlp_sdk.transport.MlpServiceSDK import MlpServiceSDK
from pydantic import BaseModel
from pydantic import Field

logger = get_logger(__name__)

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] - %(message)s',
                    level='DEBUG',
                    stream=sys.stdout)


class TextsCollection(BaseModel):
    texts: List[str]


class SdInitConfig(BaseModel):
    device: str = Field("cuda:0")
    model_path: str = Field("/resources")


class SdResponse(BaseModel):
    images_base64: List[str]


class MlpSdService(Task):
    def __init__(self, config: SdInitConfig, service_sdk: MlpServiceSDK = None):
        super().__init__(config, service_sdk)
        logger.info(f'Initializing MlpSdService, {config=}')

        self.generator = DiffusionPipeline.from_pretrained(config.model_path)
        self.generator.to("cuda")
        self.inference_lock = Lock()

    def get_schema(self):
        return {"main.proto": "content of a file"}

    def get_descriptor(self):
        return mlp_grpc_pb2.ServiceDescriptorProto(
            name="example",
            fittable=False,
            methods={"predict": mlp_grpc_pb2.MethodDescriptorProto(
                input={
                    "data": mlp_grpc_pb2.ParamDescriptorProto(type="TextsCollection"),
                    "config": mlp_grpc_pb2.ParamDescriptorProto(type="TextsCollection"),
                },
                output=mlp_grpc_pb2.ParamDescriptorProto(type="TextsCollection"),
            ),
                "ext.echo": mlp_grpc_pb2.MethodDescriptorProto(
                    input={
                        "data": mlp_grpc_pb2.ParamDescriptorProto(type="TextsCollection"),
                    },
                    output=mlp_grpc_pb2.ParamDescriptorProto(type="TextsCollection"),
                )}
        )

    def predict(self, data: TextsCollection, config: TextsCollection) -> SdResponse:
        logger.info('Start processing text2img request...', extra=data.dict())

        logger.info('Получили запрос для обработки')

        logger.info('Берём лок для обработки')
        with self.inference_lock:
            logger.info('Взяли его. Теперь с помощью list comprehension обработаем каждый запрос')
            images = [self.generate(text) for text in data.texts]
            logger.info(f'Сгенерили все картинки (WoW) в количестве {len(images)}')

        return SdResponse(images_base64=images)

    def generate(self, prompt: str) -> str:
        logger.info(f'Начинаем генерацию изображения для промпта {prompt}')

        try:
            result = self.generator(prompt)
        except Exception as e:
            logger.error("Печаль беда, поймали исключение когда генерили картинку")
            logger.exception(e)
            raise e

        try:
            image = result.images[0]
        except Exception as e:
            logger.error("Печаль беда, исключение когда пытались из result взять первую картинку")
            logger.exception(e)
            logger.error(f'Вот result: {result.dict()}')
            raise e

        try:
            buffered = BytesIO()
            image.save(buffered, format="png")
            bytes_64 = base64.b64encode(buffered.getvalue())
            return self.__bytes_to_b64_string(bytes_64)
        except Exception as e:
            logger.error("Печаль беда, исключение когда пытались сконвертировать всё в base64")
            logger.exception(e)
            raise e

    @staticmethod
    def __bytes_to_b64_string(b: bytes) -> str:
        return base64.b64encode(b).decode(encoding='utf-8')


def main():
    mlp = MlpServiceSDK()
    mlp.register_impl(MlpSdService())
    mlp.start()
    mlp.block_until_shutdown()


if __name__ == "__main__":
    main()
