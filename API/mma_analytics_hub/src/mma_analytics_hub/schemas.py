from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from typing import List

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    perfil: Optional[str] = "usuario"
    ativo: Optional[bool] = True

class UserPublic(BaseModel):
    id: int
    username: str 
    email: EmailStr
    perfil: Optional[str] = "usuario"
    ativo: Optional[bool] = True

class UserDB(UserSchema):
    id: int 

# --- Weight Class ---
class WeightClassSchema(BaseModel):
    name: str


class WeightClassDB(WeightClassSchema):
    id: int


# --- Fighter ---
class FighterSchema(BaseModel):
    name: str
    nickname: Optional[str]
    birth_date: Optional[date]
    country: Optional[str]
    location: Optional[str]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    reach_cm: Optional[float]
    stance: Optional[str]
    association: Optional[str]
    weight_class_id: int

    wins: Optional[int]
    losses: Optional[int]
    draws: Optional[int]

    wins_ko: Optional[int]
    wins_submission: Optional[int]
    wins_decision: Optional[int]

    losses_ko: Optional[int]
    losses_submission: Optional[int]
    losses_decision: Optional[int]

    sig_strikes_landed_per_min: Optional[float]
    sig_striking_accuracy: Optional[float]
    sig_strikes_absorbed_per_min: Optional[float]
    sig_strike_defense: Optional[float]

    takedowns_per_15_min: Optional[float]
    takedown_accuracy: Optional[float]
    takedown_defense: Optional[float]
    submissions_per_15_min: Optional[float]


class FighterDB(FighterSchema):
    id: int


class FighterPublic(FighterDB):
    pass


class FighterList(BaseModel):
    fighters: List[FighterPublic]
