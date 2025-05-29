from sqlalchemy import select 

from dataclasses import asdict

from mma_analytics_hub.models import User, Fighter, WeightClass

def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User({
            "username": "John Doe",
            "email": "johndoe@test.com",
            "password": "123456",
            "perfil": "usuario",
            "ativo": True
        })
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == "John Doe"))

        assert asdict(user) == {
            "username": "John Doe",
            "email": "johndoe@test.com",
            "password": "123456",
            "perfil": "usuario",
            "ativo": True
        }
