# SQL Schema for emissions tracking
DATABASE_SCHEMA = """
-- Companies table
CREATE TABLE companies (
    company_id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Facilities table (belongs to companies)
CREATE TABLE facilities (
    facility_id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) REFERENCES companies(company_id),
    facility_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    facility_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Monthly emissions data
CREATE TABLE emissions_data (
    id SERIAL PRIMARY KEY,
    facility_id VARCHAR(50) REFERENCES facilities(facility_id),
    reporting_date DATE NOT NULL,
    scope1_emissions DECIMAL(15, 2),
    scope2_emissions DECIMAL(15, 2),
    scope3_emissions DECIMAL(15, 2),
    total_emissions DECIMAL(15, 2),
    revenue DECIMAL(15, 2),
    carbon_intensity DECIMAL(10, 4),
    data_quality_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(facility_id, reporting_date)
);

-- Create indexes for common queries
CREATE INDEX idx_emissions_facility ON emissions_data(facility_id);
CREATE INDEX idx_emissions_date ON emissions_data(reporting_date);
CREATE INDEX idx_facility_company ON facilities(company_id);

-- Example query: Year-over-year comparison
-- SELECT 
--     f.facility_name,
--     DATE_PART('year', e.reporting_date) as year,
--     SUM(e.total_emissions) as annual_emissions,
--     AVG(e.carbon_intensity) as avg_carbon_intensity
-- FROM emissions_data e
-- JOIN facilities f ON e.facility_id = f.facility_id
-- WHERE e.reporting_date >= '2023-01-01'
-- GROUP BY f.facility_name, DATE_PART('year', e.reporting_date)
-- ORDER BY f.facility_name, year;
"""