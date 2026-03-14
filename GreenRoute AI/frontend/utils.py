import requests

API_URL = "http://127.0.0.1:8000/predict"

def get_prediction(uploaded_file):

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    try:
        response = requests.post(API_URL, files=files)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {
            "label": "Error",
            "confidence": 0.0,
            "message": str(e)
        }