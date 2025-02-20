# # Selecting the cloud provider
# provider "aws" {
#   access_key = var.AWS_ACCESS_KEY
#   secret_key = var.AWS_SECRET_ACCESS_KEY
#   region = var.AWS_REGION
# }

# data "aws_vpc" "c15-vpc" {
#   id = var.VPC_ID
# }

# data "aws_db_subnet_group" "c15-public-group" {
#   name = "c15-public-subnet-group"
# }


# # Security Group

# resource "aws_security_group" "db-security-group" {
#   name = "c15-play-stream-db-sg"
#   vpc_id = data.aws_vpc.c15-vpc.id
# }

# # Security group rules

# resource "aws_vpc_security_group_ingress_rule" "postgres_receive" {
#   security_group_id = aws_security_group.db-security-group.id
#   ip_protocol = "tcp"
#   from_port = 5432
#   to_port = 5432
#   cidr_ipv4 = "0.0.0.0/0"
# }

# resource "aws_vpc_security_group_egress_rule" "postgres_send" {
#   security_group_id = aws_security_group.db-security-group.id
#   ip_protocol = "tcp"
#   from_port = 5432
#   to_port = 5432
#   cidr_ipv4 = "0.0.0.0/0"
# }

# # Database

# resource "aws_db_instance" "games-tracker-db" {
#     allocated_storage            = 10
#     db_name                      = "games_tracker"
#     identifier                   = "c15-play-stream-games-tracker-db"
#     engine                       = "postgres"
#     engine_version               = "16"
#     instance_class               = "db.t3.micro"
#     publicly_accessible          = true
#     performance_insights_enabled = false
#     skip_final_snapshot          = true
#     db_subnet_group_name         = data.aws_db_subnet_group.c15-public-group.name
#     vpc_security_group_ids       = [aws_security_group.db-security-group.id]
#     username                     = var.DB_USERNAME
#     password                     = var.DB_PASSWORD
# }