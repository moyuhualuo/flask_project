import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app('testing')  # 使用测试配置
    with app.app_context():
        yield app

@pytest.fixture
def init_db(app):
    db.create_all()
    yield db
    db.drop_all()

def test_user_creation(init_db):
    user = User(username='testuser', name='Test User')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    fetched_user = User.query.filter_by(username='testuser').first()
    assert fetched_user is not None
    assert fetched_user.name == 'Test User'
    assert fetched_user.validate_password('password')

def test_message_creation(init_db):
    message = Message(name='Test User', content='Test message', time='2024-08-17 00:00:00')
    db.session.add(message)
    db.session.commit()

    fetched_message = Message.query.filter_by(name='Test User').first()
    assert fetched_message is not None
    assert fetched_message.content == 'Test message'
    assert fetched_message.time == '2024-08-17 00:00:00'
