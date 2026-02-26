"""
ImaraFund API Endpoints
RESTful API for grant matching with comprehensive filtering
"""
from app.schemas import GrantResponse, GrantCreate
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Grant, Company
from app.schemas import GrantCreate
from app.schemas import (
    GrantResponse, CompanyResponse, CompanyCreate, MatchResponse,
    ScoreBreakdown, MatchResult
)
from app.services.intelligent_matcher import IntelligentMatcher
from app.services.gemini_service import GeminiService

router = APIRouter()


@router.get("/grants", response_model=List[GrantResponse])
def list_grants(
    sector: Optional[str] = Query(None, description="Filter by target sector"),
    country: Optional[str] = Query(None, description="Filter by country"),
    repayment_required: Optional[bool] = Query(None, description="Filter by repayment requirement"),
    min_amount: Optional[float] = Query(None, description="Minimum grant amount"),
    max_amount: Optional[float] = Query(None, description="Maximum grant amount"),
    women_focused: Optional[bool] = Query(None, description="Filter women-focused programs"),
    youth_focused: Optional[bool] = Query(None, description="Filter youth-focused programs"),
    agriculture_focused: Optional[bool] = Query(None, description="Filter agriculture-focused programs"),
    verified: Optional[bool] = Query(None, description="Filter verified programs only"),
    skip: int = Query(0, ge=0, description="Records to skip for pagination"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    db: Session = Depends(get_db)
):
    """List grants with comprehensive filtering based on your CSV structure"""
    query = db.query(Grant)

    # Apply filters
    if sector:
        query = query.filter(Grant.target_sectors.ilike(f"%{sector}%"))
    if country:
        query = query.filter(
            (Grant.country.ilike(f"%{country}%")) |
            (Grant.geographic_scope.ilike(f"%{country}%"))
        )
    if repayment_required is not None:
        query = query.filter(Grant.repayment_required == repayment_required)
    if min_amount is not None:
        query = query.filter(Grant.estimated_value_amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Grant.estimated_value_amount <= max_amount)
    if women_focused is not None:
        query = query.filter(Grant.women_focused == women_focused)
    if youth_focused is not None:
        query = query.filter(Grant.youth_focused == youth_focused)
    if agriculture_focused is not None:
        query = query.filter(Grant.agriculture_focused == agriculture_focused)
    if verified is not None:
        query = query.filter(Grant.verified == verified)

    grants = query.offset(skip).limit(limit).all()
    return grants


@router.get("/grants/{grant_id}", response_model=GrantResponse)
def get_grant(grant_id: int, db: Session = Depends(get_db)):
    """Get detailed grant information"""
    grant = db.query(Grant).filter(Grant.id == grant_id).first()
    if not grant:
        raise HTTPException(status_code=404, detail=f"Grant {grant_id} not found")
    return grant


@router.get("/companies", response_model=List[CompanyResponse])
def list_companies(
    sector: Optional[str] = Query(None),
    nationality: Optional[str] = Query(None),
    business_stage: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List companies with filtering"""
    query = db.query(Company)

    if sector:
        query = query.filter(Company.sector.ilike(f"%{sector}%"))
    if nationality:
        query = query.filter(Company.nationality.ilike(f"%{nationality}%"))
    if business_stage:
        query = query.filter(Company.business_stage.ilike(f"%{business_stage}%"))

    companies = query.offset(skip).limit(limit).all()
    return companies


@router.post("/companies", response_model=CompanyResponse, status_code=201)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Register a new company in ImaraFund"""
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.post("/match/{company_id}", response_model=MatchResponse)
def match_company_with_grants(
    company_id: int,
    top_n: int = Query(5, ge=1, le=20, description="Number of top matches"),
    db: Session = Depends(get_db)
):
    """
    Run ImaraFund's intelligent matching algorithm with AI recommendations
    Uses your proven 40/30/20/10 scoring system
    """
    matcher = IntelligentMatcher(db)
    ai_service = GeminiService()

    try:
        company, matches = matcher.find_matches(company_id, top_n=top_n)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching error: {str(e)}")

    if not matches:
        return MatchResponse(
            company=CompanyResponse.from_orm(company),
            matches=[],
            ai_recommendation="No suitable matches found with score > 30.",
            total_matches_found=0
        )

    # Process matches for API response
    match_results = []
    for match in matches:
        breakdown = match['score_breakdown']

        match_result = MatchResult(
            program_name=match['program_name'],
            institution=match['institution'],
            country=match['country'],
            funding_amount=match['funding_amount'],
            match_score=match['match_score'],
            score_breakdown=ScoreBreakdown(
                geographic=breakdown['geographic'],
                sector=breakdown['sector'],
                amount_fit=breakdown['amount_fit'],
                stage=breakdown['stage']
            ),
            target_sectors=match['target_sectors'],
            website=match['website'],
            data_source_url=match['data_source_url'],
            repayment_required=match['repayment_required'],
            grant_details=GrantResponse.from_orm(match['grant'])
        )
        match_results.append(match_result)

    # Generate AI recommendation for top match
    company_profile = matcher.get_company_profile_dict(company)
    ai_recommendation = ai_service.get_ai_recommendation(company_profile, matches[0])

    return MatchResponse(
        company=CompanyResponse.from_orm(company),
        matches=match_results,
        ai_recommendation=ai_recommendation,
        total_matches_found=len(matches)
    )
@router.get("/grants/{grant_id}", response_model=GrantResponse)
def get_grant(grant_id: int, db: Session = Depends(get_db)):
    grant = db.query(Grant).filter(Grant.id == grant_id).first()
    if not grant:
        raise HTTPException(status_code=404, detail=f"Grant {grant_id} not found")
    return grant


# 👇 PASTE IT RIGHT HERE 👇
@router.post("/grants", response_model=GrantResponse, status_code=201)
def create_grant(grant: GrantResponse, db: Session = Depends(get_db)):
    """
    Create a new grant manually (for seeding production)
    """
    db_grant = Grant(**grant.dict())
    db.add(db_grant)
    db.commit()
    db.refresh(db_grant)
    return db_grant

@router.post("/grants", response_model=GrantResponse, status_code=201)
def create_grant(grant: GrantCreate, db: Session = Depends(get_db)):
    db_grant = Grant(**grant.dict())
    db.add(db_grant)
    db.commit()
    db.refresh(db_grant)
    return db_grant