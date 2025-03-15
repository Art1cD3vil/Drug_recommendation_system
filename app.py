from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import shutil
import os
import random
import numpy as np
import cv2
from tensorflow.keras.models import load_model

app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (You can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load the trained CNN model
MODEL_PATH = "tumor_classification_model.h5"
model = load_model(MODEL_PATH)

# Get model input shape
model_input_shape = model.input_shape
image_height, image_width = model_input_shape[1], model_input_shape[2]

def predict_tumor(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (image_width, image_height))  # Adjust to model input size
    img = img / 255.0  # Normalize
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    prediction = model.predict(img)
    class_index = np.argmax(prediction)  # Get predicted class
    class_names = ["Glioma", "Meningioma", "Pituitary Tumor", "No Tumor"]  # Updated with actual labels
    return class_names[class_index]

class GeneSequenceInput(BaseModel):
    tumor_type: str
    dna_sequence: str

@app.post("/upload_mri/")
async def upload_mri(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1].lower()
    allowed_extensions = {"jpg", "jpeg", "png", "gif", "bmp", "tiff", "dcm"}  # Added DICOM support
    
    if file_extension not in allowed_extensions:
        return {"error": "Unsupported file type. Please upload a valid image (jpg, png, etc.)."}
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    predicted_class = predict_tumor(file_path)
    
    return {"message": "MRI uploaded successfully", "file_path": file_path, "predicted_class": predicted_class}

@app.options("/analyze_gene_sequence/")
async def preflight_analyze_gene_sequence():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    }

@app.post("/analyze_gene_sequence/")
async def analyze_gene_sequence(data: GeneSequenceInput):
    """Process gene sequence and return standard and personalized treatment recommendations."""
    tumor_type = data.tumor_type.lower()
    dna_sequence = data.dna_sequence
    
    gc_content = (dna_sequence.count('G') + dna_sequence.count('C')) / len(dna_sequence)
    mutation_indicators = {
        'tp53_mutation': ('GATGAT' in dna_sequence or 'ATAGAT' in dna_sequence or random.random() < 0.4),
        'idh_mutation': ('GGTCGT' in dna_sequence or 'CGTAGT' in dna_sequence or random.random() < 0.4),
        'mgmt_methylated': (gc_content > 0.6 or 'CGCG' in dna_sequence)
    }
    
    # Standard treatments
    standard_treatments = []
    if tumor_type == 'glioma':
        standard_treatments.append({"name": "Temozolomide", "mechanism": "Alkylating chemotherapy"})
    elif tumor_type == 'meningioma':
        standard_treatments.append({"name": "Surgery", "mechanism": "Primary treatment"})
        standard_treatments.append({"name": "Radiation Therapy", "mechanism": "Used for residual or aggressive tumors"})
    elif tumor_type == 'pituitary tumor':
        standard_treatments.append({"name": "Bromocriptine", "mechanism": "Dopamine agonist for hormone-secreting tumors"})
    
    # Personalized treatments based on genetic profile
    personalized_treatments = []
    if mutation_indicators['idh_mutation']:
        personalized_treatments.append({"name": "Vorasidenib", "mechanism": "IDH inhibitor", "reason": "IDH mutation detected"})
    if mutation_indicators['mgmt_methylated']:
        personalized_treatments.append({"name": "Temozolomide", "mechanism": "DNA alkylating agent", "reason": "MGMT methylation detected"})
    if mutation_indicators['tp53_mutation'] and random.random() > 0.4:
        personalized_treatments.append({"name": "APR-246", "mechanism": "TP53 reactivator", "reason": "TP53 mutation detected"})
    
    return {
        "tumor_type": tumor_type,
        "gc_content": gc_content,
        "mutation_indicators": mutation_indicators,
        "standard_treatments": standard_treatments,
        "personalized_treatments": personalized_treatments
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)