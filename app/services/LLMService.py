import os, json

import requests
from dotenv import load_dotenv

from app.domain.llm.WebsitePreprocessor import WebsitePreprocessor


class LLMService:
    @staticmethod
    def extract_listing_details(content, content_type) -> dict:
        load_dotenv()
        llm_model_name = os.getenv('LLM_MODEL_NAME')
        llm_host_and_port = os.getenv('LLM_HOST_AND_PORT')
        llm_chat_completion_path = os.getenv('LLM_CHAT_COMPLETION_PATH')
        llm_endpoint = llm_host_and_port + llm_chat_completion_path

        final_content = ''

        match content_type:
            case 'html':
                website_preprocessor = WebsitePreprocessor(html=content)
                final_content = website_preprocessor.get_raw_text()
            case 'text':
                final_content = content
            case _:
                raise Exception("Content type is needed, either text or html")

        response = requests.post(
            llm_endpoint,  # Replace with actual Llama API endpoint
            headers={
                'Authorization': 'Bearer YOUR_LLAMA_API_KEY',
                'Content-Type': 'application/json'
            },
            json={
                'model': llm_model_name,  # or specific model version
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are an expert at extracting structured data from HTML.'
                    },
                    {
                        'role': 'user',
                        'content': f"""Extract structured real estate listing details from this content:

        Text Content:
        {final_content}

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
        )

        full_response = ''

        try:
            # Extract JSON from API response
            full_response = response.json()['choices'][0]['message']['content']

            # Clean and parse JSON
            # Remove any markdown code block formatting if present
            if full_response.startswith('```json'):
                full_response = full_response.strip('```json').strip('```')

            # Parse the JSON
            details = json.loads(full_response)
            return details
        except Exception as e:
            return {
                "error": f"Could not parse details: {str(e)}",
                "raw_response": full_response
            }

    @staticmethod
    def is_inference_up():
        models_data = LLMService.models_response()
        if models_data is not None:
            return True
        else:
            return False

    @staticmethod
    def models_response():
        load_dotenv()
        llm_host_and_port = os.getenv('LLM_HOST_AND_PORT')
        llm_models_path = os.getenv('LLM_MODELS_PATH')
        llm_endpoint = llm_host_and_port + llm_models_path
        response = requests.get(llm_endpoint)

        if response.status_code == 200:
            return response
        else:
            raise Exception("Error getting migrations data")
