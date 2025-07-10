"""
Test script to verify your Render API works with Langflow integration
This simulates how Langflow would call your API
"""

import requests
import base64
from PIL import Image
import io
import json
import time

class ImageGeneratorAPI:
    def __init__(self, api_url):
        self.api_url = api_url.rstrip('/')
        
    def generate_image(self, prompt, model="runwayml/stable-diffusion-v1-5", save_path="langflow_test_image.png"):
        """
        Generate image via API (same way Langflow would do it)
        """
        endpoint = f"{self.api_url}/generate-image"
        
        payload = {
            "prompt": prompt,
            "model": model
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        print(f"🚀 Calling API: {endpoint}")
        print(f"📝 Prompt: {prompt}")
        print(f"🤖 Model: {model}")
        print("⏳ Generating image... (this may take 30-60 seconds)")
        
        try:
            start_time = time.time()
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=120  # 2 minutes timeout
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"⏱️  Request took {duration:.2f} seconds")
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    print("✅ Image generated successfully!")
                    
                    # Decode base64 image (same as Langflow would do)
                    image_data = base64.b64decode(result["image_base64"])
                    image = Image.open(io.BytesIO(image_data))
                    
                    # Save image
                    image.save(save_path)
                    print(f"💾 Image saved as: {save_path}")
                    
                    # Return data that Langflow would receive
                    return {
                        "success": True,
                        "image_base64": result["image_base64"],
                        "message": result["message"],
                        "duration": duration,
                        "saved_path": save_path
                    }
                else:
                    print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                    return {"success": False, "error": result.get('message')}
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except requests.Timeout:
            print("⏰ Request timed out (>120 seconds)")
            return {"success": False, "error": "Timeout"}
            
        except Exception as e:
            print(f"💥 Request failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def test_health(self):
        """Test if API is healthy"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                print("✅ API Health Check Passed")
                print(f"   Status: {health_data.get('status')}")
                print(f"   HuggingFace: {health_data.get('huggingface')}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False

def main():
    # Replace with your actual Render URL
    API_URL = "https://your-app-name.onrender.com"  # UPDATE THIS!
    
    print("🧪 Testing Render API for Langflow Integration")
    print("=" * 50)
    
    # Initialize API client
    api = ImageGeneratorAPI(API_URL)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing API Health...")
    if not api.test_health():
        print("⚠️  API is not healthy. Check your deployment.")
        return
    
    # Test 2: Image Generation
    print("\n2️⃣ Testing Image Generation...")
    
    test_prompts = [
        "A cute cat wearing sunglasses",
        "Beautiful sunset over mountains",
        "Astronaut riding a horse in space"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🎨 Test {i}: {prompt}")
        result = api.generate_image(
            prompt=prompt,
            model="runwayml/stable-diffusion-v1-5",
            save_path=f"langflow_test_{i}.png"
        )
        
        if result["success"]:
            print(f"✅ Success! Image size: {len(result['image_base64'])} chars (base64)")
        else:
            print(f"❌ Failed: {result['error']}")
        
        print("-" * 30)
    
    print("\n🎉 Testing complete!")
    print("\n📋 For Langflow integration:")
    print(f"   • API URL: {API_URL}/generate-image")
    print("   • Method: POST")
    print("   • Headers: Content-Type: application/json")
    print("   • Body: {\"prompt\": \"your prompt\", \"model\": \"runwayml/stable-diffusion-v1-5\"}")
    print("   • Response: {\"success\": true, \"image_base64\": \"...\", \"message\": \"...\"}")

if __name__ == "__main__":
    main()
