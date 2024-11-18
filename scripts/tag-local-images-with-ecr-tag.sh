# Tag the local images that will be pushed
IMAGES=(
#  "zimba-rei-common-components_deals-api"
#  "zimba-rei-common-components_investor-profiles-api"
#  "zimba-rei-common-components_listings-api"
#  "zimba-rei-common-components_mortgages-api"
#  "zimba-rei-common-components_nginx"
#  "zimba-rei-common-components_subscriptions-api"
  "zimba-rei-common-components_underwriting"
)
for IMAGE_NAME in "${IMAGES[@]}"; do
  docker tag $IMAGE_NAME 975050215890.dkr.ecr.us-east-2.amazonaws.com/rei-engine-ecr-repo:$IMAGE_NAME
done