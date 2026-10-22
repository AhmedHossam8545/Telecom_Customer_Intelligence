-- Telecom Customer Intelligence Database Schema
-- Milestone 4: PostgreSQL Schema + Loading

-- Drop existing schemas if needed (uncomment for fresh start)
-- DROP SCHEMA IF EXISTS staging CASCADE;
-- DROP SCHEMA IF EXISTS core CASCADE;

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS core;

-- ============================================
-- STAGING TABLES (for initial data loading)
-- ============================================

CREATE TABLE IF NOT EXISTS staging.customer_info_staging (
    customer_id VARCHAR(50) PRIMARY KEY,
    age NUMERIC,
    gender VARCHAR(20),
    region VARCHAR(20),
    contract_type VARCHAR(20),
    monthly_charges NUMERIC(10, 2),
    signup_date DATE,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.usage_data_staging (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    month INTEGER,
    call_minutes NUMERIC(10, 2),
    data_usage_gb NUMERIC(10, 2),
    sms_count INTEGER,
    complaints INTEGER,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.churn_labels_staging (
    customer_id VARCHAR(50) PRIMARY KEY,
    churn INTEGER,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- CORE TABLES (with constraints and indexes)
-- ============================================

-- Customers table
CREATE TABLE IF NOT EXISTS core.customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    age NUMERIC NOT NULL,
    gender VARCHAR(20) NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    region VARCHAR(20) NOT NULL CHECK (region IN ('Urban', 'Suburban', 'Rural')),
    contract_type VARCHAR(20) NOT NULL CHECK (contract_type IN ('Monthly', 'Yearly', 'Prepaid')),
    monthly_charges NUMERIC(10, 2) NOT NULL CHECK (monthly_charges >= 0),
    signup_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer usage table
CREATE TABLE IF NOT EXISTS core.customer_usage (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    call_minutes NUMERIC(10, 2) NOT NULL CHECK (call_minutes >= 0),
    data_usage_gb NUMERIC(10, 2) NOT NULL CHECK (data_usage_gb >= 0),
    sms_count INTEGER NOT NULL CHECK (sms_count >= 0),
    complaints INTEGER NOT NULL CHECK (complaints >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usage_customer FOREIGN KEY (customer_id) REFERENCES core.customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT unique_customer_month UNIQUE (customer_id, month)
);

-- Churn labels table
CREATE TABLE IF NOT EXISTS core.churn_labels (
    customer_id VARCHAR(50) PRIMARY KEY,
    churn INTEGER NOT NULL CHECK (churn IN (0, 1)),
    observation_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_churn_customer FOREIGN KEY (customer_id) REFERENCES core.customers(customer_id) ON DELETE CASCADE
);

-- ============================================
-- INDEXES for performance
-- ============================================

-- Indexes on customers
CREATE INDEX IF NOT EXISTS idx_customers_region ON core.customers(region);
CREATE INDEX IF NOT EXISTS idx_customers_contract_type ON core.customers(contract_type);
CREATE INDEX IF NOT EXISTS idx_customers_signup_date ON core.customers(signup_date);

-- Indexes on customer_usage
CREATE INDEX IF NOT EXISTS idx_usage_customer_id ON core.customer_usage(customer_id);
CREATE INDEX IF NOT EXISTS idx_usage_month ON core.customer_usage(month);
CREATE INDEX IF NOT EXISTS idx_usage_complaints ON core.customer_usage(complaints);

-- Indexes on churn_labels
CREATE INDEX IF NOT EXISTS idx_churn_status ON core.churn_labels(churn);

-- ============================================
-- TRIGGERS for updated_at timestamps
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON core.customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_churn_labels_updated_at BEFORE UPDATE ON core.churn_labels
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- DATA TRANSFORMATION PROCEDURES
-- ============================================

-- Procedure to load data from staging to core
CREATE OR REPLACE PROCEDURE load_customer_data()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Load customers from staging
    INSERT INTO core.customers (customer_id, age, gender, region, contract_type, monthly_charges, signup_date)
    SELECT customer_id, age, gender, region, contract_type, monthly_charges, signup_date
    FROM staging.customer_info_staging
    ON CONFLICT (customer_id) DO UPDATE SET
        age = EXCLUDED.age,
        gender = EXCLUDED.gender,
        region = EXCLUDED.region,
        contract_type = EXCLUDED.contract_type,
        monthly_charges = EXCLUDED.monthly_charges,
        signup_date = EXCLUDED.signup_date,
        updated_at = CURRENT_TIMESTAMP;

    -- Load usage data from staging
    INSERT INTO core.customer_usage (customer_id, month, call_minutes, data_usage_gb, sms_count, complaints)
    SELECT customer_id, month, call_minutes, data_usage_gb, sms_count, complaints
    FROM staging.usage_data_staging
    ON CONFLICT (unique_customer_month) DO UPDATE SET
        call_minutes = EXCLUDED.call_minutes,
        data_usage_gb = EXCLUDED.data_usage_gb,
        sms_count = EXCLUDED.sms_count,
        complaints = EXCLUDED.complaints;

    -- Load churn labels from staging
    INSERT INTO core.churn_labels (customer_id, churn)
    SELECT customer_id, churn
    FROM staging.churn_labels_staging
    ON CONFLICT (customer_id) DO UPDATE SET
        churn = EXCLUDED.churn,
        updated_at = CURRENT_TIMESTAMP;

    RAISE NOTICE 'Data loaded successfully from staging to core';
END;
$$;

-- Procedure to clear staging tables
CREATE OR REPLACE PROCEDURE clear_staging()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE staging.customer_info_staging;
    TRUNCATE TABLE staging.usage_data_staging;
    TRUNCATE TABLE staging.churn_labels_staging;
    RAISE NOTICE 'Staging tables cleared';
END;
$$;

-- ============================================
-- VALIDATION QUERIES
-- ============================================

-- Check for customers without usage data
-- SELECT c.customer_id FROM core.customers c
-- LEFT JOIN core.customer_usage u ON c.customer_id = u.customer_id
-- WHERE u.customer_id IS NULL;

-- Check for customers without churn labels
-- SELECT c.customer_id FROM core.customers c
-- LEFT JOIN core.churn_labels ch ON c.customer_id = ch.customer_id
-- WHERE ch.customer_id IS NULL;

-- Check data quality
-- SELECT
--     COUNT(*) as total_customers,
--     COUNT(DISTINCT customer_id) as unique_customers,
--     AVG(age) as avg_age,
--     AVG(monthly_charges) as avg_charges
-- FROM core.customers;
