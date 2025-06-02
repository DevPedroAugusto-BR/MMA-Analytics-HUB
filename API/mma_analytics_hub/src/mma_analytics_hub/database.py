from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mma_analytics_hub.settings import Settings

settings = Settings()

# Cria o engine para o PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, bind=engine)


# Dependência para injetar a sessão no FastAP
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
