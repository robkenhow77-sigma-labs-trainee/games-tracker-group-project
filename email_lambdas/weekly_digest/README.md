# Weekly Digest

This folder contains code related to the weekly summary emails that are sent to users (and also saved in pdf form to an S3 bucket).

## How to use

This folder will require a `.env`. See the [main README](../../README.md) to see how to make a `.env` and add the following information:

```
PRIVATE_AWS_ACCESS_KEY="[Your AWS access key]"
PRIVATE_AWS_SECRET_ACCESS_KEY="[Your AWS secret key]"
PRIVATE_AWS_REGION="[Your AWS region]"

DB_HOST="[Your database host url]"
DB_PORT=[Your database access port]
DB_PASSWORD="[Your database password]"
DB_USERNAME="[Your database username]"
DB_NAME="[Your database name]"

SNS_TOPIC_ARN=[Your SNS topic ARN]
PRIVATE_BUCKET_NAME=[Your S3 bucket name]
```

You will notice that the naming convention has changed slightly where `AWS_ACCESS_KEY` is now `PRIVATE_AWS_ACCESS_KEY` this is because the former is a protected variable name in AWS.

## Files

`weekly_digest.py` contains all the code related to getting the data, generating the emails and then sending them. Run this file to send a weekly email to each subscriber.

This file meant to be [dockerised](https://www.docker.com/) and sent to an AWS ECR. The Dockerfile and related `weekly_digest_ECR.sh` relate to this process.