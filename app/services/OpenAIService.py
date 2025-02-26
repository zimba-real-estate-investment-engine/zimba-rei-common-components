
import json
import logging
import os
import pickle
from datetime import datetime
from typing import List

from openai import OpenAI
import openai

from dotenv import load_dotenv


class OpenAIService:

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)  # Set the logging level

    @staticmethod
    def extract_listing_details(raw_text: str, entities_to_extract: List[str] | None = None):

        api_key = os.getenv('LLM_OPENAI_KEY')
        client = OpenAI(api_key=api_key)

        if entities_to_extract is None:
            entities_to_extract = os.getenv('ENTITIES_TO_EXTRACT').strip().split(',')

        system_prompt = f"""
        You are a named entity recognition tool. Extract the following entities from the text:
        {', '.join(entities_to_extract)}.
        Here is the text: {raw_text}
        Please return the results in JSON format.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],
            temperature=0.0,
        )

        # Pickle chatcompletion
        # pkl_filename = str(datetime.now()) + '_openai_chatcompletion.pkl'
        # with open(pkl_filename, 'wb') as file:
        #     pickle.dump(response, file)

        try:
            # Extract JSON from API response
            # full_response = response.json()['choices'][0]['message']['content']
            full_response = response.choices[0].message.content

            # Clean and parse JSON
            # Remove any markdown code block formatting if present
            if full_response.startswith('```json'):
                full_response = full_response.strip('```json').strip('```')

            # Parse the JSON
            details = json.loads(full_response)

            # Save data for later debugging
            # json_filename = str(datetime.now()) + '_openai_response.json'
            # with open(json_filename, 'w') as file:
            #     json.dump(details, file, indent=4)

            OpenAIService.logger.info(f"OpenAI completion details: {details}")

            return details
        except Exception as e:
            logging.error("OpenAI call error", exc_info=True)
            return {
                "error": f"OpenAI call, could not parse details: {str(e)}",
                "raw_response": response
            }
