from madr.models import User, table_registry
from sqlalchemy.orm import Session

from sqlalchemy import create_engine

def test_create_user():
    engine = create_engine('sqlite:///database.db')

    table_registry.metadata.create_all(engine)

    with Session (engine) as session:

        user = User(username='Pedrao',
                    email='pedro@gmail.com',
                    password='123'
        )

        session.add(user)
        session.commit()
        session.refresh(user)

    assert user.id == 1
