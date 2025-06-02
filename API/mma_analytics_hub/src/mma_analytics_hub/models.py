# api/models/models.py
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    perfil: Mapped[str] = mapped_column(default="usuario")  # usuario | analista | matchmaker
    ativo: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class WeightClass:
    __tablename__ = "weight_classes"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


@table_registry.mapped_as_dataclass
class Fighter:
    __tablename__ = "fighters"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    nickname: Mapped[str | None]
    birth_date: Mapped[datetime | None]
    country: Mapped[str | None]
    location: Mapped[str | None]
    height_cm: Mapped[float | None]
    weight_kg: Mapped[float | None]
    reach_cm: Mapped[float | None]
    stance: Mapped[str | None]
    association: Mapped[str | None]

    weight_class_id: Mapped[int] = mapped_column(ForeignKey("weight_classes.id"))

    wins: Mapped[int | None]
    losses: Mapped[int | None]
    draws: Mapped[int | None]

    wins_ko: Mapped[int | None]
    wins_submission: Mapped[int | None]
    wins_decision: Mapped[int | None]

    losses_ko: Mapped[int | None]
    losses_submission: Mapped[int | None]
    losses_decision: Mapped[int | None]

    sig_strikes_landed_per_min: Mapped[float | None]
    sig_striking_accuracy: Mapped[float | None]
    sig_strikes_absorbed_per_min: Mapped[float | None]
    sig_strike_defense: Mapped[float | None]

    takedowns_per_15_min: Mapped[float | None]
    takedown_accuracy: Mapped[float | None]
    takedown_defense: Mapped[float | None]
    submissions_per_15_min: Mapped[float | None]
