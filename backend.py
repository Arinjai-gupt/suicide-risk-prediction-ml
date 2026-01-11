from fastapi import FastAPI
import torch
import torch.nn as nn
import numpy as np
from pydantic import BaseModel

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow Streamlit Cloud
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the model class (same as in notebook)
class LogisticRegressionModel(nn.Module):
    def __init__(self, input_dim=5):
        super().__init__()
        self.linear = nn.Linear(input_dim, 1)
    
    def forward(self, x):
        return self.linear(x)

# Load the model
model = LogisticRegressionModel()
model.load_state_dict(torch.load('suicide_risk_model.pth'))
model.eval()

# Input schema
class InputData(BaseModel):
    Depression_Score: float
    Anxiety_Score: float
    Stress_Level: float
    Social_Support_Score: float
    Self_Esteem_Score: float

@app.get("/")
def read_root():
    return {"message": "Suicide Risk Prediction API", "docs": "/docs"}

@app.post("/predict")
def predict(data: InputData):
    input_tensor = torch.tensor([[data.Depression_Score, data.Anxiety_Score, data.Stress_Level, data.Social_Support_Score, data.Self_Esteem_Score]], dtype=torch.float32)
    with torch.no_grad():
        logit = model(input_tensor)
        prob = torch.sigmoid(logit).item()
    return {"suicide_risk_probability": prob}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)