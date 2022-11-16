import time

import oneflow as torch
from oneflow import autocast

import bentoml
from bentoml.io import Image, JSON, Multipart

class StableDiffusionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", )
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):

        from diffusers import OneFlowStableDiffusionPipeline as StableDiffusionPipeline
        from diffusers import OneFlowStableDiffusionImg2ImgPipeline as StableDiffusionImg2ImgPipeline

        model_id = "./models/v1_4_fp16"
        self.device = "cuda"

        txt2img_pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16")
        self.txt2img_pipe = txt2img_pipe.to(self.device)

        self.img2img_pipe = StableDiffusionImg2ImgPipeline(
            vae=self.txt2img_pipe.vae,
            text_encoder=self.txt2img_pipe.text_encoder,
            tokenizer=self.txt2img_pipe.tokenizer,
            unet=self.txt2img_pipe.unet,
            scheduler=self.txt2img_pipe.scheduler,
            safety_checker=self.txt2img_pipe.safety_checker,
            feature_extractor=txt2img_pipe.feature_extractor,
        ).to(self.device)

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def txt2img(self, input_data):
        prompt = input_data["prompt"]
        guidance_scale = input_data.get('guidance_scale', 7.5)
        height = input_data.get('height', 512)
        width = input_data.get('width', 512)
        num_inference_steps = input_data.get('num_inference_steps', 50)
        start = time.time()
        with autocast(self.device):
            images = self.txt2img_pipe(
                prompt=prompt,
                guidance_scale=guidance_scale,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
            ).images
            print("inference time: ", time.time() - start)
            image = images[0]
            return image


    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def img2img(self, init_image, data):
        new_size = None
        longer_side = max(*init_image.size)
        if longer_side > 512:
            new_size = (512, 512)
        elif init_image.width != init_image.height:
            new_size = (longer_side, longer_side)

        if new_size:
            init_image =init_image.resize(new_size)

        prompt = data["prompt"]
        strength = data.get('strength', 0.8)
        guidance_scale = data.get('guidance_scale', 7.5)
        num_inference_steps = data.get('num_inference_steps', 50)
        with autocast(self.device):
            images = self.img2img_pipe(
                prompt=prompt,
                init_image=init_image,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
            ).images
            image = images[0]
            return image


stable_diffusion_runner = bentoml.Runner(StableDiffusionRunnable, name='oneflow_stable_diffusion_runner', max_batch_size=10)

svc = bentoml.Service("oneflow_stable_diffusion", runners=[stable_diffusion_runner])

@svc.api(input=JSON(), output=Image())
def txt2img(input_data):
    return stable_diffusion_runner.txt2img.run(input_data)

img2img_input_spec = Multipart(img=Image(), data=JSON())
@svc.api(input=img2img_input_spec, output=Image())
def img2img(img, data):
    return stable_diffusion_runner.img2img.run(img, data)
