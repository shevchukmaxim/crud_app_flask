import pytest
from app import create_app, db
from app.models import User


@pytest.fixture(scope='module')
def test_client():
    config_name = 'testing'
    flask_app = create_app(config_name)
    flask_app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture
def base_url():
    return 'http://127.0.0.1:5055'


@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    user1 = User(name="Frank", surname="Castle")
    user2 = User(name="Jon", surname="Doe")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
