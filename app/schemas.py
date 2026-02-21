"""
ImaraFund Pydantic Schemas
Request/Response models for API validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Grant Schemas
class GrantBase(BaseModel):
    """Base grant schema with essential fields"""
    program_name: str = Field(..., min_length=1, max_length=500)
    institution_name: str
    country: Optional[str] = None
    target_sectors: Optional[str] = None
    estimated_value_amount: Optional[float] = None


class GrantResponse(GrantBase):
    """Schema for grant API responses"""
    id: int
    program_id: Optional[str]
    region: Optional[str]
    geographic_scope: Optional[str]
    repayment_required: bool
    program_type: Optional[str]
    website_url: Optional[str]
    data_source_url: Optional[str]  # ✅ Fixed by data cleaning
    women_focused: bool
    youth_focused: bool
    agriculture_focused: bool
    verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Company Schemas
class CompanyBase(BaseModel):
    """Base company schema"""
    company_name: str = Field(..., min_length=1, max_length=500)
    sector: str = Field(..., min_length=1, max_length=200)
    nationality: str = Field(..., min_length=2, max_length=100)
    business_stage: str = Field(..., min_length=1, max_length=100)
    funding_need_usd: float = Field(..., gt=0)


class CompanyCreate(CompanyBase):
    """Schema for creating a new company"""
    company_id: Optional[str] = None
    business_registered_in: Optional[str] = None
    founder_age: Optional[int] = Field(None, ge=18, le=100)
    founder_gender: Optional[str] = None
    business_age_months: Optional[int] = Field(None, ge=0)
    annual_revenue_usd: Optional[float] = Field(None, ge=0)
    employees: Optional[int] = Field(None, ge=0)
    innovation_level: Optional[str] = None
    has_prototype: bool = False
    targets_underserved: bool = False


class CompanyResponse(CompanyBase):
    """Schema for company API responses"""
    id: int
    company_id: Optional[str]
    founder_age: Optional[int]
    business_age_months: Optional[int]
    annual_revenue_usd: Optional[float]
    employees: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# Matching Schemas (Your IntelligentMatcher scoring breakdown)
class ScoreBreakdown(BaseModel):
    """Your exact IntelligentMatcher scoring breakdown (40/30/20/10)"""
    geographic: float = Field(..., ge=0, le=40, description="Geography match (0-40 points)")
    sector: float = Field(..., ge=0, le=30, description="Sector alignment (0-30 points)")
    amount_fit: float = Field(..., ge=0, le=20, description="Funding amount fit (0-20 points)")
    stage: float = Field(..., ge=0, le=10, description="Business stage (0-10 points)")


class MatchResult(BaseModel):
    """Individual match result with grant details and scoring"""
    program_name: str
    institution: str
    country: str
    funding_amount: float
    match_score: float = Field(..., ge=0, le=100)
    score_breakdown: ScoreBreakdown
    target_sectors: str
    website: str
    data_source_url: str  # ✅ Fixed by data cleaning
    repayment_required: str
    grant_details: GrantResponse


class MatchResponse(BaseModel):
    """Complete matching response with AI recommendation"""
    company: CompanyResponse
    matches: List[MatchResult]
    ai_recommendation: Optional[str] = None
    total_matches_found: int
    algorithm_version: str = "ImaraFund v1.0 (40/30/20/10)"