import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionImg2ImgPipeline

from pydantic import BaseModel
import bentoml
from bentoml.io import Image, JSON, Multipart

class StableDiffusionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", )
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        model_id = "./models/v1_4_fp16"
        self.device = "cuda"

        txt2img_pipe = StableDiffusionPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, revision="fp16"
        )
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

        self.inpaint_pipe = StableDiffusionInpaintPipeline(
            vae=self.txt2img_pipe.vae,
            text_encoder=self.txt2img_pipe.text_encoder,
            tokenizer=self.txt2img_pipe.tokenizer,
            unet=self.txt2img_pipe.unet,
            scheduler=self.txt2img_pipe.scheduler,
            safety_checker=self.txt2img_pipe.safety_checker,
            feature_extractor=self.txt2img_pipe.feature_extractor,
        ).to(self.device)

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def txt2img(self, data):
        prompt = data["prompt"]
        guidance_scale = data.get('guidance_scale', 7.5)
        height = data.get('height', 512)
        width = data.get('width', 512)
        num_inference_steps = data.get('num_inference_steps', 50)
        generator = torch.Generator(self.device)
        generator.manual_seed(data.get('seed'))
        negative_prompt = data.get('negative_prompt', None)

        if not data['safety_check']:
            self.txt2img_pipe.safety_checker = lambda images, **kwargs: (images, False)

        with ExitStack() as stack:
            if self.device != "cpu":
                _ = stack.enter_context(autocast(self.device))

            images = self.txt2img_pipe(
                prompt=prompt,
                guidance_scale=guidance_scale,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
                generator=generator,
                negative_prompt=negative_prompt,
            ).images
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
        generator = torch.Generator(self.device)
        generator.manual_seed(data.get('seed'))
        negative_prompt = data.get('negative_prompt', None)

        if not data['safety_check']:
            self.img2img_pipe.safety_checker = lambda images, **kwargs: (images, False)

        with ExitStack() as stack:
            if self.device != "cpu":
                _ = stack.enter_context(autocast(self.device))

            images = self.img2img_pipe(
                prompt=prompt,
                init_image=init_image,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                generator=generator,
                negative_prompt=negative_prompt,
            ).images
            image = images[0]
            return image

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def inpaint(self, image, mask, data):
        prompt = data["prompt"]
        strength = data.get('strength', 0.8)
        guidance_scale = data.get('guidance_scale', 7.5)
        num_inference_steps = data.get('num_inference_steps', 50)
        generator = torch.Generator(self.device)
        generator.manual_seed(data.get('seed'))
        negative_prompt = data.get('negative_prompt', None)

        if not data['safety_check']:
            self.inpaint_pipe.safety_checker = lambda images, **kwargs: (images, False)

        with ExitStack() as stack:
            if self.device != "cpu":
                _ = stack.enter_context(autocast(self.device))

            images = self.inpaint_pipe(
                prompt=prompt,
                init_image=image,
                mask_image=mask,
                strength=strength,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=generator,
                negative_prompt=negative_prompt,
            ).images
            image = images[0]
            return image

stable_diffusion_runner = bentoml.Runner(StableDiffusionRunnable, name='stable_diffusion_runner', max_batch_size=10)

svc = bentoml.Service("stable_diffusion_fp16", runners=[stable_diffusion_runner])

def generate_seed_if_needed(seed):
    if seed is None:
        generator = torch.Generator()
        seed = torch.seed()
    return seed

class Txt2ImgInput(BaseModel):
    prompt: str
    guidance_scale: float = 7.5
    height: int = 512
    width: int = 512
    num_inference_steps: int = 50
    safety_check: bool = True
    seed: int = None
    negative_prompt: str = None

@svc.api(input=JSON(pydantic_model=Txt2ImgInput), output=Image())
def txt2img(data, context):
    data = data.dict()
    data['seed'] = generate_seed_if_needed(data['seed'])
    image = stable_diffusion_runner.txt2img.run(data)
    for i in data:
        context.response.headers.append(i, str(data[i]))
    return image

class Img2ImgInput(BaseModel):
    prompt: str
    strength: float = 0.8
    guidance_scale: float = 7.5
    num_inference_steps: int = 50
    safety_check: bool = True
    seed: int = None
    negative_prompt: str = None

img2img_input_spec = Multipart(img=Image(), data=JSON(pydantic_model=Img2ImgInput))
@svc.api(input=img2img_input_spec, output=Image())
def img2img(img, data, context):
    data = data.dict()
    data['seed'] = generate_seed_if_needed(data['seed'])
    image = stable_diffusion_runner.img2img.run(img, data)
    for i in data:
        context.response.headers.append(i, str(data[i]))
    return image

inpaint_input_spec = Multipart(img=Image(), mask=Image(), data=JSON(pydantic_model=Img2ImgInput))
@svc.api(input=inpaint_input_spec, output=Image())
def inpaint(img, mask, data, context):
    data = data.dict()
    data['seed'] = generate_seed_if_needed(data['seed'])
    image = stable_diffusion_runner.inpaint.run(img, mask, data)
    for i in data:
        context.response.headers.append(i, str(data[i]))
    return image