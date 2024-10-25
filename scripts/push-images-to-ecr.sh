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
  "zimba-rei-common-components_nginx"
  "zimba-rei-common-components_subscriptions-api"
  "zimba-rei-common-components_underwritings-api"
)

TAG="latest"  # Change the tag as needed, or set dynamically

# Get login command from ECR and execute it directly
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Loop through the images and push them to ECR
for IMAGE_NAME in "${IMAGES[@]}"; do

  # tag the images for pushing
  echo "Tagging Docker image for ${IMAGE_NAME}..."
  docker tag $IMAGE_NAME:$TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/${REPO_NAME}:$IMAGE_NAME

  ECR_REPOSITORY="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO_NAME}:${IMAGE_NAME}"

#  echo "Building Docker image for ${IMAGE_NAME}..."
  # Build the Docker image
#  docker build -t ${ECR_REPOSITORY}:${TAG} ./${IMAGE_NAME}


  echo "Pushing ${IMAGE_NAME} to Amazon ECR..."

  # Push the Docker image to ECR
  docker push ${ECR_REPOSITORY}

  echo "${IMAGE_NAME} has been pushed to ${ECR_REPOSITORY}"
done

echo "All images have been pushed successfully."
