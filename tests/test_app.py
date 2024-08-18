import pytest
from app import create_app, db
from app import User, Md_test, Message, Like


@pytest.fixture
def app():
    app = create_app(config_name='testing')
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


def test_login(client, init_db):
    # 创建测试用户
    user = User(username='testuser', name='Test User')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    # 测试登录功能
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # 重定向状态码
    assert b'Login success.' in response.data


def test_add_life(client, init_db):
    # 登录用户
    user = User(username='testuser', name='Test User')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    # 模拟登录
    with client.session_transaction() as sess:
        sess['user_id'] = user.id

    # 测试添加内容
    response = client.post('/life/add', data={
        'author': 'Test Author',
        'content': 'Test Content'
    })
    assert response.status_code == 404 # 重定向状态码
    assert Md_test.query.count() == 1  # 确保数据库中有一个记录


def test_edit_life(client, init_db):
    # 创建测试内容
    md_test = Md_test(author='Old Author', content='Old Content', page='life', is_published=True)
    db.session.add(md_test)
    db.session.commit()

    # 登录用户
    user = User(username='testuser', name='Test User')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    # 模拟登录
    with client.session_transaction() as sess:
        sess['user_id'] = user.id

    # 测试编辑内容
    response = client.post(f'/life/edit/{md_test.id}', data={
        'author': 'New Author',
        'content': 'New Content'
    })
    assert response.status_code == 302  # 重定向状态码
    updated_md_test = Md_test.query.get(md_test.id)
    assert updated_md_test.author == 'New Author'
    assert updated_md_test.content == 'New Content'


def test_delete_life(client, init_db):
    # 创建测试内容
    md_test = Md_test(author='Test Author', content='Test Content', page='life', is_published=True)
    db.session.add(md_test)
    db.session.commit()

    # 登录用户
    user = User(username='testuser', name='Test User')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    # 模拟登录
    with client.session_transaction() as sess:
        sess['user_id'] = user.id

    # 测试删除内容
    response = client.post(f'/life/delete/{md_test.id}')
    assert response.status_code == 302  # 重定向状态码
    assert Md_test.query.count() == 0  # 确保数据库中没有记录
