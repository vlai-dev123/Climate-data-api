import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import json

# Sample input data (what a customer might upload)
SAMPLE_CSV_DATA = """
facility_id,facility_name,month,year,scope1_emissions,scope2_emissions,revenue
F001,Malaysia HQ,1,2024,150.5,80.2,500000
F001,Malaysia HQ,2,2024,145.0,78.5,520000
F002,Singapore Office,1,2024,45.0,120.0,300000
F002,Singapore Office,2,2024,48.5,125.0,310000
F003,Jakarta Plant,1,2024,invalid,200.0,800000
"""

class EmissionsDataValidator:
    """Validates and cleans emissions data"""
    
    REQUIRED_COLUMNS = [
        'facility_id', 'facility_name', 'month', 'year',
        'scope1_emissions', 'scope2_emissions', 'revenue'
    ]
    
    def __init__(self, csv_content: str):
        self.raw_data = csv_content
        self.df = None
        self.errors = []
        self.warnings = []
    
    def validate_and_clean(self) -> tuple[pd.DataFrame, List[str], List[str]]:
        """Main validation pipeline"""
        try:
            # Load CSV
            self.df = pd.read_csv(pd.io.common.StringIO(self.raw_data))
            
            # Run validation checks
            self._check_required_columns()
            self._validate_datatypes()
            self._check_business_rules()
            self._clean_data()
            
            return self.df, self.errors, self.warnings
        
        except Exception as e:
            self.errors.append(f"Failed to parse CSV: {str(e)}")
            return None, self.errors, self.warnings
    
    def _check_required_columns(self):
        """Ensure all required columns are present"""
        missing = set(self.REQUIRED_COLUMNS) - set(self.df.columns)
        if missing:
            self.errors.append(f"Missing required columns: {missing}")
    
    def _validate_datatypes(self):
        """Convert and validate data types"""
        # Convert numeric columns
        for col in ['scope1_emissions', 'scope2_emissions', 'revenue']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
            # Track rows with invalid data
            invalid_rows = self.df[self.df[col].isna()].index.tolist()
            if invalid_rows:
                self.warnings.append(
                    f"Invalid values in {col} at rows: {invalid_rows}"
                )
        
        # Validate month and year
        self.df['month'] = pd.to_numeric(self.df['month'], errors='coerce')
        self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')
    
    def _check_business_rules(self):
        """Apply business logic validation"""
        # Month must be 1-12
        invalid_months = self.df[
            (self.df['month'] < 1) | (self.df['month'] > 12)
        ]
        if not invalid_months.empty:
            self.errors.append(f"Invalid month values found")
        
        # Emissions cannot be negative
        for col in ['scope1_emissions', 'scope2_emissions']:
            negative = self.df[self.df[col] < 0]
            if not negative.empty:
                self.errors.append(f"Negative values found in {col}")
        
        # Revenue should be positive
        zero_revenue = self.df[self.df['revenue'] <= 0]
        if not zero_revenue.empty:
            self.warnings.append("Zero or negative revenue found")
    
    def _clean_data(self):
        """Remove invalid rows"""
        # Drop rows where critical fields are missing
        self.df = self.df.dropna(
            subset=['facility_id', 'month', 'year']
        )


class EmissionsCalculator:
    """Calculate carbon intensity and aggregated metrics"""
    
    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Add calculated fields to dataframe"""
        # Total emissions (Scope 1 + Scope 2)
        df['total_emissions'] = (
            df['scope1_emissions'].fillna(0) + 
            df['scope2_emissions'].fillna(0)
        )
        
        # Carbon intensity (emissions per revenue)
        # tCO2e per $1M revenue
        df['carbon_intensity'] = (
            df['total_emissions'] / (df['revenue'] / 1_000_000)
        )
        
        # Create date field for easier querying
        df['date'] = pd.to_datetime(
            df[['year', 'month']].assign(day=1)
        )
        
        return df
    
    @staticmethod
    def aggregate_by_facility(df: pd.DataFrame) -> Dict:
        """Aggregate emissions by facility"""
        agg_data = df.groupby('facility_id').agg({
            'facility_name': 'first',
            'total_emissions': 'sum',
            'scope1_emissions': 'sum',
            'scope2_emissions': 'sum',
            'revenue': 'sum',
            'carbon_intensity': 'mean'
        }).reset_index()
        
        return agg_data.to_dict('records')
    
    @staticmethod
    def calculate_trends(df: pd.DataFrame) -> Dict:
        """Calculate month-over-month trends"""
        df_sorted = df.sort_values(['facility_id', 'date'])
        
        trends = []
        for facility_id in df_sorted['facility_id'].unique():
            facility_data = df_sorted[
                df_sorted['facility_id'] == facility_id
            ].copy()
            
            # Calculate percentage change
            facility_data['emissions_change_pct'] = (
                facility_data['total_emissions']
                .pct_change() * 100
            )
            
            latest = facility_data.iloc[-1]
            trends.append({
                'facility_id': facility_id,
                'facility_name': latest['facility_name'],
                'latest_month': latest['date'].strftime('%Y-%m'),
                'latest_emissions': float(latest['total_emissions']),
                'change_from_previous_month_pct': (
                    float(latest['emissions_change_pct']) 
                    if pd.notna(latest['emissions_change_pct']) 
                    else None
                )
            })
        
        return trends