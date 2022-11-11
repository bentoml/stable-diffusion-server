import torch
from torch import autocast


import bentoml

from sd_ait_pipeline import SDAITPipeline


class SDAITRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", )
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        self.device = "cuda"
        mode_id = "./models/v1_4_fp16"
        aitpipeline = SDAITPipeline.from_pretrained(mode_id, torch_dtype=torch.float16, revision="fp16")
        self.pipeline = aitpipeline.to(self.device)

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def txt2img(self, input_data):
        prompt = input_data["prompt"]
        guidance_scale = input_data.get('guidance_scale', 7.5)
        height = input_data.get('height', 512)
        width = input_data.get('width', 512)
        num_inference_steps = input_data.get('num_inference_steps', 50)
        with autocast(self.device):
            images = self.pipeline(
                prompt=prompt,
                guidance_scale=guidance_scale,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
            ).images
            image = images[0]
            return image
