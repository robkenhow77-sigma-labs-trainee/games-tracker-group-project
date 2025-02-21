<img src="https://raw.githubusercontent.com/robkenhow77-sigma-labs-trainee/games-tracker-group-project/refs/heads/main/dashboard/logo.png" alt="Logo" style="width:25%; height:auto;">

# Terraform

[Terraform](https://www.terraform.io/) is a service which allows for the requisitioning of cloud resources from code.
[Terraform](https://www.terraform.io/) will need to installed by following the instructions from the [website](https://www.terraform.io/). Inside this folder there are `.tf` files that create the resources. 

If you wish to [Terraform](https://www.terraform.io/) first, make sure you know what terraform is and how it works. Then in this folder type `vim variables.tfvars`, go into edit mode by pressing `i` and add

YOU WILL NEED TO CHANGE VALUES THROUGHOUT THIS CODE
AS THIS IS BEING HOSTED ON THE CLOUD THIS WILL COST MONEY.

## How to use

```
AWS_ACCESS_KEY = "[Your AWS access key]"
AWS_SECRET_ACCESS_KEY = "[Your AWS secret key]"
VPC_ID = "[Your VPC ID]"
DB_HOST = "[Your database host url]"
DB_PORT = [Your database access port]
DB_PASSWORD = "[Your database password]"
DB_USERNAME = "[Your database name]"
DB_NAME = "[Your database name]"
SNS_TOPIC_ARN = "[Your SNS topic ARN]"
```

followed by `esc` then type `wq!` to save those changes and quit out of vim.
You will now need to run `terraform plan` and `terraform apply` to create the resources.
Please note, this will not create the ECR which will need to be done through the AWS UI. You will need [Docker](https://www.docker.com/) or equivalent to containerise the program and put it on the ECR, we have included the required Dockerfiles for this.

Type `terraform init` followed by `terraform plan` to see what this terraform folder will create. Then type `terraform apply` when you are happy with what will be made.

## Files

The files are broken up into the parts of the architecture they make.

`daily_genre_releases.tf` for example contains all the parts related to the genre emails that are sent out daily to subscribers of the SNS.

dashboard.tf will build all parts related to running the dashboard.

And so on.
