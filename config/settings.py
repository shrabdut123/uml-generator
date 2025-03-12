import os

AZURE_OPENAI_ENDPOINT = "https://<your-custom-api-endpoint>-openai.openai.azure.com/"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = "<model-of-your-choice>"

if not AZURE_OPENAI_API_KEY:
    raise ValueError("Azure OpenAI API key is not set.")
