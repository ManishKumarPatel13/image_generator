import requests
import base64
import json
from PIL import Image
import io

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"API Health: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"API is not running: {e}")
        return False

def generate_image_base64(prompt, model="runwayml/stable-diffusion-v1-5"):
    """Generate image and get base64 response"""
    try:
        payload = {
            "prompt": prompt,
            "model": model
        }
        
        response = requests.post(
            f"{BASE_URL}/generate-image",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                # Decode base64 and save image
                image_data = base64.b64decode(result["image_base64"])
                image = Image.open(io.BytesIO(image_data))
                
                # Save the image
                filename = f"generated_{prompt.replace(' ', '_')[:20]}.png"
                image.save(filename)
                print(f"✅ Image saved as: {filename}")
                return True
            else:
                print(f"❌ API Error: {result['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    return False

def generate_image_file(prompt, model="runwayml/stable-diffusion-v1-5"):
    """Generate image and download as file"""
    try:
        payload = {
            "prompt": prompt,
            "model": model
        }
        
        response = requests.post(
            f"{BASE_URL}/generate-image-file",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # Save the image file
            filename = f"downloaded_{prompt.replace(' ', '_')[:20]}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Image downloaded as: {filename}")
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    return False

def get_available_models():
    """Get list of available models"""
    try:
        response = requests.get(f"{BASE_URL}/models")
        if response.status_code == 200:
            models = response.json()
            print("Available models:")
            for model in models["available_models"]:
                print(f"  - {model}")
            return models["available_models"]
        else:
            print(f"❌ Error getting models: {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    return []

if __name__ == "__main__":
    print("🚀 Testing AI Image Generator API\n")
    
    # Test API health
    if not test_api_health():
        print("❌ API is not running. Please start it with: uvicorn api:app --reload")
        exit(1)
    
    print("\n📋 Available Models:")
    get_available_models()
    
    print("\n🎨 Generating test images...")
    
    # Test image generation
    test_prompts = [
        "A cute cat wearing a space helmet",
        "Sunset over mountains with purple sky"
    ]
    
    for prompt in test_prompts:
        print(f"\n🖼️  Generating: '{prompt}'")
        generate_image_base64(prompt)
    
    print("\n✅ Test completed!")
