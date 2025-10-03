#!/usr/bin/env python3
"""
Test script for the Age & Gender Prediction API
"""

import requests
import sys
import os
import base64
from pathlib import Path


API_URL = os.getenv("API_URL", "http://localhost:8000")


def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✓ Health check passed")


def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Root endpoint passed")


def test_predict_file(image_path):
    """Test prediction with file upload"""
    print("\n=== Testing File Upload Prediction ===")

    if not os.path.exists(image_path):
        print(f"⚠ Image file not found: {image_path}")
        return

    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_URL}/predict", files=files)

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        result = response.json()
        assert "age" in result
        assert "gender" in result
        assert "prediction" in result["age"]
        assert "confidence" in result["age"]
        print("✓ File upload prediction passed")
    else:
        print(f"✗ File upload prediction failed: {response.text}")


def test_predict_url():
    """Test prediction with image URL"""
    print("\n=== Testing URL Prediction ===")

    # Using a sample image URL (this might fail if the URL is not accessible)
    test_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/300px-Cat03.jpg"

    data = {"url": test_url}
    response = requests.post(f"{API_URL}/predict/url", json=data)

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        result = response.json()
        assert "age" in result
        assert "gender" in result
        print("✓ URL prediction passed")
    else:
        print(
            f"⚠ URL prediction failed (expected for non-human images): {response.json()}"
        )


def test_predict_base64(image_path):
    """Test prediction with base64 encoded image"""
    print("\n=== Testing Base64 Prediction ===")

    if not os.path.exists(image_path):
        print(f"⚠ Image file not found: {image_path}")
        return

    with open(image_path, "rb") as f:
        image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    data = {"image": image_b64}
    response = requests.post(f"{API_URL}/predict/base64", json=data)

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        result = response.json()
        assert "age" in result
        assert "gender" in result
        print("✓ Base64 prediction passed")
    else:
        print(f"✗ Base64 prediction failed: {response.text}")


def test_invalid_inputs():
    """Test error handling with invalid inputs"""
    print("\n=== Testing Error Handling ===")

    # Test with no file
    response = requests.post(f"{API_URL}/predict")
    print(f"No file - Status: {response.status_code} (expected 422)")
    assert response.status_code == 422

    # Test with invalid base64
    data = {"image": "invalid_base64!!!"}
    response = requests.post(f"{API_URL}/predict/base64", json=data)
    print(f"Invalid base64 - Status: {response.status_code} (expected 400)")
    assert response.status_code == 400

    print("✓ Error handling passed")


def main():
    """Run all tests"""
    print(f"Testing API at: {API_URL}")

    try:
        # Basic tests
        test_health()
        test_root()
        test_invalid_inputs()

        # Find a test image
        test_image = None
        possible_images = [
            "test_image.jpg",
            "test_image.png",
            "sample.jpg",
            "sample.png",
        ]

        for img in possible_images:
            if os.path.exists(img):
                test_image = img
                break

        if test_image:
            print(f"\nUsing test image: {test_image}")
            test_predict_file(test_image)
            test_predict_base64(test_image)
        else:
            print("\n⚠ No test image found. Skipping file upload tests.")
            print("  Create a test image named 'test_image.jpg' to test file uploads.")

        # Test URL (might fail if URL is down or image is not a person)
        test_predict_url()

        print("\n" + "=" * 50)
        print("All tests completed!")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print(f"\n✗ Error: Could not connect to API at {API_URL}")
        print("  Make sure the API is running with: make run")
        sys.exit(1)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
