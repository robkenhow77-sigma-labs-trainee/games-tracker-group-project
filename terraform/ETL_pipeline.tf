# ECR definition for all three ETL pipelines

data "aws_ecr_repository" "c15-play-stream-steam-etl-pipeline-ecr" {
    name        = "c15-play-stream-steam-etl-pipeline-ecr"
}

data "aws_ecr_image" "steam-latest-image" {
  repository_name         = data.aws_ecr_repository.c15-play-stream-steam-etl-pipeline-ecr.name
  most_recent             = true
}

# ECR definition for the Epic ETL pipeline

data "aws_ecr_repository" "c15-play-stream-epic-etl-pipeline-ecr" {
    name                  = "c15-play-stream-epic-etl-pipeline-ecr"
}

data "aws_ecr_image" "epic-latest-image" {
  repository_name         = data.aws_ecr_repository.c15-play-stream-epic-etl-pipeline-ecr.name
  most_recent             = true
}

# ECR definition for the GOG ETL pipeline

data "aws_ecr_repository" "c15-play-stream-gog-etl-pipeline-ecr" {
    name                  = "c15-play-stream-gog-etl-pipeline-ecr"
}

data "aws_ecr_image" "gog-latest-image" {
  repository_name         = data.aws_ecr_repository.c15-play-stream-gog-etl-pipeline-ecr.name
  most_recent             = true
}

# IAM role for the Lambda Function

resource "aws_iam_role" "lambda_task_role" {
  name                    = "c15-play-stream-task-role"

  assume_role_policy = jsonencode({
    Version               = "2012-10-17",
    Statement = [
      {
        Action            = "sts:AssumeRole",
        Principal         = { Service = "lambda.amazonaws.com" },
        Effect            = "Allow"
      }
    ]
  })
}

# IAM Policy to allow the Lambda to run the ECR and execute the image inside

resource "aws_iam_policy" "etl-pipeline-lambda-iam-policy" {
    name                  = "c15-play-stream-etl-pipeline-lambda-iam-policy"
    policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "lambda:InvokeFunction",
        Resource = [
            aws_lambda_function.c15-play-stream-steam-etl-pipeline-lambda-function.arn,
            aws_lambda_function.c15-play-stream-epic-etl-pipeline-lambda-function.arn,
            aws_lambda_function.c15-play-stream-gog-etl-pipeline-lambda-function.arn
        ]
      }
    ]
  })
}

# Policy attached to the Lambda Role
resource "aws_iam_role_policy_attachment" "state_machine_iam_role_lambda" {
  role                    = aws_iam_role.lambda_task_role
  policy_arn              = aws_iam_policy.etl-pipeline-lambda-iam-policy.arn
}

# Lambda Function for the Steam ETL pipeline

resource "aws_lambda_function" "c15-play-stream-steam-etl-pipeline-lambda-function" {
    function_name         = "c15-play-stream-etl-pipeline-lambda-function"
    package_type          = "Image"
    image_uri             = data.aws_ecr_image.steam-latest-image.image_uri
    memory_size           = 128
    timeout               = 35

    environment {
        variables = {
        DB_HOST      = var.DB_HOST
        DB_NAME      = var.DB_NAME
        DB_PASSWORD  = var.DB_PASSWORD
        DB_PORT      = var.DB_PORT
        DB_USER      = var.DB_USERNAME
        }
    }
    role                  = aws_iam_role.lambda_task_role.arn
}

# Lambda Function for the Epic ETL pipeline

resource "aws_lambda_function" "c15-play-stream-epic-etl-pipeline-lambda-function" {
    function_name         = "c15-play-stream-epic-etl-pipeline-lambda-function"
    package_type          = "Image"
    image_uri             = data.aws_ecr_image.epic-latest-image.image_uri
    memory_size           = 128
    timeout               = 35

    environment {
        variables = {
        DB_HOST      = var.DB_HOST
        DB_NAME      = var.DB_NAME
        DB_PASSWORD  = var.DB_PASSWORD
        DB_PORT      = var.DB_PORT
        DB_USER      = var.DB_USERNAME
        }
    }
    role                  = aws_iam_role.lambda_task_role.arn
}

