# Make sure you are logged into aws  "aws sso login --profile <your_profile>"
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 975050215890.dkr.ecr.us-east-2.amazonaws.com
