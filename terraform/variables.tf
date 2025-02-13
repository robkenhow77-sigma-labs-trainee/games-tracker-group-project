# Define variables used in the config

variable "AWS_ACCESS_KEY" {
    type = string
}

variable "AWS_SECRET_ACCESS_KEY" {
    type = string
}

variable "AWS_REGION" {
    type = string
    default = "eu-west-2"
}

variable "VPC_ID" {
    type = string
}

variable "DB_HOST" {
    type = string  
}

variable "DB_PORT" {
    type = string
}

variable "DB_USERNAME" {
    type = string  
}
variable "DB_PASSWORD" {
    type = string
}

variable "DB_NAME" {
    type = string  
}

variable "ABDI_EMAIL" {
    type = string
}