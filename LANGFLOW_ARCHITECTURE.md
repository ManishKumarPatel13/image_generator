# Langflow + Render API Integration Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   LANGFLOW      │    │    RENDER API    │    │  HUGGING FACE API   │
│                 │    │                  │    │                     │
│  ┌───────────┐  │    │  ┌─────────────┐ │    │  ┌───────────────┐  │
│  │Text Input │  │    │  │   FastAPI   │ │    │  │Stable Diffusion│  │
│  │  Node     │  │    │  │  Server     │ │    │  │    Models     │  │
│  └─────┬─────┘  │    │  └──────┬──────┘ │    │  └───────────────┘  │
│        │        │    │         │        │    │                     │
│  ┌─────▼─────┐  │    │  ┌──────▼──────┐ │    │                     │
│  │API Request│  │────┤  │  POST       │ │────┤                     │
│  │   Node    │  │    │  │/generate-   │ │    │                     │
│  └─────┬─────┘  │    │  │ image       │ │    │                     │
│        │        │    │  └──────┬──────┘ │    │                     │
│  ┌─────▼─────┐  │    │         │        │    │                     │
│  │Image      │  │    │  ┌──────▼──────┐ │    │                     │
│  │Display    │  │    │  │  Response   │ │    │                     │
│  │   Node    │  │    │  │ {base64}    │ │    │                     │
│  └───────────┘  │    │  └─────────────┘ │    │                     │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
```

## Data Flow:

1. **User Input** → Langflow Text Input Node
2. **HTTP Request** → Langflow API Request Node → Render FastAPI
3. **AI Processing** → Render calls Hugging Face API
4. **Image Generation** → Stable Diffusion generates image
5. **Base64 Response** → Render returns JSON with base64 image
6. **Display** → Langflow converts base64 to image and displays

## Request/Response Format:

### Request (Langflow → Render):
```json
{
  "prompt": "A beautiful landscape with mountains",
  "model": "runwayml/stable-diffusion-v1-5"
}
```

### Response (Render → Langflow):
```json
{
  "success": true,
  "message": "Image generated successfully",
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

## Integration Benefits:

✅ **Serverless**: No local GPU needed
✅ **Scalable**: Render handles scaling
✅ **Reliable**: Hugging Face infrastructure
✅ **Fast**: Direct API integration
✅ **Flexible**: Multiple model support
✅ **Visual**: Langflow's drag-and-drop interface
