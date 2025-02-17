import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Load the Excel sheet into a pandas DataFrame
df = pd.read_excel('your_excel_file.xlsx')  # Replace with the actual path to your Excel file

# Define a Pydantic model for the request body
class CargoRequest(BaseModel):
    cargo: str

@app.post("/get_iso_tank")
async def get_iso_tank(cargo_request: CargoRequest):
    cargo = cargo_request.cargo

    if not cargo:
        raise HTTPException(status_code=400, detail="Cargo not provided")

    # Look for either the Cargo Name or UN No. match in the DataFrame
    result = df[(df['Cargo Name'].str.contains(cargo, case=False, na=False)) | (df['UN No.'] == cargo)]

    if not result.empty:
        # Extract the suitable ISO Tank from the DataFrame (Column Z is the 'UNTANKINS' column)
        iso_tank = result.iloc[0]['UNTANKINS']
        return {"iso_tank": iso_tank}
    else:
        raise HTTPException(status_code=404, detail="No suitable ISO Tank found")
