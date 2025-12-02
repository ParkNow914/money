output "region" {
  value       = var.aws_region
  description = "Região usada para recursos"
}

output "static_bucket" {
  value       = "${var.project_slug}-static"
  description = "Nome sugerido do bucket S3"
}
