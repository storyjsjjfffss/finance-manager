# 个人记账 FastAPI：拆分版

这是从原来的 `web6_crud_final.py` 拆出来的项目结构。

## 目录

```text
finance_api_split/
├── main.py                 # FastAPI 入口、CORS、路由注册
├── database.py             # SQLite、engine、Session
├── models.py               # User / Transaction 数据库表
├── schemas.py              # API 输入模型
├── auth.py                 # 密码哈希、JWT、当前用户依赖
├── routers/
│   ├── __init__.py
│   ├── auth.py             # 注册 / 登录
│   └── transactions.py     # 账单 CRUD / 报表
├── requirements.txt
└── README.md
```

## 启动

把这些文件复制到原来的 `day7_test` 目录，和原来的 `finance.db` 放在一起。

然后在该目录打开终端：

```powershell
uvicorn main:app --reload
```

Swagger：

```text
http://127.0.0.1:8000/docs
```

## CRUD

```text
POST   /transactions
GET    /transactions
GET    /transactions/report
GET    /transactions/{t_id}
PUT    /transactions/{t_id}
DELETE /transactions/{t_id}
```

注意：`/transactions/report` 必须注册在 `/transactions/{t_id}` 前面。

## 重要

如果当前目录已经存在 `finance.db`，保留它即可，这样原来的用户和账单数据仍然使用同一个 SQLite 文件。

部署时建议通过环境变量设置 `SECRET_KEY`，不要把真实密钥写进代码或上传到 GitHub。
