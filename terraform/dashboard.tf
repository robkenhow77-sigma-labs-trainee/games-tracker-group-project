# Steps to make the Dashboard work in AWS as an ECS Fargate Task
data "aws_vpc" "c15_vpc" {
    id = var.VPC_ID
}

data "aws_iam_role" "ecs_service_execution_role" {
    name = "ecsTaskExecutionRole"
}

data "aws_ecr_repository" "play-stream-dashboard-ecr" {
    name = "c15-play-stream-dashboard-ecr"
}

data "aws_ecr_image" "dashboard-latest-image" {
    repository_name = data.aws_ecr_repository.play-stream-dashboard-ecr.name
    most_recent = true
}

# Making the Task Definition for the Dashboard

resource "aws_ecs_task_definition" "play-stream-dashboard-task" {

    family                      = "c15-play-stream-dashboard-task-definition"
    network_mode                = "awsvpc"
    requires_compatibilities    = ["FARGATE"]
    cpu                         = "256"
    memory                      = "512"
    execution_role_arn          = data.aws_iam_role.ecs_service_execution_role.arn

    container_definitions = jsonencode([{
        name        = "c15-play-stream-dashboard-task-definition"
        image       = data.aws_ecr_image.dashboard-latest-image.image_uri
        cpu         = 256
        memory      = 512
        essential   = true

        portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        },
        {
          containerPort = 443
          hostPort      = 443
          protocol      = "tcp"
        },
        {
          containerPort = 1433
          hostPort      = 1433
          protocol      = "tcp"
        },
        {
          containerPort = 8501
          hostPort      = 8501
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/c15-play-stream-dashboard-task-definition"
          "awslogs-region"        = var.AWS_REGION
          "awslogs-stream-prefix" = "ecs"
          "awslogs-create-group"  = "true"
        }
      }

      environment = [
        { name = "DB_HOST", value = var.DB_HOST },
        { name = "DB_USER", value = var.DB_USERNAME },
        { name = "DB_PASSWORD", value = var.DB_PASSWORD },
        { name = "DB_NAME", value = var.DB_NAME },
        { name = "DB_PORT", value = var.DB_PORT }
      ]
    }
    ])

    runtime_platform {
        operating_system_family = "LINUX"
        cpu_architecture       = "X86_64"
    }
}

# Making the security group for the Task Definition

resource "aws_security_group" "ecs_security_group" {
    name = "c15-play-stream-task-def-security-group"
    vpc_id = data.aws_vpc.c15_vpc.id

    ingress {
        from_port   = 1433
        to_port     = 1433
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]  
    }

    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 8501
        to_port     = 8501
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# Giving the information about the resources needed for the ECS to run

data "aws_ecs_cluster" "c15-cluster" {
  cluster_name = "c15-ecs-cluster"
}

# The three public subnets for Cohort 15 in AWS

data "aws_subnet" "public-subnet1" {
  id = "subnet-09963d73cb3483abe"
}

data "aws_subnet" "public-subnet2" {
  id = "subnet-08b00202ae83c58a8"
}

data "aws_subnet" "public-subnet3" {
  id = "subnet-0a007e7162fab0ba2"
}

# Making the ECS for the Dashboard to run as a service on the C15 cluster

resource "aws_ecs_service" "play-stream-dashboard-service" {
    name                = "c15-play-stream-dashboard-service"
    cluster             = data.aws_ecs_cluster.c15-cluster.id
    task_definition     = aws_ecs_task_definition.play-stream-dashboard-task.arn
    launch_type         = "FARGATE"
    desired_count       = 1

    network_configuration {
        subnets       =   [data.aws_subnet.public-subnet1.id, 
                        data.aws_subnet.public-subnet2.id, 
                        data.aws_subnet.public-subnet3.id]
        security_groups = [aws_security_group.ecs_security_group.id]
        assign_public_ip = true
    }

    depends_on = [ aws_ecs_task_definition.play-stream-dashboard-task ]
}