from climate_io import SAMPLE_CSV_DATA, EmissionsCalculator, EmissionsDataValidator
from testing import test_emissions_calculator, test_emissions_validator


if __name__ == "__main__":
    print("=" * 60)
    print("CLIMATE DATA PROCESSING DEMO")
    print("=" * 60)
    
    # Step 1: Validate data
    print("\n1. VALIDATING DATA...")
    validator = EmissionsDataValidator(SAMPLE_CSV_DATA)
    df, errors, warnings = validator.validate_and_clean()
    
    print(f"   Errors: {len(errors)}")
    for error in errors:
        print(f"   ❌ {error}")
    
    print(f"   Warnings: {len(warnings)}")
    for warning in warnings:
        print(f"   ⚠️  {warning}")
    
    # Step 2: Calculate metrics
    print("\n2. CALCULATING METRICS...")
    df = EmissionsCalculator.calculate_metrics(df)
    print(f"   Processed {len(df)} records")
    print(f"   Added columns: {['total_emissions', 'carbon_intensity', 'date']}")
    
    # Step 3: Generate aggregations
    print("\n3. FACILITY AGGREGATIONS:")
    facility_summary = EmissionsCalculator.aggregate_by_facility(df)
    for facility in facility_summary:
        print(f"\n   {facility['facility_name']} ({facility['facility_id']})")
        print(f"   - Total Emissions: {facility['total_emissions']:.2f} tCO2e")
        print(f"   - Carbon Intensity: {facility['carbon_intensity']:.2f} tCO2e/$1M")
    
    # Step 4: Calculate trends
    print("\n4. MONTH-OVER-MONTH TRENDS:")
    trends = EmissionsCalculator.calculate_trends(df)
    for trend in trends:
        change = trend['change_from_previous_month_pct']
        change_str = f"{change:+.1f}%" if change else "N/A"
        print(f"   {trend['facility_name']}: {change_str}")
    
    print("\n" + "=" * 60)
    print("✓ PROCESSING COMPLETE")
    print("=" * 60)
    
    # Run tests
    print("\nRUNNING TESTS...")
    test_emissions_validator()
    test_emissions_calculator()
    print("\n✓ ALL TESTS PASSED")