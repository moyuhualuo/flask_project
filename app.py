from flask import Flask, render_template, url_for, jsonify, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from markupsafe import escape
from datetime import datetime
import click
import os
import time

from markupsafe import Markup

"""可以删除的md"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.',)
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, help='The password used to login.')
def admin(username, password):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating new user...')
        user = User(username=username, name='Admin')
        db.session.add(user)
    db.session.commit()
    click.echo('Done.')
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def validate_password(self, password):
        return check_password_hash(self.password, password)
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)
    like_count = db.Column(db.Integer, default=0)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(20), nullable=False)
class Web(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.String(20))
    link_url = db.Column(db.String(255))
    link_name = db.Column(db.String(255))
    description = db.Column(db.Text)
class Md_test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(20))
    author = db.Column(db.String(20))
    content = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login.html'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index_page'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index_page'))  # 确保这里使用正确的端点名称

@app.route('/', methods=['GET', 'POST'])
def index_page():  # put application's code here
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index_page'))
    return render_template('index.html')
@app.route('/life')
def life_page():
    contents = Md_test.query.filter_by(is_published=True).all()
    return render_template('life.html', contents=contents)

"""可以删除的md"""
@app.route('/self_learn', methods=['GET', 'POST'])
def self_learn_page():
    contents = Md_test.query.filter_by(is_published=True).all()
    return render_template('self_learn.html', contents=contents)
@app.route('/commit', methods=['POST', 'GET'])
def commit_page():
    if request.method == 'POST':
        name = request.form.get('name')
        content = request.form.get('message')
        now = datetime.utcnow()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        new_message = Message(name=name, content=content, time=time)
        db.session.add(new_message)
        db.session.commit()
        flash('Message added.')
        return redirect(url_for('commit_page'))

    messages = Message.query.all()
    return render_template('commit.html', messages=messages, get_random_gradient=get_random_gradient)
def get_random_gradient():
    import random
    r1, g1, b1 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    r2, g2, b2 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return f'radial-gradient(circle, rgba({r1},{g1},{b1},1) 0%, rgba({r2},{g2},{b2},1) 100%)'
@app.route('/tools')
def tools_page():
    webs = Web.query.all()
    return render_template('tools.html', webs=webs)
@app.route('/serect')
def serect_page():
    return render_template('serect.html')
@app.route('/like/<int:item_id>', methods=['POST'])
def like(item_id):
    like_record = Like.query.get(item_id)
    if like_record is None:
        like_record = Like(id=item_id, like_count=1)
        db.session.add(like_record)
    else:
        like_record.like_count += 1
    db.session.commit()
    return jsonify({'item_id': item_id, 'like_count': like_record.like_count})
@app.route('/get_like_count/<int:item_id>', methods=['GET'])
def get_like_count(item_id):
    like_record = Like.query.get(item_id)
    like_count = like_record.like_count if like_record else 0
    return jsonify({'item_id': item_id, 'like_count': like_count})
@app.route('/delete/<int:message_id>', methods=['POST', 'GET'])
@login_required
def delete_message(message_id):
    if request.method == 'POST':
        message = Message.query.get_or_404(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            flash('Message deleted.')
        return redirect(url_for('commit_page'))
    return redirect(url_for('commit_page'))
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')


if __name__ == '__main__':
    app.run()
