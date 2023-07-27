import bentoml
import torch
import diffusers


bentoml.diffusers.import_model(
    "sdxl",  # model tag in BentoML model store
    "stabilityai/stable-diffusion-xl-base-1.0",  # huggingface model card 
    variant="fp16",
    pipeline_class=diffusers.pipelines.DiffusionPipeline
)
