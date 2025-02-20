# Genre Emails

This folder contains code related to the daily genre summary emails that are sent to users who are subscribed to a genre.

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
```

You will notice that the naming convention has changed slightly where `AWS_ACCESS_KEY` is now `PRIVATE_AWS_ACCESS_KEY` this is because the former is a protected variable name in AWS.

## Files

`send_emails.py` contains all the code related to getting the data, generating the emails and then sending them. Run this file to send a daily genre email to each subscriber.

This file meant to be [dockerised](https://www.docker.com/) and sent to an AWS ECR. The Dockerfile and related `genre_emails_ECR.sh` relate to this process.