# Langflow Integration Guide

## Using Your Render Image Generator API in Langflow

This guide shows how to integrate your deployed Render API with Langflow to create image generation workflows.

## 🔧 Setup Requirements

### 1. Deployed API
- Your API deployed on Render: `https://your-app-name.onrender.com`
- API endpoints available:
  - `POST /generate-image` - Returns base64 image
  - `POST /generate-image-file` - Returns image file

### 2. Langflow Environment
- Langflow installed and running
- Access to Custom Component or API Request nodes

## 🚀 Integration Methods

### Method 1: Using API Request Component (Recommended)

#### Step 1: Add API Request Node
1. In Langflow, drag an **"API Request"** component to your flow
2. Configure the following:

**Configuration:**
```json
{
  "method": "POST",
  "url": "https://your-app-name.onrender.com/generate-image",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "prompt": "{prompt_input}",
    "model": "runwayml/stable-diffusion-v1-5"
  }
}
```

#### Step 2: Connect Input/Output
- **Input**: Connect a **Text Input** node for prompts
- **Output**: Connect to **Text Output** or **File Output** node

#### Step 3: Handle Response
The API returns JSON with base64 image:
```json
{
  "success": true,
  "message": "Image generated successfully",
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

### Method 2: Custom Python Component

#### Step 1: Create Custom Component
```python
from langflow import CustomComponent
from typing import Optional
import requests
import base64
from PIL import Image
import io

class ImageGeneratorComponent(CustomComponent):
    display_name = "AI Image Generator"
    description = "Generate images using Render deployed API"
    
    def build_config(self):
        return {
            "api_url": {
                "display_name": "API URL",
                "type": "str",
                "value": "https://your-app-name.onrender.com/generate-image"
            },
            "prompt": {
                "display_name": "Prompt",
                "type": "str",
                "multiline": True
            },
            "model": {
                "display_name": "Model",
                "type": "str",
                "options": [
                    "runwayml/stable-diffusion-v1-5",
                    "stabilityai/stable-diffusion-2-1",
                    "stabilityai/stable-diffusion-3.5-large"
                ],
                "value": "runwayml/stable-diffusion-v1-5"
            }
        }
    
    def build(self, api_url: str, prompt: str, model: str) -> str:
        """Generate image and return base64 string"""
        try:
            response = requests.post(
                api_url,
                json={
                    "prompt": prompt,
                    "model": model
                },
                timeout=120  # 2 minutes timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result["image_base64"]
                else:
                    return f"Error: {result.get('message', 'Unknown error')}"
            else:
                return f"API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Request failed: {str(e)}"
```

### Method 3: HTTP Request Node Configuration

#### Basic Configuration:
- **Method**: POST
- **URL**: `https://your-app-name.onrender.com/generate-image`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Body Template**:
  ```json
  {
    "prompt": "{{prompt}}",
    "model": "runwayml/stable-diffusion-v1-5"
  }
  ```

## 📋 Complete Langflow Workflow Examples

### Example 1: Simple Image Generation
```yaml
Workflow:
1. Text Input (prompt) → 
2. API Request (your render endpoint) → 
3. JSON Parser (extract image_base64) → 
4. Base64 to Image Converter → 
5. Image Display
```

### Example 2: Chat-to-Image Generation
```yaml
Workflow:
1. Chat Input → 
2. LLM (improve/enhance prompt) → 
3. API Request (image generation) → 
4. Image Display + Text Response
```

### Example 3: Multi-Model Comparison
```yaml
Workflow:
1. Text Input (prompt) → 
2. Split to multiple API Request nodes (different models) → 
3. Combine results → 
4. Image Gallery Display
```

## 🛠️ Langflow Component Configuration

### API Request Node Settings:
```json
{
  "name": "Image Generator API",
  "method": "POST",
  "url": "https://your-app-name.onrender.com/generate-image",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "prompt": "{input.prompt}",
    "model": "runwayml/stable-diffusion-v1-5"
  },
  "timeout": 120,
  "parse_response": true
}
```

### Response Processing:
```python
# In a Python Code node after API request
import base64
from PIL import Image
import io

def process_image_response(api_response):
    """Convert base64 response to image"""
    if api_response.get("success"):
        image_data = base64.b64decode(api_response["image_base64"])
        image = Image.open(io.BytesIO(image_data))
        return image
    else:
        raise Exception(f"API Error: {api_response.get('message', 'Unknown error')}")
```

## 🎯 Best Practices for Langflow Integration

### 1. Error Handling
```python
# Add error handling in your flow
try:
    response = api_call()
    if response.status_code != 200:
        return {"error": f"API returned {response.status_code}"}
except requests.Timeout:
    return {"error": "Request timed out - image generation can take 30-60 seconds"}
except Exception as e:
    return {"error": f"Request failed: {str(e)}"}
```

### 2. Timeout Management
- Set timeout to 120 seconds (image generation is slow)
- Add loading indicators
- Consider async processing for better UX

### 3. Caching Strategy
```python
# Cache generated images to avoid regenerating
import hashlib

def get_cache_key(prompt, model):
    return hashlib.md5(f"{prompt}_{model}".encode()).hexdigest()

# Check cache before API call
cache_key = get_cache_key(prompt, model)
if cache_key in image_cache:
    return image_cache[cache_key]
```

### 4. Input Validation
```python
def validate_prompt(prompt):
    if not prompt or len(prompt.strip()) < 3:
        raise ValueError("Prompt must be at least 3 characters long")
    if len(prompt) > 500:
        raise ValueError("Prompt too long (max 500 characters)")
    return prompt.strip()
```

## 🔗 Sample Langflow JSON Configuration

```json
{
  "nodes": [
    {
      "id": "text_input",
      "type": "TextInput",
      "data": {
        "label": "Image Prompt",
        "placeholder": "Enter your image description..."
      }
    },
    {
      "id": "api_request",
      "type": "APIRequest",
      "data": {
        "method": "POST",
        "url": "https://your-app-name.onrender.com/generate-image",
        "headers": {"Content-Type": "application/json"},
        "body_template": {
          "prompt": "{{text_input.value}}",
          "model": "runwayml/stable-diffusion-v1-5"
        }
      }
    },
    {
      "id": "image_output",
      "type": "ImageOutput",
      "data": {
        "base64_source": "{{api_request.response.image_base64}}"
      }
    }
  ],
  "edges": [
    {"source": "text_input", "target": "api_request"},
    {"source": "api_request", "target": "image_output"}
  ]
}
```

## 🚀 Quick Start Steps

1. **Deploy your API** on Render (following DEPLOYMENT.md)
2. **Get your API URL**: `https://your-app-name.onrender.com`
3. **In Langflow**:
   - Add API Request node
   - Set URL to your endpoint
   - Configure POST method with JSON body
   - Connect text input for prompts
   - Add image display for output
4. **Test** with a simple prompt like "a cat in space"

## 📝 Notes

- **First request** to Render might be slow (cold start)
- **Timeout**: Set to 120+ seconds for image generation
- **Models**: Use `runwayml/stable-diffusion-v1-5` for best reliability
- **Error handling**: Always include timeout and error handling
- **Rate limiting**: Be mindful of API rate limits

Your Langflow workflow can now generate AI images using your deployed Render API! 🎨
