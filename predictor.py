#!/usr/bin/env python3
"""
Age and Gender Predictor using ONNX Runtime
Simplified version without HuggingFace-specific code
"""

import os
import io
import numpy as np
from PIL import Image
import onnxruntime as ort
from torchvision import transforms
import glob


class AgeGenderPredictor:
    """Age and Gender prediction model using ONNX Runtime"""

    def __init__(self, model_path=None):
        """
        Initialize the predictor

        Args:
            model_path: Path to the ONNX model file. If None, will search common locations.
        """
        # Load the model - search in multiple locations
        if model_path is None:
            model_path = os.environ.get("MODEL_PATH", "model_quantized.onnx")

        # Try different potential locations for the model file
        possible_paths = [
            model_path,
            os.path.join(os.path.dirname(__file__), model_path),
            os.path.join("/app", model_path),
        ]

        # Also search for any .onnx files in common locations
        onnx_files = glob.glob("*.onnx") + glob.glob("/app/*.onnx")
        possible_paths.extend(onnx_files)

        # Try to load the model from any of the possible paths
        model_loaded = False
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Found model at: {path}")
                try:
                    self.session = ort.InferenceSession(path)
                    model_loaded = True
                    print(f"Successfully loaded model from: {path}")
                    break
                except Exception as e:
                    print(f"Error loading model from {path}: {str(e)}")

        if not model_loaded:
            raise RuntimeError(
                f"Could not find model file. Searched paths: {possible_paths}"
            )

        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [output.name for output in self.session.get_outputs()]

        # Image preprocessing - standard ImageNet preprocessing
        self.transform = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        # Load class mappings
        self.age_classes = os.environ.get(
            "AGE_CLASSES", "18-24,25-34,35-44,45-54,55+"
        ).split(",")

        self.gender_classes = ["Woman", "Man"]

    def preprocess(self, image_bytes):
        """
        Preprocess image bytes for model inference

        Args:
            image_bytes: Raw image bytes

        Returns:
            Preprocessed numpy array ready for inference
        """
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Apply transformations
        image_tensor = self.transform(image)

        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)

        return image_tensor.numpy()

    def predict(self, image_bytes):
        """
        Predict age and gender from image bytes

        Args:
            image_bytes: Raw image bytes

        Returns:
            Dictionary with age and gender predictions including confidence scores
        """
        # Preprocess the image
        input_data = self.preprocess(image_bytes)

        # Run inference
        results = self.session.run(self.output_names, {self.input_name: input_data})

        # Process results
        age_logits, gender_logits = results

        # Reshape if needed
        if age_logits.ndim == 1:
            age_logits = age_logits.reshape(1, -1)
        if gender_logits.ndim == 1:
            gender_logits = gender_logits.reshape(1, -1)

        age_pred = np.argmax(age_logits, axis=1)[0]
        gender_pred = np.argmax(gender_logits, axis=1)[0]

        # Calculate probabilities using softmax
        age_probs = np.exp(age_logits) / np.sum(
            np.exp(age_logits), axis=1, keepdims=True
        )
        gender_probs = np.exp(gender_logits) / np.sum(
            np.exp(gender_logits), axis=1, keepdims=True
        )

        # Get prediction with confidence
        age_confidence = float(age_probs[0][age_pred])
        gender_confidence = float(gender_probs[0][gender_pred])

        return {
            "age": {
                "prediction": self.age_classes[age_pred],
                "confidence": age_confidence,
                "all_probabilities": {
                    self.age_classes[i]: float(age_probs[0][i])
                    for i in range(len(self.age_classes))
                },
            },
            "gender": {
                "prediction": self.gender_classes[gender_pred],
                "confidence": gender_confidence,
                "all_probabilities": {
                    self.gender_classes[i]: float(gender_probs[0][i])
                    for i in range(len(self.gender_classes))
                },
            },
        }
