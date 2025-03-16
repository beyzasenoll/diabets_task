from enum import Enum
from pydantic import BaseModel, Field, conint, confloat



# Enum for gender
class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

# Enum for race
class RaceEnum(str, Enum):
    AfricanAmerican = "AfricanAmerican"
    Caucasian = "Caucasian"
    Other = "Other"
    Asian = "Asian"
    Hispanic = "Hispanic"

# Input model
class Patient(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Age of the patient")
    gender: GenderEnum = Field(..., description="Gender of the patient")
    weight: float = Field(..., ge=30, le=200, description="Weight of the patient in kg")
    admission_type_id: int = Field(..., ge=1, description="Admission type ID")
    discharge_disposition_id: int = Field(..., ge=1, description="Discharge disposition ID")
    admission_source_id: int = Field(..., ge=1, description="Admission source ID")
    time_in_hospital: int = Field(..., ge=1, le=30, description="Days spent in hospital")
    num_lab_procedures: int = Field(..., ge=0, description="Number of lab procedures")
    num_procedures: int = Field(..., ge=0, description="Number of procedures")
    num_medications: int = Field(..., ge=0, description="Number of medications")
    number_outpatient: int = Field(..., ge=0, description="Number of outpatient visits")
    number_emergency: int = Field(..., ge=0, description="Number of emergency visits")
    number_inpatient: int = Field(..., ge=0, description="Number of inpatient visits")
    diag_1: float = Field(..., description="Primary diagnosis code")
    diag_2: float = Field(..., description="Secondary diagnosis code")
    diag_3: float = Field(..., description="Tertiary diagnosis code")
    number_diagnoses: int = Field(..., ge=1, description="Total number of diagnoses")
    max_glu_serum: int = Field(..., ge=0, description="Max glucose serum level")
    a1cresult: int = Field(..., ge=0, description="A1C test result")
    metformin: str
    insulin: str
    diabetesmed: str
    race: RaceEnum = Field(default=RaceEnum.Other, description="Race of the patient")

# Response model
class ResponseModel(BaseModel):
    Score: float
    classification: str
    runtime: float