<p align="center">
  <h1 align="center">Stable Diffusion Bento</h1>
  <img src="https://user-images.githubusercontent.com/5261489/191204712-a3807af2-948e-46ca-b1bb-acdc7ca0ca07.png" alt="stable diffusion examples"/>
</p>

# todo

## use pre-made bento

todo

## build bento yourself

1. clone this repository and install dependencies:

	```
	git clone https://github.com/bentoml/stable-diffusion-bentoml.git && cd stable-diffusion-bentoml
	python3 -m venv venv && . venv/bin/activate
	pip install -U pip
	pip install -r requirements.txt
	```

2. select fp32 (for GPU card with more than 10GB VRAM or CPU only) or fp16 (for GPU card with less than 10GB VRAM)

	```
	cd fp32/
	```

	or for fp16

	```
	cd fp16/
	```

3. download stable diffusion model:

	for fp32 model:

	```
	# if tar and gzip is availabe
	curl https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4.tgz | tar zxf - -C models/

	# or if unzip is availabe
	curl -O https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4.zip && unzip -d models/ sd_model_v1_4.zip
	```

	for fp16 model:

	```
	# if tar and gzip is availabe
	curl https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4_fp16.tgz | tar zxf - -C models/

	# or if unzip is availabe
	curl -O https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4_fp16.zip && unzip -d models/ sd_model_v1_4_fp16.zip
	```

4. run and test BentoML server:

	```
	bentoml serve service:svc --production
	```

	Then you can run `../txt2img_test.sh` and `../img2img_test.sh` to test the server

5. Build a bento:

	```
	bentoml build
	```

## Deploy to EC2

We will be using [bentoctl](https://github.com/bentoml/bentoctl) to deploy the bento to EC2. Bentoctl helps deploy your bentos into any cloud platform easily. It creates and configures the terraform files to deploy into the cloud platform. If you want a bit more background on bentoctl check out the [quickstart](https://github.com/bentoml/bentoctl/blob/main/docs/quickstart.md). Follow the steps to deploy the stable-diffusion model into EC2.

1. Generate Terraform Files: The deployment has already been configured for you in ./bentoctl/deployment_config.yaml file. By default bentoctl is configured to deploy the model on a [g4dn.2xlarge](https://aws.amazon.com/ec2/instance-types/g4/) instance with *Deep Learning AMI GPU PyTorch 1.12.0 (Ubuntu 20.04) AMI* on us-west-1.

> Note: This default configuration only works in the us-west-1 region. Choose the corresponding AMI Id in your region from [AWS AMI Catalog](https://console.aws.amazon.com/ec2/home#AMICatalog) to deploy to your desired region.

```bash
cd bentoctl
bentoctl generate
```

2. Build Docker Image: Will containerize the bento and push it into the default ECR for the region
```bash
bentoctl build -b stable_diffusion_demo:latest
```

3. Apply the Terraform Files: will install the required terraform providers and modules and run `terraform plan` and `terraform apply` command on your behalf. It might take a while for all the resources to be created, a nice oppertunity to get some coffee :).
```bash
bentoctl apply
```

4. Head over to the endpoint URL displayed at the end and you can see your stable diffusion service up and running. Run some test prompts to make sure everything is working.
