from fastapi import Depends, FastAPI, HTTPException
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session

#from .Analysis.etl import load_fighters_data
from mma_analytics_hub.settings import Settings
from mma_analytics_hub.database import get_session
from mma_analytics_hub.schemas import (
    UserDB,
    UserPublic,
    UserSchema,
    WeightClassDB,
    WeightClassSchema,
    FighterDB,
    FighterSchema,
    Message,
    FighterPublic,
    FighterList,
)

from mma_analytics_hub.models import User, WeightClass, Fighter


app = FastAPI()

@app.get("/fighters/names")
def get_all_fighter_names(db: Session = Depends(get_session)):
    fighters = db.query(Fighter.name).order_by(Fighter.name).all()
    names = [name for (name,) in fighters]
    return {"fighters": names}


@app.get("/fighters/{name}")
def get_fighter_by_name(name: str, db: Session = Depends(get_session)):
    fighter = db.query(Fighter).filter(Fighter.name.ilike(name)).first()
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return fighter


@app.get("/weight_classes")
def get_weight_classes(db: Session = Depends(get_session)):
    categories = db.query(WeightClass.name).order_by(WeightClass.name).all()
    return {"weight_classes": [name for (name,) in categories]}


@app.get("/weight_classes/{category}/fighters")
def get_fighters_by_category(category: str, db: Session = Depends(get_session)):
    weight_class = db.query(WeightClass).filter(WeightClass.name.ilike(category)).first()
    if not weight_class:
        raise HTTPException(status_code=404, detail="Weight class not found")

    fighters = db.query(Fighter).filter(Fighter.weight_class_id == weight_class.id).order_by(Fighter.name).all()
    return fighters


@app.get("/fighters")
def get_all_fighters(db: Session = Depends(get_session)):
    fighters = db.query(Fighter).order_by(Fighter.name).all()
    return fighters



#Métodos de PUT
from mma_analytics_hub.schemas import FighterSchema

@app.put("/update_fighter/{fighter_id}")
def update_fighter(fighter_id: int, fighter_data: FighterSchema, db: Session = Depends(get_session)):
    fighter = db.query(Fighter).filter(Fighter.id == fighter_id).first()
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")

    for key, value in fighter_data.model_dump().items():
        setattr(fighter, key, value)

    db.commit()
    db.refresh(fighter)
    return fighter


@app.get("/import_fighters")
def import_fighters(db: Session = Depends(get_session)):
    df_final = load_fighters_data()
    count = 0

    for _, row in df_final.iterrows():
        name = row["name"]
        if not name:
            continue

        # Verificar se já existe
        existing = db.query(Fighter).filter(Fighter.name == name).first()
        if existing:
            continue

        # Gerenciar categoria de peso
        weight_class_name = row.get("weight_class")
        if weight_class_name:
            weight_class = db.query(WeightClass).filter(WeightClass.name == weight_class_name).first()
            if not weight_class:
                weight_class = WeightClass(name=weight_class_name)
                db.add(weight_class)
                db.commit()
                db.refresh(weight_class)
        else:
            weight_class = None

        fighter = Fighter(
            name=name,
            nickname=row.get("nickname"),
            birth_date=row.get("birth_date"),
            country=row.get("country"),
            location=row.get("location"),
            height_cm=row.get("height_cm"),
            weight_kg=row.get("weight_kg"),
            reach_cm=row.get("reach_cm"),
            stance=row.get("stance"),
            association=row.get("association"),
            weight_class_id=weight_class.id if weight_class else None,
            wins=row.get("wins"),
            losses=row.get("losses"),
            draws=row.get("draws"),
            wins_ko=row.get("wins_ko"),
            wins_submission=row.get("wins_submission"),
            wins_decision=row.get("wins_decision"),
            losses_ko=row.get("losses_ko"),
            losses_submission=row.get("losses_submission"),
            losses_decision=row.get("losses_decision"),
            sig_strikes_landed_per_min=row.get("sig_strikes_landed_per_min"),
            sig_striking_accuracy=row.get("sig_striking_accuracy"),
            sig_strikes_absorbed_per_min=row.get("sig_strikes_absorbed_per_min"),
            sig_strike_defense=row.get("sig_strike_defense"),
            takedowns_per_15_min=row.get("takedowns_per_15_min"),
            takedown_accuracy=row.get("takedown_accuracy"),
            takedown_defense=row.get("takedown_defense"),
            submissions_per_15_min=row.get("submissions_per_15_min"),
        )

        db.add(fighter)
        count += 1

    db.commit()
    return {"message": f"{count} fighters imported successfully."}
