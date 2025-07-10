import os
import io
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file (for local development)
load_dotenv()

app = FastAPI(
    title="AI Image Generator", 
    description="Generate images from text prompts using Stable Diffusion",
    version="1.0.0"
)

# Add CORS middleware for web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Hugging Face client
try:
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise ValueError("HF_TOKEN environment variable not set")
    
    client = InferenceClient(api_key=hf_token)
except Exception as e:
    print(f"Warning: Failed to initialize Hugging Face client: {e}")
    client = None

class ImageRequest(BaseModel):
    prompt: str
    model: str = "stabilityai/stable-diffusion-3.5-large"  # Default model
    
class ImageResponse(BaseModel):
    success: bool
    message: str
    image_base64: str = None

@app.get("/")
async def root():
    return {
        "message": "AI Image Generator API", 
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    hf_status = "connected" if client else "not connected"
    return {
        "status": "healthy",
        "huggingface": hf_status,
        "version": "1.0.0"
    }

@app.post("/generate-image", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    """
    Generate an image from a text prompt
    """
    if not client:
        raise HTTPException(status_code=503, detail="Hugging Face client not initialized. Check HF_TOKEN.")
    
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        # Generate image using Hugging Face
        image = client.text_to_image(
            request.prompt,
            model=request.model
        )
        
        # Convert PIL Image to base64 string
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Encode to base64
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        
        return ImageResponse(
            success=True,
            message="Image generated successfully",
            image_base64=img_base64
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

@app.post("/generate-image-file")
async def generate_image_file(request: ImageRequest):
    """
    Generate an image and return it as a file download
    """
    if not client:
        raise HTTPException(status_code=503, detail="Hugging Face client not initialized. Check HF_TOKEN.")
    
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        # Generate image using Hugging Face
        image = client.text_to_image(
            request.prompt,
            model=request.model
        )
        
        # Convert PIL Image to bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(img_buffer.read()),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=generated_image.png"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

@app.get("/models")
async def get_available_models():
    """
    Get list of available models
    """
    models = [
        "runwayml/stable-diffusion-v1-5",
        "stabilityai/stable-diffusion-2-1",
        "stabilityai/stable-diffusion-3.5-large",
        "CompVis/stable-diffusion-v1-4"
    ]
    return {"available_models": models}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
