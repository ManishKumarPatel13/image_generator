# Deployment Guide for Render

## Prerequisites
1. GitHub repository with your code
2. Render account (https://render.com)
3. Hugging Face token

## Deployment Steps

### 1. Prepare Your Repository
```bash
# Add all files to git
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)
1. Go to https://render.com/dashboard
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Set environment variables in the Render dashboard:
   - `HF_TOKEN`: Your Hugging Face token

#### Option B: Manual Setup
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: ai-image-generator
   - **Environment**: Python 3
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `HF_TOKEN`: Your Hugging Face token

### 3. Environment Variables
Set these in Render Dashboard → Your Service → Environment:
- `HF_TOKEN`: Your Hugging Face API token

### 4. Custom Domain (Optional)
- Go to Settings → Custom Domains
- Add your domain and configure DNS

## Important Notes

### Performance
- **Free Tier**: Spins down after 15 minutes of inactivity
- **Paid Tier**: Always on, better performance
- **Memory**: Image generation is memory-intensive

### Scaling
- Consider using **Starter** plan or higher for production
- Enable **Auto-Deploy** for automatic updates

### Security
- Never commit `.env` file to git
- Use Render's environment variables for secrets
- Consider restricting CORS origins in production

### Monitoring
- Check logs in Render Dashboard
- Use `/health` endpoint for monitoring
- Monitor response times and errors

## Testing Your Deployment

Once deployed, test your API:

```bash
# Replace YOUR_RENDER_URL with your actual URL
curl -X POST "https://YOUR_RENDER_URL.onrender.com/generate-image" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A beautiful sunset",
       "model": "runwayml/stable-diffusion-v1-5"
     }'
```

## Troubleshooting

### Common Issues:
1. **Build fails**: Check requirements.txt versions
2. **HF_TOKEN error**: Verify token is set correctly
3. **Memory issues**: Use smaller models or upgrade plan
4. **Timeout**: Image generation can take 30-60 seconds
5. **Pillow build error**: Use requirements-minimal.txt instead

### Pillow Build Error Fix:
If you get a Pillow build error like "KeyError: '__version__'", try these solutions:

#### Solution 1: Use Minimal Requirements
Replace `requirements.txt` content with:
```
fastapi
uvicorn[standard]
huggingface_hub
pillow
python-dotenv
pydantic
```

#### Solution 2: Update Build Command
In Render dashboard or render.yaml:
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
```

#### Solution 3: Force Python Version
In render.yaml, set:
```yaml
envVars:
  - key: PYTHON_VERSION
    value: 3.11.9
```

### Memory Issues:
- **Free Tier**: Limited memory, may fail on larger models
- **Solution**: Use `runwayml/stable-diffusion-v1-5` (most memory efficient)
- **Upgrade**: Consider Starter plan ($7/month) for better reliability

### Deployment Verification:
After deployment, test these endpoints:
```bash
# Health check
curl https://your-app.onrender.com/health

# Test image generation
curl -X POST "https://your-app.onrender.com/generate-image" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "test image", "model": "runwayml/stable-diffusion-v1-5"}'
```

### Logs:
Check Render Dashboard → Your Service → Logs for detailed error messages.
