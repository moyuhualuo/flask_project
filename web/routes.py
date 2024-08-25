from flask import Blueprint, render_template, url_for, jsonify, request, redirect, flash
from .models import User, Like, Message, Web, Md_test
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from .functions import get_random_gradient
from . import db

bp = Blueprint("web", __name__)


@bp.context_processor
def inject_user():  # 函数名可以随意修改
    user = current_user
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('web.login'))
        user = User.query.filter_by(username=username).first()

        # 验证用户名和密码是否一致
        if user and username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('web.index_page'))  # 重定向到主页
        else:
            flash('Invalid username or password.')  # 如果验证失败，显示错误消息
            return redirect(url_for('web.login'))  # 重定向回登录页面

    return render_template('login.html')


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')

    return redirect(url_for('web.index_page'))  # 确保这里使用正确的端点名称


@bp.route('/', methods=['GET', 'POST'])
def index_page():  # put application's code here
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('web.index_page'))
    return render_template('index.html')


@bp.route('/life', methods=['GET', 'POST'])
def life_page():
    contents = Md_test.query.filter_by(is_published=True, page='life').all()
    return render_template('life.html', contents=contents)


@bp.route('/life/delete/<int:id>', methods=['POST'])
@login_required
def delete_life(id):
    md_test = Md_test.query.get_or_404(id)
    db.session.delete(md_test)
    db.session.commit()
    flash('Successfully deleted.')
    return redirect(url_for('web.life_page'))


@bp.route('/life/edit/<int:id>', methods=['POST'])
@login_required
def edit_life(id):
    md_test = Md_test.query.get(id)
    md_test.author = request.form.get('author')
    md_test.content = request.form.get('content')
    md_test.is_published = True
    db.session.commit()
    flash('Successfully edited.')
    return redirect(url_for('web.life_page'))


@bp.route('/life/add', methods=['POST'])
@login_required
def add_life():
    if request.method == 'POST':
        author = request.form.get('author')
        content = request.form.get('content')
        is_published = True
        new_record = Md_test(page='life', author=author, content=content, is_published=is_published)
        db.session.add(new_record)
        db.session.commit()
        flash('Successfully added.')
        return redirect(url_for('web.life_page'))


@bp.route('/self_learn', methods=['GET', 'POST'])
def self_learn_page():
    contents = Md_test.query.filter_by(page='learn', is_published=True).all()
    return render_template('self_learn.html', contents=contents)


@bp.route('/self_learn/delete/<int:id>', methods=['POST'])
@login_required
def delete_self_learn(id):
    md_test = Md_test.query.get_or_404(id)
    db.session.delete(md_test)
    db.session.commit()
    flash('Successfully deleted.')
    return redirect(url_for('web.self_learn_page'))


@bp.route('/self_learn/edit/<int:id>', methods=['POST'])
@login_required
def edit_self_learn(id):
    md_test = Md_test.query.get_or_404(id)
    md_test.author = request.form.get('author')
    md_test.content = request.form.get('content')
    md_test.is_published = True
    db.session.commit()
    flash('Successfully edited.')
    return redirect(url_for('web.self_learn_page'))


@bp.route('/self_learn/add', methods=['POST'])
@login_required
def add_self_learn():
    if request.method == 'POST':
        author = request.form.get('author')
        content = request.form.get('content')
        is_published = True
        new_record = Md_test(page='learn', author=author, content=content, is_published=is_published)
        db.session.add(new_record)
        db.session.commit()
        flash('Successfully added.')

        return redirect(url_for('web.self_learn_page'))


@bp.route('/commit', methods=['POST', 'GET'])
def commit_page():
    if request.method == 'POST':
        name = request.form.get('name')
        content = request.form.get('message')
        now = datetime.utcnow()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        new_message = Message(name=name, content=content, time=time)
        db.session.add(new_message)
        db.session.commit()
        flash('Message added.', 'success')
        return redirect(url_for('web.commit_page'))

    messages = Message.query.all()
    return render_template('commit.html', messages=messages, get_random_gradient=get_random_gradient)


@bp.route('/tools')
def tools_page():
    webs = Web.query.all()
    return render_template('tools.html', webs=webs)


@bp.route('/secret')
def secret_page():
    return render_template('secret.html')


@bp.route('/like/<int:item_id>', methods=['POST'])
def like(item_id):
    like_record = Like.query.get(item_id)
    if like_record is None:
        like_record = Like(id=item_id, like_count=1)
        db.session.add(like_record)
    else:
        like_record.like_count += 1
    db.session.commit()
    return jsonify({'item_id': item_id, 'like_count': like_record.like_count})


@bp.route('/get_like_count/<int:item_id>', methods=['GET'])
def get_like_count(item_id):
    like_record = Like.query.get(item_id)
    like_count = like_record.like_count if like_record else 0
    return jsonify({'item_id': item_id, 'like_count': like_count})


@bp.route('/delete/<int:message_id>', methods=['POST', 'GET'])
@login_required
def delete_message(message_id):
    if request.method == 'POST':
        message = Message.query.get_or_404(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            flash('Message deleted.')
        return redirect(url_for('web.commit_page'))
    return redirect(url_for('web.commit_page'))


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('web.settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('web.index_page'))
    return render_template('settings.html')


@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
