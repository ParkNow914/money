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

data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  azs = slice(data.aws_availability_zones.available.names, 0, 2)
  tags = merge({
    Project     = var.project_slug
    Environment = "always-free"
    ManagedBy   = "terraform"
    Owner       = data.aws_caller_identity.current.account_id
  }, var.extra_tags)
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name    = "${var.project_slug}-vpc"
  cidr    = var.vpc_cidr
  azs     = local.azs

  public_subnets  = [for idx, az in local.azs : cidrsubnet(var.vpc_cidr, 4, idx)]
  private_subnets = [for idx, az in local.azs : cidrsubnet(var.vpc_cidr, 4, idx + 4)]

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = local.tags
}

# S3 bucket for datasets/static assets
resource "aws_s3_bucket" "datasets" {
  bucket        = "${var.project_slug}-datasets-${data.aws_caller_identity.current.account_id}"
  force_destroy = var.dataset_bucket_force_destroy
  tags          = local.tags
}

resource "aws_s3_bucket_public_access_block" "datasets" {
  bucket = aws_s3_bucket.datasets.id

  block_public_acls   = true
  block_public_policy = true
  restrict_public_buckets = true
  ignore_public_acls      = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "datasets" {
  bucket = aws_s3_bucket.datasets.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# CloudWatch log group for the API service
resource "aws_cloudwatch_log_group" "api" {
  name              = "/aws/ecs/${var.project_slug}-api"
  retention_in_days = 14
  tags              = local.tags
}

# IAM roles for ECS tasks
resource "aws_iam_role" "ecs_task_execution" {
  name               = "${var.project_slug}-ecs-exec"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume_role.json
  tags               = local.tags
}

data "aws_iam_policy_document" "ecs_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role_policy_attachment" "ecs_execution_default" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_cluster" "backend" {
  name = "${var.project_slug}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = local.tags
}

resource "aws_lb" "api" {
  name               = "${var.project_slug}-alb"
  load_balancer_type = "application"
  subnets            = module.vpc.public_subnets
  security_groups    = [aws_security_group.alb.id]
  tags               = local.tags
}

resource "aws_security_group" "alb" {
  name        = "${var.project_slug}-alb-sg"
  description = "Allow HTTP ingress"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.tags
}

resource "aws_security_group" "ecs_service" {
  name        = "${var.project_slug}-ecs-sg"
  description = "Allow traffic from ALB"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = var.container_port
    to_port         = var.container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.tags
}

resource "aws_lb_target_group" "api" {
  name     = "${var.project_slug}-tg"
  port     = var.container_port
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    matcher             = "200"
  }

  target_type = "ip"
  tags        = local.tags
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.api.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

resource "aws_ecs_task_definition" "api" {
  family                   = "${var.project_slug}-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.container_cpu
  memory                   = var.container_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name      = "backend"
      image     = var.container_image
      essential = true
      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]
      environment = [
        { name = "NODE_ENV", value = "production" },
        { name = "PORT", value = tostring(var.container_port) }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.api.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])

  tags = local.tags
}

resource "aws_ecs_service" "api" {
  name            = "${var.project_slug}-svc"
  cluster         = aws_ecs_cluster.backend.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = module.vpc.private_subnets
    assign_public_ip = false
    security_groups  = [aws_security_group.ecs_service.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "backend"
    container_port   = var.container_port
  }

  lifecycle {
    ignore_changes = [desired_count]
  }

  depends_on = [aws_lb_listener.http]
  tags       = local.tags
}

# Postgres for ledger/quotas (can stay in free tier)
resource "aws_db_subnet_group" "ledger" {
  name       = "${var.project_slug}-db-subnets"
  subnet_ids = module.vpc.private_subnets
  tags       = local.tags
}

resource "aws_security_group" "rds" {
  name        = "${var.project_slug}-rds-sg"
  description = "Allow ECS to talk to Postgres"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_service.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.tags
}

resource "aws_db_instance" "ledger" {
  identifier              = "${var.project_slug}-ledger"
  engine                  = "postgres"
  engine_version          = var.db_engine_version
  instance_class          = var.db_instance_class
  allocated_storage       = var.db_allocated_storage
  db_subnet_group_name    = aws_db_subnet_group.ledger.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  username                = var.db_username
  password                = var.db_password
  publicly_accessible     = false
  backup_retention_period = 7
  skip_final_snapshot     = true
  storage_encrypted       = true
  tags                    = local.tags
}
