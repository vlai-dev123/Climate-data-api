from climate_io import SAMPLE_CSV_DATA, EmissionsCalculator, EmissionsDataValidator


def test_emissions_validator():
    """Example test case"""
    validator = EmissionsDataValidator(SAMPLE_CSV_DATA)
    df, errors, warnings = validator.validate_and_clean()
    
    # Assertions
    assert df is not None, "DataFrame should be created"
    assert len(df) > 0, "Should have valid rows"
    assert 'total_emissions' not in df.columns, "Calculated fields not added yet"
    
    print("✓ Validation test passed")

def test_emissions_calculator():
    """Test calculations"""
    validator = EmissionsDataValidator(SAMPLE_CSV_DATA)
    df, _, _ = validator.validate_and_clean()
    
    df = EmissionsCalculator.calculate_metrics(df)
    
    assert 'total_emissions' in df.columns
    assert 'carbon_intensity' in df.columns
    assert (df['total_emissions'] >= 0).all()
    
    print("✓ Calculator test passed")