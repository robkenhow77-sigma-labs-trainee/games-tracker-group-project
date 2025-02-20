# ECR definition for the code that gets daily email summaries
data "aws_ecr_repository" "c15-play-stream-daily-email" {
    name = "c15-play-stream-daily-email" 
}

data "aws_ecr_image" "daily-genre-latest-image" {
    repository_name = "c15-play-stream-daily-email"
    image_tag     = latest
}

# Setting up IAM information

resource "aws_iam_role_policy_attachment" "lambda-daily-genre-policy-attachment" {
  role       = aws_iam_role.lambda_task_role.name
  policy_arn = aws_iam_policy.send_email_policy.arn
}

# Lambda Function to make the Daily Email Summary work

resource "aws_lambda_function" "c15-play-stream-daily-genre-email-lambda-function" {
    function_name = "c15-play-stream-daily-genre-email-lambda-function"
    package_type = "Image"
    image_uri = data.aws_ecr_image.daily-genre-latest-image.image_uri
    memory_size   = 512
    timeout       = 512

    environment {
        variables = {
        DB_HOST                         = var.DB_HOST
        DB_NAME                         = var.DB_NAME
        DB_PASSWORD                     = var.DB_PASSWORD
        DB_PORT                         = var.DB_PORT
        DB_USERNAME                     = var.DB_USERNAME
        PRIVATE_AWS_ACCESS_KEY          = var.AWS_ACCESS_KEY
        PRIVATE_AWS_SECRET_ACCESS_KEY   = var.AWS_SECRET_ACCESS_KEY
        PRIVATE_AWS_REGION              = var.AWS_REGION
        SNS_TOPIC_ARN                   = var.SNS_TOPIC_ARN
        }
    }

    role = aws_iam_role.lambda_task_role.arn
}

# Making the Step Function to call the Daily Email Summary Lambda Function

resource "aws_sfn_state_machine" "daily-genre-email-step-function" {
    name     = "c15-play-stream-daily-genre-email-step-function"
    role_arn = aws_iam_role.etl-pipeline-step-function-role.arn
    publish  = true
    type     = "EXPRESS"

    definition = jsonencode({
        "Comment": "Step Function to run the Daily Genre Email Summary Lambda Function",
        "StartAt": "Run Daily Genre Email Lambda",
        "States": {
            "Run Daily Genre Email Lambda": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "Parameters": {
                    "FunctionName": aws_lambda_function.c15-play-stream-daily-genre-email-lambda-function.arn,
                    "Payload": {}
                },
                "End": true,
            }
        }
    })

    logging_configuration {
        log_destination       = "${aws_cloudwatch_log_group.play-stream_state_machine_logs.arn}:*"
        include_execution_data = true
        level                 = "ALL"
    }
}

# Making the EventBridge Scheduler to run this daily

resource "aws_scheduler_schedule" "daily-genre-email-scheduler" {
    name = "c15-play-stream-daily-genre-email-scheduler"
    schedule_expression   = "cron(15 17 ? * * *)"  # Runs every day at 17:15
    flexible_time_window {
        mode = "OFF"
    }
    target {
        arn      = aws_lambda_function.c15-play-stream-weekly-summary-lambda-function.arn
        role_arn = aws_iam_role.report_scheduler_role.arn
    }
}