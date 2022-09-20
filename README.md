<p align="center">
  <h1 align="center">Stable Diffusion Bento</h1>
  <img src="https://user-images.githubusercontent.com/5261489/191204712-a3807af2-948e-46ca-b1bb-acdc7ca0ca07.png" alt="stable diffusion examples"/>
</p>

# todo

## use pre-made bento

todo

## build bento yourself

1. install [huggingface_hub](https://github.com/huggingface/huggingface_hub) and login to you huggingface account because downloading stable diffusion model require your registration:

	```
	pip install huggingface_hub
	huggingface-cli login
	```

2. clone this repository and install dependencies:

	```
	git clone xxx %% cd xxx
	pip install -r requirements.txt
	```

3. download stable diffusion model:

	```
	python download_model.py
	```

	or download fp16 model (if your GPU has less than 10GB VRAM)

	```
	python download_model_fp16.py
	```

4. run and test BentoML server:

	```
	bentoml serve service:svc --production
	```

	or for fp16 model:

	```
	bentoml serve service_fp16:svc --production
	```

	Then you can run `txt2img_test.sh` and `img2img_test.sh` to test the server

5. Build a bento:

	```
	bentoml build
	```

	or for fp16 model:

	```
	bentoml build -f bentofile_fp16.yaml
	```
## Deploy with EC2

We will be using [bentoctl](https://github.com/bentoml/bentoctl) to deploy the bento to EC2. If you want a bit more background on bentoctl check out the [quickstart](https://github.com/bentoml/bentoctl/blob/main/docs/quickstart.md) but everything you need to deploy stable diffusion is mentioned.

1. Generate terraform files
```bash
cd bentoctl
bentoctl generate
```

2. build the docker image for deploying to EC2. After the docker build is complete this will also push the image into your ECR registry.
```bash
bentoctl build -b stable_diffusion_demo:latest
```

3. Apply the changes
```bash
bentoctl apply
```
