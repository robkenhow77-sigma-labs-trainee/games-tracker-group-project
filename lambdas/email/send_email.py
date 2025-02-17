import boto3
import json
from os import environ as ENV
from dotenv import load_dotenv

load_dotenv()


def get_ses_connection():
    """Get SES client connection"""
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=ENV['AWS_ACCESS_KEY'],
        aws_secret_access_key=ENV['AWS_SECRET_ACCESS_KEY'],
        region_name=ENV['AWS_REGION']
    )
    return ses_client


def lambda_handler(event, context):
    try:
        ses = get_ses_connection()
        email_data = event  # generated email data

        # iterate each genre in email data
        for genre, details in email_data.items():
            subscribers = details['subscribers']
            html_body = details['html_body']

            # iterate each subscriber of the genre
            for subscriber in subscribers:
                email_params = {
                    'Destination': {
                        'ToAddresses': [subscriber]
                    },
                    'Message': {
                        'Body': {
                            'Html': {
                                'Data': html_body
                            }
                        },
                        'Subject': {
                            'Data': f'🎮 New Game Releases in {genre}'
                        }
                    },
                    'Source': 'trainee.jamie.groom@sigmalabs.co.uk',
                }

                # Send email using ses
                response = ses.send_email(**email_params)

                print(
                    f"Email sent to {subscriber} with response: {response['ResponseMetadata']}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Emails sent successfully.'})
        }
    except Exception as e:
        print(f'Error sending email: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to send emails.', 'error': str(e)})
        }
