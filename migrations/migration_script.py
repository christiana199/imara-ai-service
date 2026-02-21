"""
ImaraFund Data Migration Script
Import your cleaned CSV data into the database
"""

import pandas as pd
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal, init_db
from app.models import Grant, Company


class ImaraFundMigrator:
    """Data migration utility for ImaraFund cleaned datasets"""

    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def safe_float(self, value: Any) -> Optional[float]:
        """Safely convert value to float"""
        if pd.isna(value) or value == "" or value is None:
            return None
        try:
            if isinstance(value, str):
                cleaned = value.replace("$", "").replace(",", "").strip()
                return float(cleaned) if cleaned else None
            return float(value)
        except (ValueError, TypeError):
            return None

    def safe_int(self, value: Any) -> Optional[int]:
        """Safely convert value to integer"""
        if pd.isna(value) or value == "" or value is None:
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def safe_bool(self, value: Any) -> bool:
        """Safely convert value to boolean"""
        if pd.isna(value) or value == "" or value is None:
            return False
        if isinstance(value, bool):
            return value
        str_val = str(value).lower().strip()
        return str_val in ["true", "yes", "1", "y", "on", "t"]

    def safe_string(self, value: Any, max_length: Optional[int] = None) -> Optional[str]:
        """Safely convert value to string"""
        if pd.isna(value) or value is None:
            return None
        result = str(value).strip()
        if not result or result.lower() in ['nan', 'null', 'none']:
            return None
        if max_length and len(result) > max_length:
            result = result[:max_length-3] + "..."
        return result

    def import_cleaned_grants(self, csv_path: str = "data/cleaned/grants_cleaned_latest.csv") -> Dict[str, int]:
        """Import the cleaned grants CSV (with fixed data_source_url)"""
        print(f"📊 Importing grants from: {csv_path}")

        csv_file = Path(csv_path)
        if not csv_file.exists():
            raise FileNotFoundError(f"Cleaned grants CSV not found: {csv_path}")

        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"✅ Loaded {len(df)} grants")

        imported_count = 0
        error_count = 0

        for idx, row in df.iterrows():
            try:
                grant = Grant(
                    program_id=self.safe_string(row.get('program_id'), 100) or f"GRANT_{idx+1}",
                    program_name=self.safe_string(row.get('program_name'), 500) or f"Program {idx+1}",
                    institution_name=self.safe_string(row.get('institution_name'), 500) or "Unknown",
                    country=self.safe_string(row.get('country'), 200),
                    region=self.safe_string(row.get('region'), 200),
                    geographic_scope=self.safe_string(row.get('geographic_scope'), 200),
                    currency_code=self.safe_string(row.get('currency_code'), 10),
                    estimated_value_amount=self.safe_float(row.get('estimated_value_amount')),
                    minimum_amount=self.safe_float(row.get('minimum_amount')),
                    maximum_amount=self.safe_float(row.get('maximum_amount')),
                    repayment_required=self.safe_bool(row.get('repayment_required')),
                    interest_rate=self.safe_string(row.get('interest_rate'), 50),
                    program_type=self.safe_string(row.get('program_type'), 200),
                    target_sectors=self.safe_string(row.get('target_sectors')),
                    duration_months=self.safe_int(row.get('duration_months')),
                    minimum_employees=self.safe_int(row.get('minimum_employees')),
                    maximum_employees=self.safe_int(row.get('maximum_employees')),
                    minimum_revenue=self.safe_float(row.get('minimum_revenue')),
                    maximum_revenue=self.safe_float(row.get('maximum_revenue')),
                    eligibility_criteria=self.safe_string(row.get('eligibility_criteria')),
                    application_process=self.safe_string(row.get('application_process')),
                    application_deadline=self.safe_string(row.get('application_deadline'), 200),
                    language_requirements=self.safe_string(row.get('language_requirements'), 200),
                    website_url=self.safe_string(row.get('website_url'), 500),
                    data_source_url=self.safe_string(row.get('data_source_url'), 500),  # ✅ Fixed by cleaning
                    contact_email=self.safe_string(row.get('contact_email'), 200),
                    contact_phone=self.safe_string(row.get('contact_phone'), 100),
                    target_beneficiaries=self.safe_string(row.get('target_beneficiaries'), 200),
                    target_demographics=self.safe_string(row.get('target_demographics'), 200),
                    age_restrictions=self.safe_string(row.get('age_restrictions'), 100),
                    gender_focus=self.safe_string(row.get('gender_focus'), 50),
                    environmental_focus=self.safe_bool(row.get('environmental_focus')),
                    innovation_focus=self.safe_bool(row.get('innovation_focus')),
                    digital_focus=self.safe_bool(row.get('digital_focus')),
                    export_focus=self.safe_bool(row.get('export_focus')),
                    women_focused=self.safe_bool(row.get('women_focused')),
                    youth_focused=self.safe_bool(row.get('youth_focused')),
                    agriculture_focused=self.safe_bool(row.get('agriculture_focused')),
                    green_climate_focused=self.safe_bool(row.get('green_climate_focused')),
                    technical_assistance=self.safe_bool(row.get('technical_assistance')),
                    mentorship_available=self.safe_bool(row.get('mentorship_available')),
                    networking_opportunities=self.safe_bool(row.get('networking_opportunities')),
                    training_provided=self.safe_bool(row.get('training_provided')),
                    co_financing_required=self.safe_bool(row.get('co_financing_required')),
                    co_financing_available=self.safe_bool(row.get('co_financing_available')),
                    export_support=self.safe_bool(row.get('export_support')),
                    technology_innovation=self.safe_bool(row.get('technology_innovation')),
                    digital_application=self.safe_bool(row.get('digital_application')),
                    collateral_required=self.safe_string(row.get('collateral_required'), 50),
                    grace_period_months=self.safe_int(row.get('grace_period_months')),
                    guarantee_coverage=self.safe_string(row.get('guarantee_coverage'), 50),
                    success_rate=self.safe_float(row.get('success_rate')),
                    total_beneficiaries=self.safe_int(row.get('total_beneficiaries')),
                    year_established=self.safe_int(row.get('year_established')),
                    funding_source=self.safe_string(row.get('funding_source'), 500),
                    program_start_date=self.safe_string(row.get('program_start_date'), 100),
                    verified=self.safe_bool(row.get('verified')),
                    last_verified_date=self.safe_string(row.get('last_verified_date'), 50),
                    last_updated=self.safe_string(row.get('last_updated'), 50),
                    verification_date=self.safe_string(row.get('verification_date'), 50),
                    special_features=self.safe_string(row.get('special_features')),
                    notes=self.safe_string(row.get('notes'))
                )

                self.db.add(grant)
                imported_count += 1

                if imported_count % 20 == 0:
                    self.db.commit()
                    print(f"  ✓ Imported {imported_count} grants...")

            except Exception as e:
                error_count += 1
                print(f"  ✗ Error on row {idx + 2}: {str(e)}")
                continue

        self.db.commit()
        print(f"\n✅ Grants import completed!")

        return {"imported": imported_count, "errors": error_count, "total_rows": len(df)}

    def import_companies(self, csv_path: str = "data/companies/synthetic_companies.csv") -> Dict[str, int]:
        """Import companies CSV"""
        print(f"\n📊 Importing companies from: {csv_path}")

        csv_file = Path(csv_path)
        if not csv_file.exists():
            print(f"  ⚠ Companies CSV not found: {csv_path}")
            return {"imported": 0, "errors": 0, "total_rows": 0}

        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"✅ Loaded {len(df)} companies")

        imported_count = 0
        for idx, row in df.iterrows():
            try:
                company = Company(
                    company_id=self.safe_string(row.get('company_id'), 100) or f"COMP_{idx+1}",
                    company_name=self.safe_string(row.get('company_name'), 500) or f"Company {idx+1}",
                    sector=self.safe_string(row.get('sector'), 200) or "General",
                    nationality=self.safe_string(row.get('nationality'), 100) or "Unknown",
                    business_registered_in=self.safe_string(row.get('business_registered_in'), 100),
                    business_stage=self.safe_string(row.get('business_stage'), 100) or "Unknown",
                    innovation_level=self.safe_string(row.get('innovation_level'), 50),
                    founder_age=self.safe_int(row.get('founder_age')),
                    founder_gender=self.safe_string(row.get('founder_gender'), 20),
                    business_age_months=self.safe_int(row.get('business_age_months')),
                    annual_revenue_usd=self.safe_float(row.get('annual_revenue_usd')),
                    employees=self.safe_int(row.get('employees')),
                    funding_need_usd=self.safe_float(row.get('funding_need_usd')) or 0.0,
                    has_prototype=self.safe_bool(row.get('has_prototype')),
                    targets_underserved=self.safe_bool(row.get('targets_underserved')),
                    created_date=self.safe_string(row.get('created_date'), 50)
                )

                self.db.add(company)
                imported_count += 1

                if imported_count % 10 == 0:
                    self.db.commit()
                    print(f"  ✓ Imported {imported_count} companies...")

            except Exception as e:
                print(f"  ✗ Error on row {idx + 2}: {str(e)}")
                continue

        self.db.commit()
        print(f"\n✅ Companies import completed!")

        return {"imported": imported_count, "errors": 0, "total_rows": len(df)}


def main():
    """Interactive migration"""
    print("=" * 70)
    print("🚀 ImaraFund Data Migration")
    print("=" * 70)

    print("\n📦 Initializing database...")
    init_db()

    with ImaraFundMigrator() as migrator:
        print("\n" + "=" * 70)
        print("IMPORTING GRANTS")
        print("=" * 70)

        try:
            results = migrator.import_cleaned_grants()
            print(f"\n✅ Grants: {results['imported']}/{results['total_rows']}")
        except Exception as e:
            print(f"✗ Grant import failed: {str(e)}")

        print("\n" + "=" * 70)
        print("IMPORTING COMPANIES")
        print("=" * 70)

        try:
            results = migrator.import_companies()
            print(f"\n✅ Companies: {results['imported']}/{results['total_rows']}")
        except Exception as e:
            print(f"✗ Company import failed: {str(e)}")

    print("\n" + "=" * 70)
    print("✅ Migration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()