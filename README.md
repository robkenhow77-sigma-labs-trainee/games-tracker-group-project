# Game Tracker Project

A project designed for monitoring the latest game releases across Steam, GOG and Epic.

[comment]: <> (could add images for steam gog and epic here?)

## Description

This project includes an ETL pipeline for each storefront, each in their own folder. These pipelines are designed to be ran on AWS using lambdas which get triggered every 3 hours. The pipeline scrapes data from the store pages, cleans that data and inserts it into a database. That database is then read by a streamlit dashboard which is designed to be hosted online. Users will be able to then view information about the latest game releases as well as sign up to an email system that alerts them when a new game releases in a genre they have subscribed to.

The project *can* be run locally with some minor adjustments but is ultimately designed to be run on AWS. There are terraform files and Dockerfiles provided for this end.

## Getting Started

### Dependencies

* Python 3

Python libraries:
* beautifulsoup4
* logging
* logging
* pylint
* pytest
* pytest-cov
* requests
* requests
* rich
* selenium
* webdriver_manager

Optional:
* [terraform](https://www.terraform.io/)
* [docker](https://www.docker.com/)
* An AWS account and knowledge of using ECRs

### Installing

- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `find . -name 'requirements.txt' -exec pip install -r {} \;` from the root directory of this project to install all the required libraries or just run `pip install -r requirements.txt` in the folder you want to run.

- Type `vim .env` and then add the following by going into edit mode by pressing `i`:

```
DB_HOST=[Your database host address]
DB_NAME=[Your database name]
DB_PASSWORD=[Your database password]
DB_PORT=[Your database access port]
DB_USERNAME=[Your database username]
```

followed by `esc` then type `wq!` to save those changes and quit out of vim.

- OPTIONAL: If you wish to [terraform](https://www.terraform.io/) the required resources go into the `terraform` folder and type `vim variables.tfvars`, go into edit mode by pressing `i` and add

```
AWS_ACCESS_KEY = "[Your AWS access key]"
AWS_SECRET_KEY = "[Your AWS secret key]"
DB_HOST = "[Your database host address]"
DB_NAME = "[Your database name]"
DB_PASSWORD = "[Your database password]"
DB_PORT = "[Your database access port]"
DB_USERNAME = "[Your database username]"
VPC_ID = "[Your VPC ID]"
```

followed by `esc` then type `wq!` to save those changes and quit out of vim.
You will now need to run `terraform plan` and `terraform apply` to create the resources.
Please note, this will not create the ECR which will need to be done through the AWS UI. You will need [docker](https://www.docker.com/) or equivalent to containerise the program and put it on the ECR, we have included the required Dockerfiles for this.

## Files

#### README.md

- This file you are currently reading :)

### cloud/

#### main.py

- Currently empty

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

### dashboard/

#### dashboard.py

- Currently empty

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

### database/

- Type `vim .env` and then add the following by going into edit mode by pressing `i`:

```
DB_HOST=[Your database host address]
DB_NAME=[Your database name]
DB_PASSWORD=[Your database password]
DB_PORT=[Your database access port]
DB_USERNAME=[Your database username]
```

followed by `esc` then type `wq!` to save those changes and quit out of vim.

#### connect_to_db.sh

- Contains a bash script that will connect you to your database.
- Run with `bash connect_to_db.sh`

#### main.py

- Currently empty

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

#### reset_database.sh

- WARNING: ONLY RUN THIS IF YOU KNOW WHAT YOU ARE DOING.
- Contains a bash script that will connect you to your database and remove all data.
- Run with `bash reset_database.sh`

#### schema.sql

- Contains the postgres SQL required to set up the database as the script is expecting.
- Running reset_database.sh will seed the database with this architecture.

### pipeline/

#### extract_epic.py

- Scrapes the epic game store page for games released today.

#### extract_steam.py

- Scrapes the steam store page for games released today.
- Can specify a target date to scrape until that date is reached. The script will scroll through the page 100 times.
- If more than 100 scrolls is needed there is a comment pointing out the number to change to the desired scrolls.
- Formats the data of all the games extracted in the form of a list of dictionaries.

#### extract.py

- Currently empty

#### load.py

- Currently empty

#### main.py

- Currently empty

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

#### run_extract.sh

- Runs the steam_extract file with all logging sent a folder that will be created.
- Run with `bash run_extract.sh`

#### run_month.sh

- Runs the steam_extract file with all logging sent a folder that will be created. Will extract all games between today and the 11th of January 2025.
- Run with `bash run_month.sh`

#### test_extract.py

- Contains all tests related to the steam_extract file.
- Run `pytest` to see the test output.

#### test_transform.py

- Contains all tests related to the transform file.
- Run `pytest` to see the test output.

#### test.sh

- Runs `pytest` including outputting the test coverage.
- Run with `bash test.sh`

#### transform.py

- Takes the data from steam_extract.py and cleans it.
- Removes all erroneous data and formats all correct data into the form required by the database

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

## Authors

Contributors names and contact info

* [Candice Bennett](https://github.com/Candice-Bennett)
* [Robert Howarth](https://github.com/robkenhow77-sigma-labs-trainee)
* [Abdirahman Mohamud](https://github.com/OfficialARM17)
* [Benjamin Smith](https://github.com/CodeTechBen)

