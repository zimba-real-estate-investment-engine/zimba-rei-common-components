# import requests
# import json
#
# def extract_listing_details(raw_html):
#     # OpenAI API call (replace with your actual API endpoint)
#     response = requests.post(
#         'https://api.openai.com/v1/chat/completions',
#         headers={
#             'Authorization': 'Bearer YOUR_API_KEY',
#             'Content-Type': 'application/json'
#         },
#         json={
#             'model': 'gpt-3.5-turbo',
#             'messages': [
#                 {
#                     'role': 'system',
#                     'content': 'You are an expert at extracting structured data from HTML.'
#                 },
#                 {
#                     'role': 'user',
#                     'content': f"""Extract structured real estate listing details from this HTML:
#
# HTML Content:
# {raw_html}
#
# Please return JSON with these fields:
# - address
# - price
# - bedrooms
# - bathrooms
# - square_footage
# - listing_type
#
# Structured JSON Response:"""
#                 }
#             ],
#             'response_format': {'type': 'json_object'}
#         }
#     )
#
#     # Parse the response
#     try:
#         # Extract JSON from API response
#         details = response.json()['choices'][0]['message']['content']
#         return json.loads(details)
#     except Exception as e:
#         return {"error": f"Could not parse details: {str(e)}"}
#
# # Alternative with Anthropic Claude API
# def extract_listing_details_claude(raw_html):
#     response = requests.post(
#         'https://api.anthropic.com/v1/messages',
#         headers={
#             'x-api-key': 'YOUR_ANTHROPIC_API_KEY',
#             'Content-Type': 'application/json',
#             'anthropic-version': '2023-06-01'
#         },
#         json={
#             'model': 'claude-3-opus-20240229',
#             'max_tokens': 300,
#             'messages': [
#                 {
#                     'role': 'user',
#                     'content': f"""Extract structured real estate listing details from this HTML:
#
# HTML Content:
# {raw_html}
#
# Please return JSON with these fields:
# - address
# - price
# - bedrooms
# - bathrooms
# - square_footage
# - listing_type
#
# Structured JSON Response:"""
#                 }
#             ],
#             'response_format': {'type': 'json'}
#         }
#     )
#
#     # Parse the response
#     try:
#         details = response.json()['content'][0]['text']
#         return json.loads(details)
#     except Exception as e:
#         return {"error": f"Could not parse details: {str(e)}"}