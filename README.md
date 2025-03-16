# Patient Readmission Prediction

## Project Overview  
This project aims to predict whether a patient will be readmitted to the hospital using machine learning techniques. The dataset used for this project is the **Diabetes 130-US hospitals dataset** from Kaggle. A **CatBoostClassifier** is trained and deployed using **FastAPI** and **Streamlit**, containerized with **Docker**, and deployed to the cloud.

---

## Project Workflow

### 1. Machine Learning Model Development
- The **Diabetes 130-US Hospitals dataset** was used to build the model.
- Data preprocessing steps included handling missing values, encoding categorical variables, and feature selection.
- **CatBoostClassifier** was trained to predict whether a patient would be readmitted.
- The trained model was saved as **scoring_model.cbm**.
- An additional imputer model (**imputer_model.cbm**) was created for missing values.

### 2. Streamlit Application Development
- A **Streamlit-based UI** was developed to visualize patient risk assessment.
- The app allows users to input patient data and get a prediction.
- SHAP values are displayed to explain model predictions.
- The trained model is loaded dynamically to predict patient readmission risk.

### 3. FastAPI Backend Development
- A **FastAPI backend** was created to expose the ML model as an API.
- The API receives patient data in JSON format and returns the risk classification.
- The endpoint `/check_patient/` was implemented for inference.
- **Pydantic** was used to validate incoming data.

### 4. Dockerization of the Application
- A **Dockerfile** was created to containerize the application.
- Both **FastAPI** and **Streamlit** run inside the same container.
- The application exposes **FastAPI on port 8000** and **Streamlit on port 8501**.
- Dependencies were managed with **requirements.txt**.

### **5. Cloud Deployment (Incomplete)**
- The Dockerized application was prepared for cloud deployment.
- Cloud services like **AWS, Google Cloud, or Azure** were considered, but the deployment has **not been completed yet**.
- Future steps will involve deploying the application using **AWS ECS, Google Cloud Run, or Azure App Service**.

---

## Project Structure

This project includes the following directories and files:

### `artifacts/` - Saved models and encoders
- `scoring_model.cbm` - Trained CatBoost model for prediction  
- `imputer_model.cbm` - Trained model for handling missing values  
- `demo_data.pq` - Sample patient data for testing  

### `data/` - Raw dataset
- `diabetic_data.csv` - Original dataset  

### `notebooks/` - Jupyter notebooks for exploration and training
- `diabetes_model_training.ipynb` - Model training notebook  
- [Open in Google Colab](https://colab.research.google.com/drive/1mKRX8_jwBJJU4IhYpzcO7_FcRHD9EKPu#scrollTo=a83214ca)  

### `app/` - Application files
- `api.py` - FastAPI backend for model inference  
- `streamlit_app.py` - Streamlit frontend for visualization  
- `data_models.py` - Pydantic models for input validation  

### Other Files
- `Dockerfile` - Configuration for Docker container  
- `requirements.txt` - Python dependencies  
- `README.md` - Project documentation  

---

## Dataset Information

- **Source:** [Kaggle - Diabetes 130-US Hospitals](https://www.kaggle.com/datasets/brandao/diabetes)  
- **File Used:** `diabetic_data.csv`  
- **Target Variable:** `readmitted` (Binary classification: 1 if readmitted, 0 if not)  

### Features Used
- **Demographics:** Age, gender, race  
- **Hospitalization details:** Number of inpatient visits, number of procedures, number of lab procedures  
- **Diagnosis:** Primary, secondary, tertiary diagnosis codes  
- **Medications:** Insulin usage, diabetes medication, A1C test results  
- **Other Factors:** Number of emergency visits, time in hospital

## Installation and Running Locally

### Install Dependencies
```bash
pip install -r requirements.txt
```
### Run the FastAPI Backend
```bash
uvicorn api:app --reload
```

### Run the Streamlit Frontend
```bash
 -r requirements.txt
```

## API Usage
Endpoint: POST /check_patient/
Request Body:
```
{
  "age": 65,
  "gender": "Male",
  "weight": 75.0,
  "admission_type_id": 1,
  "discharge_disposition_id": 1,
  "admission_source_id": 1,
  "time_in_hospital": 4,
  "num_lab_procedures": 10,
  "num_procedures": 2,
  "num_medications": 5,
  "number_outpatient": 0,
  "number_emergency": 1,
  "number_inpatient": 1,
  "diag_1": 250.1,
  "diag_2": 250.2,
  "diag_3": 250.3,
  "number_diagnoses": 3,
  "max_glu_serum": 0,
  "a1cresult": 1,
  "metformin": "Yes",
  "insulin": "No",
  "diabetesmed": "Yes",
  "race": "Caucasian"
}
```
Response Example:
```
{
  "Score": 0.72,
  "classification": "High Risk",
  "runtime": 0.03
}
```




