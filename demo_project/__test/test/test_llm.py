import requests
import json

# Replace with your key
API_KEY = ""

# Your endpoint
ENDPOINT = "https://shubh-mam7gp5g-westus3.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview"

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

payload = {
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 200
}

response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))

print("Status:", response.status_code)
print("Response:")
print(response.json())


from pprint import  pprint


pprint(response.json())