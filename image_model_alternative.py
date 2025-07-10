import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try different approaches
def generate_image_alternative():
    """Alternative approach using public models"""
    try:
        # Option 1: Try without API key for public models
        client = InferenceClient()
        
        image = client.text_to_image(
            "Astronaut riding a horse",
            model="runwayml/stable-diffusion-v1-5",
        )
        
        image.save("generated_image.png")
        print("✅ Image generated successfully and saved as 'generated_image.png'")
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def generate_image_with_token():
    """Original approach with token"""
    try:
        client = InferenceClient(
            api_key=os.environ["HF_TOKEN"],
        )
        
        image = client.text_to_image(
            "Astronaut riding a horse",
            model="runwayml/stable-diffusion-v1-5",
        )
        
        image.save("generated_image.png")
        print("✅ Image generated successfully with token and saved as 'generated_image.png'")
        return True
        
    except Exception as e:
        print(f"❌ Token approach failed: {e}")
        return False

if __name__ == "__main__":
    print("Trying to generate image...")
    
    # Try with token first
    if not generate_image_with_token():
        print("\nTrying alternative approach without token...")
        generate_image_alternative()
