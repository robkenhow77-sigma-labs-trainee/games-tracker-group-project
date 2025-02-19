# ECR definition for the code that gets weekly email summaries

data "aws_ecr_repository" "c15-play-stream-weekly-email-summary" {
    name = "c15-play-stream-weekly-email-summary" 
}

data "aws_ecr_image" "weekly-summary-latest-image" {
    repository_name = "c15-play-stream-weekly-email-summary"
    most_recent     = true
}

# Setting IAM information

resource "aws_iam_policy" "send_weekly_email_policy" {
  name        = "SES_SendEmailPolicy"
  description = "Policy for sending emails using SES"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Effect   = "Allow"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda-weekly-summary-policy-attachment" {
  role       = aws_iam_role.lambda_task_role.name
  policy_arn = aws_iam_policy.send_weekly_email_policy.arn
}

# Lambda Function to make the Weekly Email Summary work

resource "aws_lambda_function" "c15-play-stream-weekly-summary-lambda-function" {
    function_name = "c15-play-stream-weekly-email-summary-lambda-function"
    package_type = "Image"
    image_uri = data.aws_ecr_image.weekly-summary-latest-image.image_uri
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

# Making the Step Function to call the Weekly Email Summary Lambda Function

resource "aws_sfn_state_machine" "weekly-email-summary-step-function" {
    name     = "c15-play-stream-weekly-email-summary-step-function"
    role_arn = aws_iam_role.etl-pipeline-step-function-role.arn
    publish  = true
    type     = "EXPRESS"

    definition = jsonencode({
        "Comment": "Step Function to run the Weekly Email Summary Lambda Function",
        "StartAt": "Run Weekly Email Summary Lambda",
        "States": {
            "Run Weekly Email Summary Lambda": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "Parameters": {
                    "FunctionName": aws_lambda_function.c15-play-stream-weekly-summary-lambda-function.arn,
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


# Making the EventBridge Scheduler to run this weekly

resource "aws_scheduler_schedule" "weekly-email-summary-scheduler" {
    name = "c15-play-stream-weekly-email-summary-scheduler"
    schedule_expression   = "cron(15 17 ? * MON *)"  # Runs every Monday at 17:15
    flexible_time_window {
        mode = "OFF"
    }
    target {
        arn      = aws_lambda_function.c15-play-stream-weekly-summary-lambda-function.arn
        role_arn = aws_iam_role.report_scheduler_role.arn
    }
}