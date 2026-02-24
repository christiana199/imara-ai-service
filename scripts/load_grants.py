import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Grant

CSV_PATH = "data/cleaned/grants_cleaned_latest.csv"  # adjust filename if needed

def load_grants():
    db: Session = SessionLocal()

    df = pd.read_csv(CSV_PATH)

    for _, row in df.iterrows():
        grant = Grant(
            program_id=row.get("program_id"),
            program_name=row.get("program_name"),
            institution_name=row.get("institution_name"),
            country=row.get("country"),
            region=row.get("region"),
            geographic_scope=row.get("geographic_scope"),
            target_sectors=row.get("target_sectors"),
            estimated_value_amount=row.get("estimated_value_amount"),
            repayment_required=row.get("repayment_required"),
            website_url=row.get("website_url"),
            data_source_url=row.get("data_source_url"),
            women_focused=row.get("women_focused"),
            youth_focused=row.get("youth_focused"),
            agriculture_focused=row.get("agriculture_focused"),
            verified=row.get("verified")
        )

        db.add(grant)

    db.commit()
    db.close()

    print("✅ Grants loaded successfully!")

if __name__ == "__main__":
    load_grants()