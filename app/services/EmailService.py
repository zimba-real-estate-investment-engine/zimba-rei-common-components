# from fastapi import FastAPI, Request
# import boto3
# from botocore.exceptions import ClientError
#
# app = FastAPI()
#
# # Initialize the SES client
# ses_client = boto3.client('ses', region_name='us-east-1')
#
# @app.post("/send-email/")
# async def send_email(request: Request):
#     data = await request.json()
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     email = data.get('email')
#     subject = data.get('subject')
#     message = data.get('message')
#
#     sender_name = f"{first_name} {last_name}"
#     sender_email = "no-reply@example.com"  # Use your verified SES email or domain
#     formatted_sender = f"{sender_name} <{sender_email}>"
#
#     try:
#         # Send email using AWS SES
#         response = ses_client.send_email(
#             Source=formatted_sender,  # This includes the display name and email
#             Destination={
#                 'ToAddresses': [email]
#             },
#             Message={
#                 'Subject': {
#                     'Data': subject
#                 },
#                 'Body': {
#                     'Text': {
#                         'Data': message
#                     }
#                 }
#             }
#         )
#         return {"message": "Email sent successfully!", "response": response}
#     except ClientError as e:
#         return {"error": str(e)}
#
#
#
#
# response = ses_client.send_email(
#     Source=formatted_sender,
#     Destination={
#         'ToAddresses': [email]
#     },
#     Message={
#         'Subject': {
#             'Data': subject
#         },
#         'Body': {
#             'Text': {
#                 'Data': message
#             }
#         }
#     },
#     ReplyToAddresses=['reply-to@example.com']
# )
