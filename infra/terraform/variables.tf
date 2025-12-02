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
