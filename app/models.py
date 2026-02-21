"""
ImaraFund Database Models
Optimized for 63-column grants CSV and IntelligentMatcher algorithm
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Grant(Base):
    """
    Grant model for ImaraFund's 63-column CSV structure
    Optimized for the 40/30/20/10 scoring algorithm
    """

    __tablename__ = "grants"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Core Identification
    program_id = Column(String(100), unique=True, index=True)
    program_name = Column(String(500), nullable=False, index=True)
    institution_name = Column(String(500), nullable=False, index=True)

    # Geographic Fields (CRITICAL for 40% geography scoring)
    country = Column(String(200), index=True)
    region = Column(String(200), index=True)
    geographic_scope = Column(String(200), index=True)

    # Financial Fields (CRITICAL for 20% funding scoring)
    currency_code = Column(String(10))
    estimated_value_amount = Column(Float)
    minimum_amount = Column(Float)
    maximum_amount = Column(Float)
    repayment_required = Column(Boolean, default=False, index=True)
    interest_rate = Column(String(50))

    # Sector Fields (CRITICAL for 30% sector scoring)
    program_type = Column(String(200))
    target_sectors = Column(Text, index=True)

    # Business Requirements
    duration_months = Column(Integer)
    minimum_employees = Column(Integer)
    maximum_employees = Column(Integer)
    minimum_revenue = Column(Float)
    maximum_revenue = Column(Float)

    # Application Process & Links (✅ data_source_url filled from website_url by cleaning script)
    eligibility_criteria = Column(Text)
    application_process = Column(Text)
    application_deadline = Column(String(200))
    language_requirements = Column(String(200))
    website_url = Column(String(500))
    data_source_url = Column(String(500))  # Fixed by data cleaning script

    # Contact Information
    contact_email = Column(String(200))
    contact_phone = Column(String(100))

    # Demographics and Target Groups
    target_beneficiaries = Column(String(200))
    target_demographics = Column(String(200))
    age_restrictions = Column(String(100))
    gender_focus = Column(String(50))

    # Focus Areas (Boolean flags - cleaned from CSV)
    environmental_focus = Column(Boolean, default=False)
    innovation_focus = Column(Boolean, default=False)
    digital_focus = Column(Boolean, default=False)
    export_focus = Column(Boolean, default=False)
    women_focused = Column(Boolean, default=False, index=True)
    youth_focused = Column(Boolean, default=False, index=True)
    agriculture_focused = Column(Boolean, default=False, index=True)
    green_climate_focused = Column(Boolean, default=False)

    # Support Services
    technical_assistance = Column(Boolean, default=False)
    mentorship_available = Column(Boolean, default=False)
    networking_opportunities = Column(Boolean, default=False)
    training_provided = Column(Boolean, default=False)
    co_financing_required = Column(Boolean, default=False)
    co_financing_available = Column(Boolean, default=False)
    export_support = Column(Boolean, default=False)
    technology_innovation = Column(Boolean, default=False)
    digital_application = Column(Boolean, default=False)

    # Financial Terms
    collateral_required = Column(String(50))
    grace_period_months = Column(Integer)
    guarantee_coverage = Column(String(50))

    # Program Metrics and History
    success_rate = Column(Float)
    total_beneficiaries = Column(Integer)
    year_established = Column(Integer)
    funding_source = Column(String(500))
    program_start_date = Column(String(100))

    # Status and Verification
    verified = Column(Boolean, default=False, index=True)
    last_verified_date = Column(String(50))
    last_updated = Column(String(50))
    verification_date = Column(String(50))
    special_features = Column(Text)
    notes = Column(Text)

    # Flexible storage for additional CSV columns
    additional_data = Column(JSON)

    # System timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Grant(id={self.id}, name='{self.program_name}')>"


class Company(Base):
    """
    Company model matching your synthetic companies dataset structure
    Optimized for IntelligentMatcher algorithm
    """

    __tablename__ = "companies"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Core Identification
    company_id = Column(String(100), unique=True, index=True)
    company_name = Column(String(500), nullable=False, index=True)

    # Business Classification (CRITICAL for matching)
    sector = Column(String(200), nullable=False, index=True)
    business_stage = Column(String(100), nullable=False, index=True)
    innovation_level = Column(String(50))

    # Geographic Information (CRITICAL for 40% geography scoring)
    nationality = Column(String(100), nullable=False, index=True)
    business_registered_in = Column(String(100))

    # Founder Demographics
    founder_age = Column(Integer)
    founder_gender = Column(String(20))

    # Business Metrics
    business_age_months = Column(Integer)
    annual_revenue_usd = Column(Float)
    employees = Column(Integer)

    # Funding Requirements (CRITICAL for 20% funding scoring)
    funding_need_usd = Column(Float, nullable=False, index=True)
    has_prototype = Column(Boolean, default=False)
    targets_underserved = Column(Boolean, default=False)

    # System timestamps
    created_date = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.company_name}')>"