# Will be run manually and later included in terraform and CI/CD
#!/bin/bash

# AWS parameters
AWS_REGION="us-east-2"  # Change to your region
ACCOUNT_ID="975050215890"  # Replace with your AWS account ID
REPO_NAME="rei-engine-ecr-repo"

# List of images to build and push
IMAGES=(
  "zimba-rei-common-components_deals-api"
  "zimba-rei-common-components_investor-profiles-api"
  "zimba-rei-common-components_listings-api"
  "zimba-rei-common-components_mortgages-api"
#  "zimba-rei-common-components_nginx"
  "zimba-rei-common-components_subscriptions-api"
  "zimba-rei-common-components_underwritings-api"
)

TAG="latest"  # Change the tag as needed, or set dynamically

# Get login command from ECR and execute it directly
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

PORT_NUMBER=8081
# Loop through the images and push them to ECR
for IMAGE_NAME in "${IMAGES[@]}"; do

  IMAGE_TAG="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO_NAME}:${IMAGE_NAME}"

  echo "Running container based on ${IMAGE_NAME} on port ${PORT_NUMBER}"

  # Run container the Docker image from ECR
  docker run --restart always --name $IMAGE_NAME -d -p $PORT_NUMBER:8000 $IMAGE_TAG

  echo "${IMAGE_NAME} is running on port $PORT_NUMBER"

  ((PORT_NUMBER++))
done

echo "All containers have been started successfully."