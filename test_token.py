import os
from dotenv import load_dotenv
from huggingface_hub import HfApi

load_dotenv()

# Test the token
api = HfApi()
token = os.environ.get("HF_TOKEN")

print(f"Token starts with: {token[:10]}..." if token else "No token found")

try:
    # Try to get user info - this should work with any valid token
    user_info = api.whoami(token=token)
    print("✅ Token is valid!")
    print(f"Logged in as: {user_info['name']}")
except Exception as e:
    print("❌ Token is invalid!")
    print(f"Error: {e}")
