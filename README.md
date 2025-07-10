# AI Image Generator API

A FastAPI-based service that generates images from text prompts using Hugging Face's Stable Diffusion models.

## 🚀 Getting Started

### Local Development

#### 1. Clone and Setup
```bash
git clone <your-repo>
cd image_generator
```

#### 2. Create Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Configure Environment
Create a `.env` file:
```
HF_TOKEN=your_hugging_face_token_here
```

#### 4. Start the API Server
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 🌐 Deployment

#### Deploy to Render
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Quick deploy:
1. Push code to GitHub
2. Connect to Render
3. Set `HF_TOKEN` environment variable
4. Deploy using the included `render.yaml`

### 2. API Endpoints

#### Health Check
- **GET** `/health` - Check if API is running
- **GET** `/` - Root endpoint with API info

#### Image Generation
- **POST** `/generate-image` - Generate image and return as base64
- **POST** `/generate-image-file` - Generate image and return as file download

#### Models
- **GET** `/models` - Get list of available models

## 📖 API Documentation

Once the server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Usage Examples

### Using curl

#### Generate Image (Base64 Response)
```bash
curl -X POST "http://localhost:8000/generate-image" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A beautiful sunset over mountains",
       "model": "runwayml/stable-diffusion-v1-5"
     }'
```

#### Generate Image (File Download)
```bash
curl -X POST "http://localhost:8000/generate-image-file" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A cute cat in space",
       "model": "runwayml/stable-diffusion-v1-5"
     }' \
     --output generated_image.png
```

#### Get Available Models
```bash
curl -X GET "http://localhost:8000/models"
```

### Using Python

```python
import requests
import base64
from PIL import Image
import io

# Generate image
response = requests.post(
    "http://localhost:8000/generate-image",
    json={
        "prompt": "Astronaut riding a horse",
        "model": "runwayml/stable-diffusion-v1-5"
    }
)

if response.status_code == 200:
    result = response.json()
    if result["success"]:
        # Decode and save image
        image_data = base64.b64decode(result["image_base64"])
        image = Image.open(io.BytesIO(image_data))
        image.save("my_image.png")
        print("Image saved!")
```

### Using JavaScript/Fetch

```javascript
// Generate image
fetch('http://localhost:8000/generate-image', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        prompt: "Beautiful landscape with mountains",
        model: "runwayml/stable-diffusion-v1-5"
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Create image element from base64
        const img = document.createElement('img');
        img.src = `data:image/png;base64,${data.image_base64}`;
        document.body.appendChild(img);
    }
});
```

## 🎨 Available Models

- `runwayml/stable-diffusion-v1-5` (Default, most reliable)
- `stabilityai/stable-diffusion-2-1`
- `stabilityai/stable-diffusion-3.5-large`
- `CompVis/stable-diffusion-v1-4`

## 📝 Request Format

```json
{
    "prompt": "Your text prompt here",
    "model": "runwayml/stable-diffusion-v1-5"  // Optional, defaults to stable-diffusion-v1-5
}
```

## 📤 Response Format

### Success Response (Base64)
```json
{
    "success": true,
    "message": "Image generated successfully",
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

### Error Response
```json
{
    "detail": "Error generating image: [error message]"
}
```

## 🧪 Testing

Run the test client:
```bash
python test_client.py
```

## 🔒 Environment Variables

Make sure your `.env` file contains:
```
HF_TOKEN=your_hugging_face_token_here
```

## 📊 Features

- ✅ Multiple Stable Diffusion models
- ✅ Base64 image response
- ✅ File download response
- ✅ Error handling
- ✅ Health checks
- ✅ Interactive API documentation
- ✅ CORS support ready
- ✅ Async support
# image_generator
