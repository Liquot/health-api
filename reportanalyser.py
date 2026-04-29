from PIL import Image
import re
from model import get_recommendation


import requests
import base64
import os

import requests
import base64
import os

def extract_text(image_path):
    with open(image_path, "rb") as img:
        img_base64 = base64.b64encode(img.read()).decode()

    API_KEY = os.getenv("VISION_API_KEY")  # safer

    url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

    body = {
        "requests": [
            {
                "image": {"content": img_base64},
                "features": [{"type": "TEXT_DETECTION"}]
            }
        ]
    }

    response = requests.post(url, json=body)
    result = response.json()

    print("FULL GOOGLE RESPONSE:", result)

    if "responses" in result:
        return result["responses"][0].get("fullTextAnnotation", {}).get("text", "")
    else:
        print("OCR FAILED:", result)
        return ""


def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace(":", " ")
    return text


def extract_values(text):
    data = {}

    # Hemoglobin
    hb = re.search(r'Hemoglobin.*?(\d+\.?\d*)', text, re.I)
    data['hemoglobin'] = float(hb.group(1)) if hb else None

    # Vitamin B12
    b12 = re.search(r'Vitamin B12\s+(\d+\.?\d*)', text, re.I)
    data['b12'] = float(b12.group(1)) if b12 else None

    # Vitamin D
    vitd = re.search(r'Vitamin D.*?(\d+\.?\d*)', text, re.I)
    data['vitamin_d'] = float(vitd.group(1)) if vitd else None

    # Cholesterol
    chol = re.search(r'Cholesterol.*?(\d+\.?\d*)', text, re.I)
    data['cholesterol'] = float(chol.group(1)) if chol else None

    # Calcium
    cal = re.search(r'Calcium\s+(\d+\.?\d*)', text, re.I)
    data['calcium'] = float(cal.group(1)) if cal else None

    return data


def fill_defaults(data):
    defaults = {
        "age": 25,
        "protein": 6,
        "diet_type": 0,
        "genetic_iron_deficiency": 0,
        "genetic_b12_deficiency": 0,
        "genetic_vitd_deficiency": 0,
        "family_diabetes": 0,
        "family_heart_disease": 0,
        "gender": 0,
        "cycle_phase": 0,
        "heavy_bleeding": 0,
        "pcos_risk": 0
    }

    for k, v in defaults.items():
        if data.get(k) is None:
            data[k] = v

    return data


def analyze_report(image_path):
    text = extract_text(image_path)
    text = clean_text(text)

    data = extract_values(text)
    data = fill_defaults(data)

    recommendations = get_recommendation(data)

    # Health insights
    # Health insights
    # Health insights
    # Health insights
    insights = []
    
    if data['hemoglobin'] is not None and data['hemoglobin'] < 12:
        insights.append("Low Hemoglobin → Risk of anemia")
    
    if data['vitamin_d'] is not None and data['vitamin_d'] < 20:
        insights.append("Low Vitamin D → Bone weakness risk")
    
    if data['b12'] is not None and data['b12'] < 300:
        insights.append("Low Vitamin B12 → Fatigue / nerve issues")
    
    if data['cholesterol'] is not None and data['cholesterol'] > 200:
        insights.append("High Cholesterol → Heart risk")

    return {
    "values": {
        "hemoglobin": data['hemoglobin'],
        "b12": data['b12'],
        "vitamin_d": data['vitamin_d'],
        "cholesterol": data['cholesterol'],
        "calcium": data['calcium']
    },
    "insights": insights,
    "supplements": recommendations['supplements'],
    "diet": recommendations['diet']
}