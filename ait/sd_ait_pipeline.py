import torch

from diffusers import StableDiffusionPipeline


class SDAITPipeline(StableDiffusionPipeline):
    def __init__(self):
        super().__init__()
