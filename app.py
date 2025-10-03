#!/usr/bin/env python3
"""
FastAPI application for Age and Gender Prediction
"""

import io
import base64
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import uvicorn

from predictor import AgeGenderPredictor

# Initialize FastAPI app
app = FastAPI(
    title="Age & Gender Prediction API",
    description="Predict age group and gender from images using a ResNet50-based model",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
predictor = None


@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup"""
    global predictor
    try:
        predictor = AgeGenderPredictor()
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise e


class ImageURLRequest(BaseModel):
    """Request model for image URL"""

    url: str


class Base64ImageRequest(BaseModel):
    """Request model for base64 encoded image"""

    image: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Age & Gender Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict_file": "/predict (POST with multipart/form-data)",
            "predict_url": "/predict/url (POST with JSON)",
            "predict_base64": "/predict/base64 (POST with JSON)",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": predictor is not None}


@app.post("/predict")
async def predict_from_file(file: UploadFile = File(...)):
    """
    Predict age and gender from uploaded image file

    Args:
        file: Image file (JPEG, PNG, etc.)

    Returns:
        JSON with age and gender predictions
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Read image bytes
        image_bytes = await file.read()

        # Validate it's an image
        try:
            Image.open(io.BytesIO(image_bytes))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Get predictions
        result = predictor.predict(image_bytes)

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/url")
async def predict_from_url(request: ImageURLRequest):
    """
    Predict age and gender from image URL

    Args:
        request: JSON with 'url' field containing image URL

    Returns:
        JSON with age and gender predictions
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        import requests

        # Download image
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(request.url, headers=headers, timeout=10)

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to download image from URL (Status: {response.status_code})",
            )

        image_bytes = response.content

        # Validate it's an image
        try:
            Image.open(io.BytesIO(image_bytes))
        except Exception:
            raise HTTPException(
                status_code=400, detail="URL does not point to a valid image"
            )

        # Get predictions
        result = predictor.predict(image_bytes)

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/base64")
async def predict_from_base64(request: Base64ImageRequest):
    """
    Predict age and gender from base64 encoded image

    Args:
        request: JSON with 'image' field containing base64 encoded image

    Returns:
        JSON with age and gender predictions
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Decode base64 image
        try:
            image_bytes = base64.b64decode(request.image)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid base64 string")

        # Validate it's an image
        try:
            Image.open(io.BytesIO(image_bytes))
        except Exception:
            raise HTTPException(
                status_code=400, detail="Decoded data is not a valid image"
            )

        # Get predictions
        result = predictor.predict(image_bytes)

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import os

    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(app, host=host, port=port)
