import os
import torch
from diffusers import StableDiffusionPipeline

def main():
    model_id = "CompVis/stable-diffusion-v1-4"
    save_path = "./models/v1_4_fp16"
    if os.path.exists(save_path):
        print(f"save path {save_path} already exists, delete it to re-import the model")
        return
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16, revision="fp16", use_auth_token=True
    )
    pipe.save_pretrained(save_path)


if __name__ == "__main__":
    main()
