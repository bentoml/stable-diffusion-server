import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

import bentoml
from bentoml.io import Image, JSON

class StableDiffusionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        model_id = "./models/v1_4"
        model = StableDiffusionPipeline.from_pretrained(model_id)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = model.to(self.device)

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def render(self, input_data):
        prompt = input_data["prompt"]
        if self.device == "cpu":
            images = self.model(prompt, guidance_scale=7.5).images
            image = images[0]
            return image
                    
        with autocast(self.device):
            images = self.model(prompt, guidance_scale=7.5).images
            image = images[0]
            return image
                    

stable_diffusion_runner = bentoml.Runner(StableDiffusionRunnable, max_batch_size=10)

svc = bentoml.Service("stable_diffusion_demo", runners=[stable_diffusion_runner])

@svc.api(input=JSON(), output=Image())
def txt2img(input_data):
    return stable_diffusion_runner.run(input_data)
