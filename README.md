# Serving Stable Diffusion with BentoML

<p align="center">
  <img src="https://user-images.githubusercontent.com/861225/191730233-e0786728-0a35-4244-b196-d176a48499e9.png" alt="stable diffusion examples"/>
</p>

[Stable Diffusion](https://stability.ai/blog/stable-diffusion-public-release) is an open-source text-to-image model released by stability.ai. It enables you to generate creative arts from natural language prompts in just seconds. Follow the steps in this repository to create a production-ready Stable Diffusion service with BentoML and deploy it to AWS EC2.


## Prepare the Environment

If you don't wish to build the bento from scratch, feel free to download one of the pre-built bentos.

Clone repository and install dependencies:

```bash
git clone https://github.com/bentoml/stable-diffusion-bentoml.git && cd stable-diffusion-bentoml
python3 -m venv venv && . venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

🎉 Environment is ready!

## Create the Stable Diffusion Bento

Here you can choose to either download pre-built Stable Diffusion bentos or build bentos from the Stable Diffusion models.

### Download Pre-built Stable Diffusion Bentos

- Download fp32 bento (for CPU or GPU with more than 10GB VRAM)

  ```bash
  curl -O https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_fp32.bento && bentoml import ./sd_fp32.bento
  ```

- Download fp16 bento (for GPU with less than 10GB VRAM)

  ```bash
  curl -O https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_fp16.bento && bentoml import ./sd_fp16.bento
  ```

🎉 The Stable Diffusion bento is imported. You can advance to the "Deploy the Stable Diffusion Bento to EC2" section.

### Build from Stable Diffusion Models

Choose a Stable Diffusion model

- fp32 (for CPU or GPU with more than 10GB VRAM)

	```bash
	cd fp32/
	```

- fp16 (for GPU with less than 10GB VRAM)

	```bash
	cd fp16/
	```

Download the Stable Diffusion model

- For fp32 model:

	```bash
	# if tar and gzip is availabe
	curl https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4.tgz | tar zxf - -C models/

	# or if unzip is availabe
	curl -O https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4.zip && unzip -d models/ sd_model_v1_4.zip
	```

- For fp16 model:

	```bash
	# if tar and gzip is availabe
	curl https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4_fp16.tgz | tar zxf - -C models/

	# or if unzip is availabe
	curl -O https://s3.us-west-2.amazonaws.com/bentoml.com/stable_diffusion_bentoml/sd_model_v1_4_fp16.zip && unzip -d models/ sd_model_v1_4_fp16.zip
	```

Run and test the BentoML service:

- Bring up the BentoML service with the following command.

	```bash
	BENTOML_CONFIG=configuration.yaml bentoml serve service:svc --production
	```

- Then you can run one of the scripts to test the service.

	```bash
	../txt2img_test.sh
	../img2img_test.sh
	```

Build a bento:

```bash
bentoml build

Building BentoML service "stable_diffusion_fp32:abclxar26s44kcvj" from build context "/Users/ssheng/github/stable-diffusion-bentoml/fp32"
Locking PyPI package versions..

██████╗░███████╗███╗░░██╗████████╗░█████╗░███╗░░░███╗██╗░░░░░
██╔══██╗██╔════╝████╗░██║╚══██╔══╝██╔══██╗████╗░████║██║░░░░░
██████╦╝█████╗░░██╔██╗██║░░░██║░░░██║░░██║██╔████╔██║██║░░░░░
██╔══██╗██╔══╝░░██║╚████║░░░██║░░░██║░░██║██║╚██╔╝██║██║░░░░░
██████╦╝███████╗██║░╚███║░░░██║░░░╚█████╔╝██║░╚═╝░██║███████╗
╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░░╚════╝░╚═╝░░░░░╚═╝╚══════╝

Successfully built Bento(tag="stable_diffusion_fp32:abclxar26s44kcvj")
```

🎉 The Stable Diffusion bento has been built! You can advance to the "Deploy the Stable Diffusion Bento to EC2" section.

## Deploy the Stable Diffusion Bento to EC2

We will be using [bentoctl](https://github.com/bentoml/bentoctl) to deploy the bento to EC2. bentoctl helps deploy your bentos into any cloud platform easily. Install the AWS EC2 operator to generate and apply Terraform files to EC2.

```
bentoctl operator install aws-ec2
```

The deployment has already been configured for you in the [deployment_config.yaml](https://github.com/bentoml/stable-diffusion-bentoml/blob/main/bentoctl/deployment_config.yaml) file. By default bentoctl is configured to deploy the model on a [g4dn.xlarge](https://aws.amazon.com/ec2/instance-types/g4/) instance with *Deep Learning AMI GPU PyTorch 1.12.0 (Ubuntu 20.04) AMI* on `us-west-1`.

> Note: This default configuration only works in the us-west-1 region. Choose the corresponding AMI Id in your region from [AWS AMI Catalog](https://console.aws.amazon.com/ec2/home#AMICatalog) to deploy to your desired region.

Generate the Terraform files.
```bash
# In the /bentoctl directory
bentoctl generate -f deployment_config.yaml

✨ generated template files.
  - ./main.tf
  - ./bentoctl.tfvars
```


Build the Docker image and push to AWS ECR.
```bash
bentoctl build -b stable_diffusion_fp32:latest -f deployment_config.yaml

🚀 Image pushed!
✨ generated template files.
  - ./bentoctl.tfvars
  - ./startup_script.sh
  
There is also an experimental command that you can use.
To create the resources specifed run this after the build command.
$ bentoctl apply

To cleanup all the resources created and delete the registry run
$ bentoctl destroy
```

Apply the Terraform files to deploy to AWS EC2. Head over to the endpoint URL displayed at the end and you can see your Stable Diffusion service is up and running. Run some test prompts to make sure everything is working.

```bash
bentoctl apply -f deployment_config.yaml

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

ec2_instance_status = "running"
endpoint = "http://53.183.151.211"
```

Finally, delete the deployment if the Stable Diffusion BentoML service is no longer needed.

```bash
bentoctl destroy -f deployment_config.yaml
```
