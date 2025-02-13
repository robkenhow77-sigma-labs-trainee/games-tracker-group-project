# games-tracker-group-project

### terraform/

- If you wish to [terraform](https://www.terraform.io/) the required resources go into the `terraform` folder and type `vim variables.tfvars`, go into edit mode by pressing `i` and add

```
AWS_ACCESS_KEY = "[Your AWS access key]"
AWS_SECRET_KEY = "[Your AWS secret key]"
VPC_ID = "[Your VPC ID]"
DB_HOST = "[Your database host address]"
DB_PORT = "[Your database access port]"
DB_USERNAME = "[Your database username]"
DB_PASSWORD = "[Your database password]"
DB_NAME = "[Your database name]"
```

followed by `esc` then type `wq!` to save those changes and quit out of vim.
You will now need to run `terraform plan` and `terraform apply` to create the resources.
Please note, this will not create the ECR which will need to be done through the AWS UI. You will need [docker](https://www.docker.com/) or equivalent to containerise the program and put it on the ECR, we have included the required Dockerfiles for this.

WARNING: Much of the details of this code will need to changed for your specific circumstances, a full list will not be provided. If you are using terraform it is assumed you are aware of what this is doing.

#### dashboard.tf

- Builds a task definition running on FARGATE  that hosts the database.
- Builds a security group for the task that allows traffic in on ports 1433, 80, 443 and 8501 and traffic out on all ports.
- Builds an ECS to host the task.

#### database_creation.tf

- Builds a security group.
- Assigns rules to the security group that allows in and out traffic on port 5432.
- Builds an RDS assigned to the security group.

#### ETL_pipeline.tf

- Builds a IAM role.
- Builds an IAM policy that allows the lambda access.
- Attaches policy to the role.
- Builds three lambdas and assigns it the policy.
- Builds an IAM role for a step function.
- Builds an IAM policy that allows the lambda access.
- Attaches policy to the role.
- Builds a cloudwatch log group.
- Builds a policy for cloudwatch.
- Builds a state machine to trigger the lambdas with the pipeline in them.
- Builds an IAM role for the scheduler.
- Builds a scheduler that triggers every day to trigger the lambdas.

#### genre_new_releases.tf

- Currently empty

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

#### variables.tf

- Contains all the variables used in the terraform scripts

#### weekly_summary.tf

- Currently empty