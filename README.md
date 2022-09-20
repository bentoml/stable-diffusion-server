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
