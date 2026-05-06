# Flask Project

一个简洁的 Flask 个人站点。项目包含首页、文章页、留言板、工具收藏页、图片墙和一个贪吃蛇小游戏。

## 目录结构

```text
app.py                 Vercel 和本地启动入口
config.py              Flask 配置和数据库连接
web/__init__.py        应用工厂、扩展初始化、CLI 注册
web/routes.py          页面路由和表单处理
web/models.py          SQLAlchemy 数据模型
web/templates/         Jinja2 页面模板
web/static/            CSS、JavaScript、图片和图标
docs/                  部署说明和代码 review 记录
```

## 本地运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app initdb
flask --app app admin
flask --app app run
```

浏览器访问：

```text
http://127.0.0.1:5000
```

## 环境变量

- `SECRET_KEY`：生产环境必须设置，用于会话签名。
- `DATABASE_URL`：生产数据库连接。Vercel 上建议使用 Postgres 等外部数据库。
- `AUTO_CREATE_DB`：默认 `1`，会在启动时自动建表；稳定后可设为 `0`。

如果没有设置 `DATABASE_URL`，本地会使用 SQLite 文件；Vercel 上会临时写入 `/tmp`，数据不会持久保存。

## Vercel

Vercel 会识别根目录的 `app.py`，其中导出了顶层 Flask `app`。部署前在 Vercel 项目里配置 `SECRET_KEY`，需要持久数据时再配置 `DATABASE_URL`。

更多部署注意事项见 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)。

## 验证

```powershell
python -m compileall app.py config.py web
python -m pip check
python -c "from app import app; client = app.test_client(); assert client.get('/healthz').status_code == 200"
```

## 维护记录

- 代码 review 记录：[docs/CODE_REVIEW.md](docs/CODE_REVIEW.md)
- 部署说明：[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
