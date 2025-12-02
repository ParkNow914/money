terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Optional networking skeleton (commented)
# module "vpc" {
#   source  = "terraform-aws-modules/vpc/aws"
#   name    = "always-free-vpc"
#   cidr    = "10.42.0.0/16"
#   azs     = ["${var.aws_region}a", "${var.aws_region}b"]
#   public_subnets  = ["10.42.1.0/24", "10.42.2.0/24"]
#   private_subnets = ["10.42.11.0/24", "10.42.12.0/24"]
#   enable_dns_hostnames = true
# }

# Placeholder RDS (free tier compatible)
# resource "aws_db_instance" "ledger" {
#   identifier           = "always-free-ledger"
#   engine               = "postgres"
#   instance_class       = "db.t4g.micro"
#   allocated_storage    = 20
#   skip_final_snapshot  = true
#   publicly_accessible  = false
#   username             = var.db_username
#   password             = var.db_password
#   vpc_security_group_ids = []
#   depends_on = [module.vpc]
# }

# Static asset bucket skeleton
# resource "aws_s3_bucket" "static_site" {
#   bucket = "${var.project_slug}-static"
#   force_destroy = false
#   tags = {
#     Project = var.project_slug
#   }
# }

# Optional EKS cluster placeholder
# module "eks" {
#   source          = "terraform-aws-modules/eks/aws"
#   cluster_name    = "${var.project_slug}-eks"
#   cluster_version = "1.28"
#   subnets         = module.vpc.private_subnets
#   vpc_id          = module.vpc.vpc_id
# }

output "manual_next_steps" {
  value = "Preencha variáveis em variables.tf e descomente módulos conforme necessidade."
}
