from climate_io import EmissionsCalculator, EmissionsDataValidator
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI(title="Climate Data API")

class EmissionsUploadResponse(BaseModel):
    status: str
    message: str
    records_processed: int
    errors: List[str]
    warnings: List[str]
    summary: Optional[Dict] = None

class FacilitySummary(BaseModel):
    facility_id: str
    facility_name: str
    total_emissions: float
    carbon_intensity: float

@app.post("/api/v1/emissions/upload", response_model=EmissionsUploadResponse)
async def upload_emissions_data(file: UploadFile = File(...)):
    """
    Upload and process emissions data from CSV file
    
    Expected CSV format:
    facility_id,facility_name,month,year,scope1_emissions,scope2_emissions,revenue
    """
    
    try:
        # Read file content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Validate and clean data
        validator = EmissionsDataValidator(csv_content)
        df, errors, warnings = validator.validate_and_clean()
        
        # If critical errors, return immediately
        if errors and df is None:
            raise HTTPException(
                status_code=400,
                detail={"errors": errors, "warnings": warnings}
            )
        
        # Calculate metrics
        df = EmissionsCalculator.calculate_metrics(df)
        
        # Generate summary
        facility_summary = EmissionsCalculator.aggregate_by_facility(df)
        trends = EmissionsCalculator.calculate_trends(df)
        
        # In production, you would save to database here
        # db.save_emissions_data(df)
        
        return EmissionsUploadResponse(
            status="success" if not errors else "partial_success",
            message=f"Processed {len(df)} records successfully",
            records_processed=len(df),
            errors=errors,
            warnings=warnings,
            summary={
                "facilities": facility_summary,
                "trends": trends,
                "total_emissions": float(df['total_emissions'].sum()),
                "average_carbon_intensity": float(
                    df['carbon_intensity'].mean()
                )
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/v1/facilities/{facility_id}/emissions")
async def get_facility_emissions(
    facility_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Retrieve emissions data for a specific facility
    
    In production, this would query the database
    """
    # Placeholder - would query database
    return {
        "facility_id": facility_id,
        "message": "This would return emissions data from database",
        "filters": {
            "start_date": start_date,
            "end_date": end_date
        }
    }