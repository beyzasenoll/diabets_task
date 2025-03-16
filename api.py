import time
import uvicorn
import pandas as pd
from fastapi import FastAPI, Depends
from catboost import CatBoostClassifier
from data_models import Patient, ResponseModel


def load_model(model_path: str = "artifacts/scoring_model.cbm") -> CatBoostClassifier:
    """Load and return the CatBoost model."""
    model = CatBoostClassifier()
    model.load_model(model_path)
    return model


# Load model at startup to avoid reloading on each request
MODEL = load_model()


def get_score(patient_data: dict, model: CatBoostClassifier = MODEL) -> float:
    """Calculate the probability score for a given patient."""
    dataframe = pd.DataFrame([patient_data])
    score = model.predict_proba(dataframe)[0][1]
    return score


# FastAPI instance
app = FastAPI(title="Patient Risk Scoring API", version="1.0",
              description="API to assess patient risk based on input features.")


@app.post("/check_patient/", response_model=ResponseModel)
def check_patient(patient: Patient, model: CatBoostClassifier = Depends(lambda: MODEL)):
    """Check the patient's risk score and classify them as High or Low risk."""
    start_time = time.time()
    score = get_score(patient.dict(), model)
    runtime = round(time.time() - start_time, 2)
    classification = "High Risk" if score > 0.5 else "Low Risk"

    return {"Score": score, "classification": classification, "runtime": runtime}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=5000, reload=True)
