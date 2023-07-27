# Serving Stable Diffusion with BentoML

<p align="center">
  <img src="https://user-images.githubusercontent.com/861225/191730233-e0786728-0a35-4244-b196-d176a48499e9.png" alt="stable diffusion examples"/>
</p>

[Stable Diffusion](https://stability.ai/blog/stable-diffusion-public-release) is an open-source text-to-image model released by stability.ai. It enables you to generate creative arts from natural language prompts in just seconds. Follow the steps in this repository to create a production-ready Stable Diffusion service with BentoML and deploy it to AWS EC2.


## Prepare the Environment

Clone repository and install dependencies:

```bash
git clone https://github.com/bentoml/stable-diffusion-bentoml.git && cd stable-diffusion-bentoml
python3 -m venv venv && . venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```


## Launch a local StableDiffusion Server

### Download Models



### Launch Local Server

Bring up the BentoML service with the following command.

```bash
BENTOML_CONFIG=configuration.yaml bentoml serve service:svc --production
```

Then you can run one of the scripts to test the service.

```bash
../txt2img_test.sh
../img2img_test.sh
```

## Deploying to Production

### Building a Bento


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

### Deploy to BentoCloud


..


## Community



