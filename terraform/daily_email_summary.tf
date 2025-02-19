# ECR definition for the code that gets daily email summaries
data "aws_ecr_repository" "c15-play-stream-daily-email-summary" {
    name = "c15-play-stream-daily-email-summary" 
}

data "aws_ecr_image" "daily-summary-latest-image" {
    repository_name = "c15-play-stream-daily-email-summary"
    most_recent     = true
}

# Setting IAM information
resource "aws_iam_policy" "send_email_policy" {
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

resource "aws_iam_role_policy_attachment" "lambda-daily-summary-policy-attachment" {
  role       = aws_iam_role.lambda_task_role.name
  policy_arn = aws_iam_policy.send_email_policy.arn
}

# Lambda Function to make the daily Email Summary work
resource "aws_lambda_function" "c15-play-stream-daily-summary-lambda-function" {
    function_name = "c15-play-stream-daily-email-summary-lambda-function"
    package_type = "Image"
    image_uri = data.aws_ecr_image.daily-summary-latest-image.image_uri
    memory_size   = 512
    timeout       = 512
    
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

# Making the EventBridge Scheduler to run this daily
resource "aws_scheduler_schedule" "daily-email-summary-scheduler" {
    name = "c15-play-stream-daily-email-summary-scheduler"
    schedule_expression   = "rate(1 day)"  # Runs every week
    flexible_time_window {
        mode = "OFF"
    }
    target {
        arn      = aws_lambda_function.c15-play-stream-daily-summary-lambda-function.arn
        role_arn = aws_iam_role.report_scheduler_role.arn
    }
}