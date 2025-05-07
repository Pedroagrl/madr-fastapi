from madr.models import User

from sqlalchemy import select

def test_create_user(session):
    user = User(
        username='Pedrao',
        email='pedro@gmail.com',
        password='123'
        )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'pedro@gmail.com')
    )

    assert result.username == 'Pedrao'
