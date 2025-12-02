variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_slug" {
  description = "Prefixo dos recursos"
  type        = string
  default     = "always-free"
}

variable "extra_tags" {
  description = "Tags adicionais aplicadas a todos os recursos"
  type        = map(string)
  default     = {}
}

variable "db_username" {
  description = "Usuário Postgres"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Senha Postgres (use SSM em produção)"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "Classe do RDS (compatível com free tier: db.t4g.micro)"
  type        = string
  default     = "db.t4g.micro"
}

variable "db_allocated_storage" {
  description = "Armazenamento (GB) do banco"
  type        = number
  default     = 20
}

variable "db_engine_version" {
  description = "Versão do Postgres"
  type        = string
  default     = "15.4"
}

variable "vpc_cidr" {
  description = "CIDR do VPC"
  type        = string
  default     = "10.42.0.0/16"
}

variable "dataset_bucket_force_destroy" {
  description = "Se true, permite destruir bucket mesmo com objetos"
  type        = bool
  default     = false
}

variable "container_image" {
  description = "Imagem do container backend publicada no ECR ou registry público"
  type        = string
  default     = "public.ecr.aws/docker/library/node:20-alpine"
}

variable "container_port" {
  description = "Porta exposta pelo container"
  type        = number
  default     = 4000
}

variable "container_cpu" {
  description = "CPU para o task definition (unidades ECS)"
  type        = number
  default     = 512
}

variable "container_memory" {
  description = "Memória (MB) para o task definition"
  type        = number
  default     = 1024
}

variable "desired_count" {
  description = "Número de tasks Fargate simultâneas"
  type        = number
  default     = 1
}
