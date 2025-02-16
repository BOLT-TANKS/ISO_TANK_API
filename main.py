from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load the Excel file
EXCEL_FILE = "iso_tank_data.xlsx"

try:
    df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
except Exception as e:
    print("Error loading Excel file:", e)
    df = None

class CargoRequest(BaseModel):
    cargo: str

@app.post("/get_tank")
def get_suitable_tank(request: CargoRequest):
    if df is None:
        raise HTTPException(status_code=500, detail="Excel file not found or corrupted.")
    
    cargo_input = str(request.cargo).strip().lower()
    
    matched_row = df[(df["UN No."].astype(str).str.lower() == cargo_input) |
                     (df["Cargo Name"].astype(str).str.lower() == cargo_input)]
    
    if not matched_row.empty:
        tank_type = matched_row.iloc[0]["Suitable ISO Tank Type"]
        return {"message": f"The suitable ISO Tank for {request.cargo} is {tank_type}"}
    else:
        raise HTTPException(status_code=404, detail="No suitable tank found for this cargo.")
