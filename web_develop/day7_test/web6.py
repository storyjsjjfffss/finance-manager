from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware  # <-- 1. 新增导入
from fastapi import FastAPI, HTTPException
from collections import defaultdict

from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn


# ==========================================
# 1. 数据库模型定义
# ==========================================
class Transaction(SQLModel, table=True):
    # 核心修复点：告诉底层，如果表已经在内存里了，就直接复用，不要报错

    __table_args__ = {'extend_existing': True}

    id: int | None = Field(default=None, primary_key=True)
    amount: float
    category: str
    t_type: str = "支出"


sqlite_url = "sqlite:///finance.db"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ==========================================
# 2. 现代 FastAPI 生命周期管理 (Lifespan)
# 替代已被淘汰的 @app.on_event("startup")
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):#直接自动建立表
    # yield 之前的代码，会在服务器启动时执行
    create_db_and_tables()
    yield
    # yield 之后的代码，可以在服务器关闭时执行清理工作（目前留空即可）


# 将 lifespan 注入到 FastAPI 实例中
app = FastAPI(lifespan=lifespan)

# 2. 新增跨域配置 (CORS)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有网页访问（仅限开发环境）
    allow_credentials=True,
    allow_methods=["*"],  # 允许 GET, POST, DELETE 等所有方法
    allow_headers=["*"],  # 允许所有请求头
)

# ==========================================
# 3. 路由重构 (与数据库真实交互)
# ==========================================
@app.post("/transactions")
def create_transaction(transaction: Transaction):
    # Session 是你与数据库通话的“对讲机”
    with Session(engine) as session:
        session.add(transaction)  # 把对象加入对讲机通道
        session.commit()  # 正式提交（写入硬盘）
        session.refresh(transaction)  # 把数据库生成的自增 ID 刷新回对象里
        return {"message": "✅ 写入数据库成功", "data": transaction}


@app.get("/transactions")
# transactions 是一个列表，列表中的每个元素都是 Transaction 对象
def get_all_transactions():
    with Session(engine) as session:
        # select(Transaction) 相当于向数据库下达查询全表指令
        transactions = session.exec(select(Transaction)).all()
        return transactions


@app.delete("/transactions/{t_id}")
def delete_transaction(t_id: int):
    with Session(engine) as session:
        # 先根据主键 ID 查出该条数据
        transaction = session.get(Transaction, t_id)
        if not transaction:
            raise HTTPException(status_code=404, detail=f"数据库中未找到 ID 为 {t_id} 的账单")

        # 执行删除并提交硬盘
        session.delete(transaction)
        session.commit()
        return {"message": "🗑️ 数据库删除成功"}

@app.get("/transactions/report")
def generate_report():
    expense_summary = defaultdict(float)

    transactions = get_all_transactions()

    for transaction in transactions:
        if transaction.t_type == "支出":
            expense_summary[transaction.category] += transaction.amount

    return {
        "report_type": "支出汇总",
        "data": dict(expense_summary)
    }

if __name__ == "__main__":
    uvicorn.run("web6:app", host="127.0.0.1", port=8000, reload=True)