# Lambda Function for the GOG ETL pipeline

resource "aws_lambda_function" "c15-play-stream-gog-etl-pipeline-lambda-function" {
    function_name = "c15-play-stream-gog-etl-pipeline-lambda-function"
    package_type = "Image"
    image_uri = data.aws_ecr_image.gog-latest-image.image_uri
    memory_size = 128
    timeout = 35

    environment {
        variables = {
        DB_HOST      = var.DB_HOST
        DB_NAME      = var.DB_NAME
        DB_PASSWORD  = var.DB_PASSWORD
        DB_PORT      = var.DB_PORT
        DB_USER      = var.DB_USERNAME
        }
    }
    role = aws_iam_role.lambda_task_role.arn
}

# IAM Role for Step Function that invokes the Lambda

resource "aws_iam_role" "etl-pipeline-step-function-role" {
    name = "c15-play-stream-etl-pipeline-step-function-role"
    assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Principal = { Service = "states.amazonaws.com" },
        Effect    = "Allow"
      }
    ]
  })
}

resource "aws_iam_policy" "etl-pipeline-state_machine_lambda_policy" {
  name   = "c15-play-stream-etl-pipeline-state-machine-lambda-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "lambda:InvokeFunction",
        Resource = [
            aws_lambda_function.c15-play-stream-steam-etl-pipeline-lambda-function.arn,
            aws_lambda_function.c15-play-stream-epic-etl-pipeline-lambda-function.arn,
            aws_lambda_function.c15-play-stream-gog-etl-pipeline-lambda-function.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "state_role_lambda" {
  role       = aws_iam_role.etl-pipeline-step-function-role
  policy_arn = aws_iam_policy.etl-pipeline-state_machine_lambda_policy.arn
}

# CloudWatch Log Group for The Step Function

resource "aws_cloudwatch_log_group" "play-stream_state_machine_logs" {
  name = "/aws/vendedlogs/states/play-stream-state-machine-logs"
}

resource "aws_iam_role_policy_attachment" "state_machine_cw_logs" {
  role       = aws_iam_role.etl-pipeline-step-function-role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

# Step Function to call the lambda

resource "aws_sfn_state_machine" "etl-pipeline-state-machine" {
  name     = "c15-play-stream-etl-pipeline-state-machine"
  role_arn = aws_iam_role.lambda_task_role.arn
  publish  = true
  type     = "EXPRESS"

  definition = jsonencode({
    "Comment": "Step Function to trigger the three ETL pipeline Lambda functions sequentially",
    "StartAt": "Invoke Steam ETL Pipeline Lambda Function",
    "States": {
      "Invoke Steam ETL Pipeline Lambda Function": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "Parameters": {
          "FunctionName": aws_lambda_function.c15-play-stream-steam-etl-pipeline-lambda-function.arn,
          "Payload.$": "$"
        },
        "Next": "Invoke Epic ETL Pipeline Lambda Function"
      },
      "Invoke Epic ETL Pipeline Lambda Function": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "Parameters": {
          "FunctionName": aws_lambda_function.c15-play-stream-epic-etl-pipeline-lambda-function.arn,
          "Payload.$": "$"
        },
        "Next": "Invoke GOG ETL Pipeline Lambda Function"
      },
      "Invoke GOG ETL Pipeline Lambda Function": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "Parameters": {
          "FunctionName": aws_lambda_function.c15-play-stream-gog-etl-pipeline-lambda-function.arn,
          "Payload.$": "$"
        },
        "End": true
      }
    }
  })
}
# IAM Role for Scheduler
resource "aws_iam_role" "report_scheduler_role" {
  name = "c15-play-steam-state-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = { Service = "scheduler.amazonaws.com" },
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# EventBridge Scheduler to run Step Function every day

resource "aws_scheduler_schedule" "steam_etl_pipeline_schedule" {
    name = "c15-play-stream-etl-pipeline-daily-trigger"
    schedule_expression   = "rate(1 day)"  # Runs every day
    flexible_time_window {
        mode = "OFF"
    }
    target {
        arn      = aws_sfn_state_machine.etl-pipeline-state-machine.arn
        role_arn = aws_iam_role.report_scheduler_role.arn
    }
}