# 代码 Review 记录

## Review 范围

本次 review 覆盖 Flask 应用启动、配置、路由、模板、静态资源、Vercel 部署准备和 UI 主题切换。

## 已处理的问题

- `SECRET_KEY` 原先每次启动随机生成，冷启动后会导致会话失效；已改为从环境变量读取，并保留本地开发默认值。
- `requirements.txt` 原先包含大量未使用依赖，并且是 UTF-16 编码；已精简为 Flask 运行所需依赖并改为 UTF-8。
- Flask-Login 的 `login_view` 原先指向错误端点；已改为 `web.login`。
- SQLAlchemy 的部分旧式主键查询已改为 `db.session.get`。
- 留言删除等危险操作已改为只接受 `POST`。
- 表单输入增加基础 trim 和长度校验，避免空内容直接写入数据库。
- 增加 `/healthz`，方便本地和部署平台做健康检查。
- 增加黑白主题切换，并改善登录页、文章页和贪吃蛇页面的对比度。
- 贪吃蛇页面增加得分、坚持时间、最高纪录和重新开始能力。
- 增加 `vercel.json`、`.env.example`、`.python-version` 和部署说明文档。

## 剩余风险

- 生产环境必须配置 `SECRET_KEY`，不要使用默认开发值。
- Vercel 上未配置 `DATABASE_URL` 时，SQLite 只能临时写入 `/tmp`，数据不持久。
- 当前没有 CSRF 防护，后续如果开放登录后的写操作给更多用户，建议引入 Flask-WTF 或自定义 CSRF token。
- 自动建表适合个人站点和演示环境；数据结构稳定后建议切换到迁移工具管理 schema。
- 主题切换使用 `localStorage`，极少数禁用本地存储的浏览器会退回默认主题。

## 验证结果

已执行：

```powershell
python -m compileall app.py config.py web
python -m pip check
python -c "from app import app; client = app.test_client(); paths=['/','/login','/life','/self_learn','/tools','/commit','/secret','/healthz']; assert all(client.get(path).status_code == 200 for path in paths)"
node --check web/static/js/theme.js
node --check web/static/js/game.js
node --check web/static/js/snake.js
node --check web/static/js/input.js
node --check web/static/js/food.js
node --check web/static/js/snakeUtils.js
```
