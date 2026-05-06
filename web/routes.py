from datetime import datetime, timezone

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import db
from .functions import get_random_gradient
from .models import Like, Md_test, Message, User, Web

bp = Blueprint("web", __name__)
VALID_WEB_TYPES = {"web", "app", "book"}


def _form_text(name, max_length=None):
    value = (request.form.get(name) or "").strip()
    if max_length and len(value) > max_length:
        return ""
    return value


def _get_content_form():
    author = _form_text("author", 20)
    content = _form_text("content")
    if not author or not content:
        flash("标题和内容不能为空。", "warning")
        return None, None
    return author, content


def _published_contents(page):
    return (
        Md_test.query.filter_by(page=page, is_published=True)
        .order_by(Md_test.id.desc())
        .all()
    )


@bp.context_processor
def inject_user():
    return {"user": current_user}


@bp.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = _form_text("username", 20)
        password = request.form.get("password") or ""

        if not username or not password:
            flash("用户名和密码不能为空。", "warning")
            return redirect(url_for("web.login"))

        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            login_user(user)
            flash("登录成功。", "success")
            return redirect(url_for("web.index_page"))

        flash("用户名或密码错误。", "danger")
        return redirect(url_for("web.login"))

    return render_template("login.html")


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("已退出登录。", "success")
    return redirect(url_for("web.index_page"))


@bp.get("/")
def index_page():
    return render_template("index.html")


@bp.get("/life")
def life_page():
    return render_template("life.html", contents=_published_contents("life"))


@bp.post("/life/delete/<int:id>")
@login_required
def delete_life(id):
    md_test = Md_test.query.get_or_404(id)
    db.session.delete(md_test)
    db.session.commit()
    flash("删除成功。", "success")
    return redirect(url_for("web.life_page"))


@bp.post("/life/edit/<int:id>")
@login_required
def edit_life(id):
    md_test = Md_test.query.get_or_404(id)
    author, content = _get_content_form()
    if not author:
        return redirect(url_for("web.life_page"))

    md_test.author = author
    md_test.content = content
    md_test.is_published = True
    db.session.commit()
    flash("更新成功。", "success")
    return redirect(url_for("web.life_page"))


@bp.post("/life/add")
@login_required
def add_life():
    author, content = _get_content_form()
    if not author:
        return redirect(url_for("web.life_page"))

    db.session.add(Md_test(page="life", author=author, content=content, is_published=True))
    db.session.commit()
    flash("新增成功。", "success")
    return redirect(url_for("web.life_page"))


@bp.get("/self_learn")
def self_learn_page():
    return render_template("self_learn.html", contents=_published_contents("learn"))


@bp.post("/self_learn/delete/<int:id>")
@login_required
def delete_self_learn(id):
    md_test = Md_test.query.get_or_404(id)
    db.session.delete(md_test)
    db.session.commit()
    flash("删除成功。", "success")
    return redirect(url_for("web.self_learn_page"))


@bp.post("/self_learn/edit/<int:id>")
@login_required
def edit_self_learn(id):
    md_test = Md_test.query.get_or_404(id)
    author, content = _get_content_form()
    if not author:
        return redirect(url_for("web.self_learn_page"))

    md_test.author = author
    md_test.content = content
    md_test.is_published = True
    db.session.commit()
    flash("更新成功。", "success")
    return redirect(url_for("web.self_learn_page"))


@bp.post("/self_learn/add")
@login_required
def add_self_learn():
    author, content = _get_content_form()
    if not author:
        return redirect(url_for("web.self_learn_page"))

    db.session.add(Md_test(page="learn", author=author, content=content, is_published=True))
    db.session.commit()
    flash("新增成功。", "success")
    return redirect(url_for("web.self_learn_page"))


@bp.route("/commit", methods=["GET", "POST"])
def commit_page():
    if request.method == "POST":
        name = _form_text("name", 20)
        content = _form_text("message")
        if not name or not content:
            flash("昵称和留言不能为空。", "warning")
            return redirect(url_for("web.commit_page"))

        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(Message(name=name, content=content, time=now))
        db.session.commit()
        flash("留言成功。", "success")
        return redirect(url_for("web.commit_page"))

    messages = Message.query.order_by(Message.id.desc()).all()
    return render_template(
        "commit.html",
        messages=messages,
        get_random_gradient=get_random_gradient,
    )


@bp.get("/tools")
def tools_page():
    webs = Web.query.order_by(Web.id.desc()).all()
    return render_template("tools.html", webs=webs)


@bp.post("/tools/add")
@login_required
def tools_add():
    id_type = _form_text("id_type", 20)
    link_url = _form_text("link_url", 255)
    link_name = _form_text("link_name", 255)
    description = _form_text("description")

    if id_type not in VALID_WEB_TYPES or not link_url or not link_name:
        flash("分类、链接和名称不能为空，分类仅支持 web/app/book。", "warning")
        return redirect(url_for("web.tools_page"))

    db.session.add(
        Web(
            id_type=id_type,
            link_url=link_url,
            link_name=link_name,
            description=description,
        )
    )
    db.session.commit()
    flash("新增成功。", "success")
    return redirect(url_for("web.tools_page"))


@bp.post("/tools/delete/<int:id>")
@login_required
def delete_tools(id):
    web = Web.query.get_or_404(id)
    db.session.delete(web)
    db.session.commit()
    flash("删除成功。", "success")
    return redirect(url_for("web.tools_page"))


@bp.post("/tools/edit/<int:id>")
@login_required
def edit_tools(id):
    web = Web.query.get_or_404(id)
    id_type = _form_text("id_type", 20)
    link_name = _form_text("link_name", 255)
    link_url = _form_text("link_url", 255)
    description = _form_text("description")

    if id_type not in VALID_WEB_TYPES or not link_url or not link_name:
        flash("分类、链接和名称不能为空，分类仅支持 web/app/book。", "warning")
        return redirect(url_for("web.tools_page"))

    web.id_type = id_type
    web.link_name = link_name
    web.link_url = link_url
    web.description = description
    db.session.commit()
    flash("更新成功。", "success")
    return redirect(url_for("web.tools_page"))


@bp.get("/secret")
def secret_page():
    return render_template("secret.html")


@bp.post("/like/<int:item_id>")
def like(item_id):
    like_record = db.session.get(Like, item_id)
    if like_record is None:
        like_record = Like(id=item_id, like_count=1)
        db.session.add(like_record)
    else:
        like_record.like_count += 1
    db.session.commit()
    return jsonify({"item_id": item_id, "like_count": like_record.like_count})


@bp.get("/get_like_count/<int:item_id>")
def get_like_count(item_id):
    like_record = db.session.get(Like, item_id)
    like_count = like_record.like_count if like_record else 0
    return jsonify({"item_id": item_id, "like_count": like_count})


@bp.post("/delete/<int:message_id>")
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash("留言已删除。", "success")
    return redirect(url_for("web.commit_page"))


@bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        name = _form_text("name", 20)
        if not name:
            flash("昵称不能为空，且不能超过 20 个字符。", "warning")
            return redirect(url_for("web.settings"))

        current_user.name = name
        db.session.commit()
        flash("设置已更新。", "success")
        return redirect(url_for("web.index_page"))
    return render_template("settings.html")


@bp.get("/imgs")
def imgs_page():
    return render_template("imgs.html")
