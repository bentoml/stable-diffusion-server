import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

import bentoml
from bentoml.io import Image, JSON

class StableDiffusionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", )
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        model_id = "./models/v1_4_fp16"
        model = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16")
        self.device = "cuda"
        self.model = model.to(self.device)

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def render(self, input_data):
        prompt = input_data["prompt"]
        with autocast(self.device):
            images = self.model(prompt, guidance_scale=7.5).images
            image = images[0]
            return image
                    

stable_diffusion_runner = bentoml.Runner(StableDiffusionRunnable, max_batch_size=10)

svc = bentoml.Service("stable_diffusion_demo_fp16", runners=[stable_diffusion_runner])

@svc.api(input=JSON(), output=Image())
def render(input_data):
    return stable_diffusion_runner.run(input_data)
