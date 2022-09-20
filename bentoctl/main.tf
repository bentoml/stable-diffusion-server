terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
}

################################################################################
# Input variable definitions
################################################################################

variable "deployment_name" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "region" {
  type = string
}

variable "ami_id" {
  type = string
}

variable "enable_gpus" {
  type = bool
}

variable "image_repository" {
  type = string
}

variable "image_version" {
  type = string
}

variable "image_tag" {
  type = string
}

################################################################################
# Resource definitions
################################################################################

resource "aws_iam_role" "ec2_role" {
  name = "${var.deployment_name}-iam"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      }
    ]
  })
  inline_policy {
    name = "my_inline_policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "ecr:GetAuthorizationToken",
            "ecr:BatchGetImage",
            "ecr:GetDownloadUrlForLayer"
          ]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }
}

resource "aws_iam_instance_profile" "ip" {
  name = "${var.deployment_name}-instance-profile"
  role = aws_iam_role.ec2_role.name
}


resource "aws_security_group" "allow_bentoml" {
  name        = "${var.deployment_name}-bentoml-sg"
  description = "SG for bentoml server"

  ingress {
    description      = "HTTP for bentoml"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  # add this to open SSH port for the EC2 instance.
  ingress {
    description      = "SSH access for server"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_launch_template" "lt" {
  name                   = "${var.deployment_name}-lt"
  image_id               = var.ami_id
  instance_type          = var.instance_type
  update_default_version = true
  user_data              = filebase64("startup_script.sh")
  security_group_names   = [aws_security_group.allow_bentoml.name]

  iam_instance_profile {
    arn = aws_iam_instance_profile.ip.arn
  }
}

resource "aws_instance" "app_server" {
  key_name = "jithin-test"
  launch_template {
    id = aws_launch_template.lt.id
  }

  provisioner "local-exec" {
    command = <<-EOT
        attempt_counter=0
        max_attempts=20
        printf 'waiting for server to start'
        until $(curl --output /dev/null --silent --head --fail http://${self.public_ip}); do
            if [ $attempt_counter -eq $max_attempts ];then
              echo "Max attempts reached"
              exit 1
            fi

            printf '.'
            attempt_counter=$(($attempt_counter+1))
            sleep 15
        done
        EOT
  }
}

################################################################################
# Output value definitions
################################################################################
output "endpoint" {
  description = "address of ec2 instance created. You can go to that URL to interate with the service"
  value       = "http://${aws_instance.app_server.public_ip}"
}

output "ec2_instance_status" {
  description = "Status of the created instance"
  value       = aws_instance.app_server.instance_state
}
