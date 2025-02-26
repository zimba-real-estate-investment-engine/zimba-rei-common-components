import boto3
import logging
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from app.schemas.EmailSchema import EmailSchema

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Ensures logs are displayed in the console
    ]
)

class EmailService:
    @staticmethod
    def get_ses_client():
        load_dotenv()
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

        return ses_client

    @staticmethod
    def send_email(email: EmailSchema) -> dict:

        try:
            ses_client = EmailService.get_ses_client()

            message_body = {
                'Text': {
                    'Data': email.body_text,
                    'Charset': 'UTF-8'
                }
            }

            # Add HTML if it's not None
            if email.body_html is not None:
                message_body['Html'] = {
                    'Data': email.body_html,
                    'Charset': 'UTF-8'
                }

            response = ses_client.send_email(
                Source=email.sender,
                Destination={
                    'ToAddresses': email.to_addresses,
                },
                Message={
                    'Subject': {
                        'Data': email.subject,
                        'Charset': 'UTF-8'
                    },
                    'Body': message_body
                }
            )
            message_id = response['MessageId']
            if message_id:
                logging.info(f'Email successfully sent with message id {message_id}')

            return response

        except Exception as e:
            logging.error(f'Error: {e}')


