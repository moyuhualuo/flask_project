# 部署说明

## 本地运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app initdb
flask --app app admin
flask --app app run
```

默认地址：

```text
http://127.0.0.1:5000
```

## Vercel 部署

项目根目录的 `app.py` 导出了顶层 Flask `app`，Vercel 可以直接识别 Python/Flask 应用。

部署前建议在 Vercel 项目环境变量中配置：

```text
SECRET_KEY=<强随机字符串>
DATABASE_URL=<生产数据库连接，可选但推荐>
AUTO_CREATE_DB=1
```

## 数据库说明

本地默认使用 SQLite：

```text
data.db
```

Vercel 函数环境只有 `/tmp` 可写，因此未配置 `DATABASE_URL` 时只能用于演示，数据不会长期保存。需要正式保存留言、文章、点赞和工具记录时，请配置 Postgres 等外部数据库。

## 健康检查

```text
GET /healthz
```

正常返回：

```json
{"status":"ok"}
```

## 验证命令

```powershell
python -m compileall app.py config.py web
python -m pip check
python -c "from app import app; client = app.test_client(); paths=['/','/login','/life','/secret','/healthz']; assert all(client.get(path).status_code == 200 for path in paths)"
```
