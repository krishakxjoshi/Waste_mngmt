from fastapi import FastAPI, UploadFile, File
from prediction import predict
from schema import PredictionResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Waste Classifier API Running"}

@app.post("/predict", response_model=PredictionResponse)
async def get_prediction(file: UploadFile = File(...)):

    label, confidence = predict(file.file)

    return PredictionResponse(
        label = label,
        confidence = confidence
    )