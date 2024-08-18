import pytest
from app import create_app, db
from app.models import Md_test, User, Message, Like

@pytest.fixture
def app():
    app = create_app('testing')  # 使用测试配置
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    db.create_all()
    yield db
    db.drop_all()

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data  # 根据你的主页内容调整

def test_login(client, init_db):
    response = client.post('/login', data={'username': 'admin', 'password': 'password'})
    assert response.status_code == 302  # 重定向到主页
    assert b'Login success' in response.data

def test_edit_life(client, init_db):
    # 添加测试数据
    new_content = Md_test(page='life', author='Test Author', content='Test Content', is_published=True)
    db.session.add(new_content)
    db.session.commit()

    response = client.post('/life/edit/1', data={
        'author': 'Updated Author',
        'content': 'Updated Content',
        'is_published': 'on'
    })
    assert response.status_code == 302  # 重定向
    updated_content = Md_test.query.get(1)
    assert updated_content.author == 'Updated Author'
    assert updated_content.content == 'Updated Content'

def test_add_life(client, init_db):
    response = client.post('/life/add', data={
        'author': 'New Author',
        'content': 'New Content',
        'is_published': 'on'
    })
    assert response.status_code == 302  # 重定向
    new_content = Md_test.query.filter_by(author='New Author').first()
    assert new_content is not None
    assert new_content.content == 'New Content'

def test_delete_life(client, init_db):
    # 添加测试数据
    new_content = Md_test(page='life', author='Delete Test', content='Content to delete', is_published=True)
    db.session.add(new_content)
    db.session.commit()

    response = client.post('/life/delete/1')  # 使用适当的 ID
    assert response.status_code == 302  # 重定向状态码
    assert Md_test.query.filter_by(author='Delete Test').first() is None  # 确保数据被删除

def test_commit_page(client, init_db):
    response = client.post('/commit', data={
        'name': 'Test User',
        'message': 'Test message'
    })
    assert response.status_code == 302  # 重定向
    new_message = Message.query.filter_by(name='Test User').first()
    assert new_message is not None
    assert new_message.content == 'Test message'
