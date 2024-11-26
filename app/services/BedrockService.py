import json
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


class BedrockService:
    @staticmethod
    def extract_listing_details(raw_text):
        load_dotenv()
        bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_LLM_REGION', 'us-west-2') # llama3.2 is in us-west-1 avoids cross-region inference
        )

        model_id = os.getenv('AWS_LLM_MODEL_ID')

        input_prompt = {
            'prompt': [
                {
                    'role': 'system',
                    'content': 'You are an expert at extracting structured data from HTML.'
                },
                {
                    'role': 'user',
                    'content': f"""Extract structured real estate listing details from this content:

            Text Content:
            {raw_text}

            Please return a JSON object with these fields:
            - address
            - price
            - bedrooms
            - bathrooms
            - square_footage
            - listing_type

            Important: Return ONLY a valid JSON object. Do not include any additional text or explanation."""
                }
            ],
            'temperature': 0.2,  # Low temperature for more consistent extraction
            # 'max_tokens': 300
        }
        # input_prompt = f"""You are an expert at extracting structured data from text.
        #
        # Extract structured real estate listing details from this content:
        #
        # Text Content:
        # {raw_text}
        #
        # Please return a JSON object with these fields:
        # - address
        # - price
        # - bedrooms
        # - bathrooms
        # - square_footage
        # - listing_type
        #
        # Important: Return ONLY a valid JSON object. Do not include any additional text or explanation.
        #
        # JSON:
        # """

        # Additional parameters
        temperature = 0.2  # Low temperature for more consistent extraction
        # max_tokens = 300  # Uncomment and adjust if needed

        try:
            # Invoke the model with the request.
            response = bedrock_client.invoke_model(
                modelId=model_id,
                contentType='applicaiton/json',
                accept='application/json',
                body=json.dumps(input_prompt))

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            exit(1)

        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract and print the response text.
        response_text = model_response["generation"]
        print(response_text)

        # try:
        #     # Extract JSON from API response
        #     full_response = response.json()['choices'][0]['message']['content']
        #
        #     # Clean and parse JSON
        #     # Remove any markdown code block formatting if present
        #     if full_response.startswith('```json'):
        #         full_response = full_response.strip('```json').strip('```')
        #
        #     # Parse the JSON
        #     details = json.loads(full_response)
        #     return details
        # except Exception as e:
        #     return {
        #         "error": f"Could not parse details: {str(e)}",
        #         "raw_response": full_response
        #     }


#
#
# # Use the native inference API to send a text message to Meta Llama 3.
#
# import boto3
# import json
#
# from botocore.exceptions import ClientError
#
# # Create a Bedrock Runtime client in the AWS Region of your choice.
# client = boto3.client("bedrock-runtime", region_name="us-west-2")
#
# # Set the model ID, e.g., Llama 3 70b Instruct.
# model_id = "meta.llama3-70b-instruct-v1:0"
#
# # Define the prompt for the model.
# prompt = "Describe the purpose of a 'hello world' program in one line."
#
# # Embed the prompt in Llama 3's instruction format.
# formatted_prompt = f"""
# <|begin_of_text|><|start_header_id|>user<|end_header_id|>
# {prompt}
# <|eot_id|>
# <|start_header_id|>assistant<|end_header_id|>
# """
#
# # Format the request payload using the model's native structure.
# native_request = {
#     "prompt": formatted_prompt,
#     "max_gen_len": 512,
#     "temperature": 0.5,
# }
#
# # Convert the native request to JSON.
# request = json.dumps(native_request)
#
# try:
#     # Invoke the model with the request.
#     response = client.invoke_model(modelId=model_id, body=request)
#
# except (ClientError, Exception) as e:
#     print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
#     exit(1)
#
# # Decode the response body.
# model_response = json.loads(response["body"].read())
#
# # Extract and print the response text.
# response_text = model_response["generation"]
# print(response_text)


