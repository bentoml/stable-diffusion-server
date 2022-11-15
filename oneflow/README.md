A machine with cuda 11.2 (or higher) is required.

Make a venv and install dependencies:

```bash
python3 -m venv venv && . venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Download FP16 model

```bash
# if tar and gzip is availabe
curl https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4_fp16.tgz | tar zxf - -C models/

# or if unzip is availabe
curl -O https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4_fp16.zip && unzip -d models/ sd_model_v1_4_fp16.zip
```

Run and test the BentoML service:

- Bring up the BentoML service with the following command.

	```bash
	bentoml serve service:svc --production
	```

- Then you can run one of the scripts to test the service.

	```bash
	../txt2img_test.sh
	../img2img_test.sh
	```

Build a bento:

```bash
bentoml build
```

