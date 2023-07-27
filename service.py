from typing import Optional, Union, List, Any

import torch
import bentoml

from bentoml.io import Image, JSON
from pydantic import BaseModel




class Input(BaseModel):
    prompt: str
    # negative_prompt: Optional[str] = None
    # prompt: Union[str, List[str]] = None
    height: Optional[int] = None
    width: Optional[int] = None
    num_inference_steps: int = 50
    guidance_scale: float = 5.0
    negative_prompt: Optional[Union[str, List[str]]] = None
    num_images_per_prompt: Optional[int] = 1
    return_dict: bool = True
    cross_attention_kwargs: Optional[Dict[str, Any]] = None
    
    class Config:
        extra = "allow"

bento_model = bentoml.diffusers.get("sdxl:latest")



# pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)

# If you are limited by GPU VRAM, you can enable cpu offloading by calling 
#
# - pipe.to("cuda")
# + pipe.enable_model_cpu_offload



svc = bentoml.Service("stable-diffusion-21", runners=[sd21_runner])

input_spec = JSON.from_sample(SDArgs(prompt="a bento box"))

@svc.api(input=input_spec, output=Image())
async def txt2img(input_data):
    kwargs = input_data.dict()
    res = await sd21_runner.async_run(**kwargs)
    images = res[0]
    return images[0]
