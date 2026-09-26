"""
web6_clean.py
个人记账 FastAPI 示例

功能：
1. 用户注册
2. 用户登录（OAuth2 Password + JWT）
3. 新增账单
4. 查询当前用户自己的账单
5. 删除当前用户自己的账单
6. 当前用户的支出分类汇总
"""

import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select


# ============================================================
# 1. 基础配置
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "finance.db"

# 这个连接字符串告诉 SQLAlchemy / SQLModel：
# 使用 SQLite，并把数据库文件放到当前 Python 文件所在目录。
sqlite_url = f"sqlite:///{DB_PATH.as_posix()}"

# FastAPI 可能在不同线程中处理请求。
# 官方 SQLModel 示例对 SQLite 使用这个参数。
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    echo=False,  # 学习 SQL 时可临时改成 True
)


# ============================================================
# 2. 数据库表模型
# ============================================================

class User(SQLModel, table=True):
    """用户表。"""

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str


class Transaction(SQLModel, table=True):
    """账单表。"""

    id: int | None = Field(default=None, primary_key=True)
    amount: float
    category: str
    t_type: str = "支出"
    user_id: int = Field(foreign_key="user.id", index=True)


# ============================================================
# 3. API 请求模型
#    不直接把数据库表 Transaction 当作前端输入模型
# ============================================================

class UserCreate(BaseModel):
    """注册时前端提交的数据。"""

    username: str
    password: str


class TransactionCreate(BaseModel):
    """新增账单时前端提交的数据。"""

    amount: float
    category: str
    t_type: str = "支出"


# ============================================================
# 4. 数据库初始化
# ============================================================

def create_db_and_tables() -> None:
    """创建数据库中尚不存在的表。"""
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 启动 / 关闭生命周期。"""
    create_db_and_tables()
    yield


# ============================================================
# 5. 密码处理
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],#指定用哪些哈希算法(计划）
    deprecated="auto", #自动把非首选算法标记为"已弃用"（不在推荐）
)


def get_password_hash(password: str) -> str:
    """将明文密码转换为密码哈希。"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码是否与数据库中的哈希匹配。"""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# 6. JWT 配置与生成
# ============================================================

# 开发环境可以使用默认值；
# 正式项目建议通过环境变量提供 SECRET_KEY。
SECRET_KEY = os.getenv(
    #os.getenv(key, default) 的作用：先读环境变量，读不到就用默认值。
    #获取环境变量 get env

    "SECRET_KEY",
    "dev-only-change-this-secret-key",
)

ALGORITHM = "HS256" #HS256 是 JWT 的一种签名算法，全称 HMAC-SHA256。 对称加密：签名和验签用同一个密钥
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #访问令牌过期时间（分钟）


def create_access_token(data: dict) -> str:
    """生成 JWT 访问令牌。"""
    to_encode = data.copy()#不直接改调用者传进来的字典。如果直接 data.update(...)，会污染原字典

    expire = datetime.now(timezone.utc) + timedelta(
        #JWT 的 exp 是 UNIX 时间戳，本质就是 UTC。如果用本地时间
        # （比如北京时间 UTC+8），会差 8 小时，导致令牌要么提前失效、要么延后失效
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})
    #exp 是 JWT 的标准声明字段（registered claim），jwt.decode 会自动识别并检查它。
    return jwt.encode(
        #JWT字符串
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ============================================================
# 7. FastAPI 依赖：数据库 Session
# ============================================================

def get_session():
    """为每个请求提供一个数据库 Session。"""
    with Session(engine) as session:
        yield session


# ============================================================
# 8. FastAPI 依赖：JWT 身份验证
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #OAuth2密码承载
# OAuth2PasswordBearer是 FastAPI 提供的安全方案类
#tokenUrl="login"：告诉 FastAPI 去哪里获取令牌，即你的登录接口路径


def get_current_user(#验证身份
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """
    从 Authorization: Bearer <token> 中解析当前用户。

    验证流程：
    1. JWT 签名是否正确
    2. JWT 是否过期
    3. token 中是否存在 sub
    4. 数据库中该用户名是否仍然存在
    """

    credentials_exception = HTTPException(
        status_code=401,
        detail="身份验证失败，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,#就是客户端传过来的 JWT。
            SECRET_KEY,
            algorithms=[ALGORITHM],#HS256
        )

        username = payload.get("sub")#payload 本质上是一个字典

        if not username:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if user is None:
        raise credentials_exception

    return user


# ============================================================
# 9. 创建 FastAPI 应用
# ============================================================

app = FastAPI(
    title="Personal Finance API",
    version="1.0.0",
    lifespan=lifespan, #lifespan 里 yield 之前的代码   ← 建表、初始化
)


# ============================================================
# 10. CORS 跨域配置
# ============================================================

app.add_middleware(
    CORSMiddleware,# 中间件类
    allow_origins=["*"],   # 开发环境使用；正式项目改成具体前端地址 允许的源
    allow_credentials=False,# 是否允许携带凭证
    allow_methods=["*"],# 允许的 HTTP 方法
    allow_headers=["*"], # 允许的请求头
)


# ============================================================
# 11. 用户注册
# ============================================================

@app.post("/register")
def register_user(user: UserCreate):
    with Session(engine) as session:

        # 1. 检查用户名是否已存在
        existing_user = session.exec(
            select(User).where(User.username == user.username)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="用户名已被注册",
            )

        # 2. 密码只保存哈希值，不保存明文
        hashed_password = get_password_hash(user.password)

        # 3. 创建用户
        new_user = User(
            username=user.username,
            password_hash=hashed_password,
        )

        session.add(new_user)
        session.commit()

    return {
        "message": f"欢迎 {user.username}，注册成功！"
    }


# ============================================================
# 12. 用户登录
# ============================================================

@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    使用 OAuth2 Password Form 登录。

    Swagger /docs 中会自动显示 username 和 password 输入框。
    """

    with Session(engine) as session:

        db_user = session.exec(
            select(User).where(
                User.username == form_data.username
            )
        ).first()

        if db_user is None:
            raise HTTPException(
                status_code=400,
                detail="用户名或密码错误",
            )

        if not verify_password(
            form_data.password,
            db_user.password_hash,
        ):
            raise HTTPException(
                status_code=400,
                detail="用户名或密码错误",
            )

        access_token = create_access_token(
            data={"sub": db_user.username}
        )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ============================================================
# 13. 查看当前用户自己的账单
# ============================================================

@app.get("/transactions")
def get_all_transactions(
        #Depends(某个函数) 的意思是：调用这个函数，把它返回值注入给参数。
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
        #这个会话连接的是哪个数据库，取决于 get_session 里面用的 engine 绑定到哪个数据库。
):
    transactions = session.exec(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
    ).all()

    return transactions


# ============================================================
# 14. 新增当前用户的账单
# ============================================================

@app.post("/transactions")
def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    transaction = Transaction(
        amount=transaction_data.amount,
        category=transaction_data.category,
        t_type=transaction_data.t_type,
        user_id=current_user.id,
    )

    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return {
        "message": "写入数据库成功",
        "data": transaction,
    }


# ============================================================
# 15. 删除当前用户自己的账单
# ============================================================

@app.delete("/transactions/{t_id}")
def delete_transaction(
    t_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    transaction = session.get(Transaction, t_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail=f"数据库中未找到 ID 为 {t_id} 的账单",
        )

    # 防止用户删除别人的账单
    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="无权删除其他用户的账单",
        )

    session.delete(transaction)
    session.commit()

    return {
        "message": "数据库删除成功"
    }


# ============================================================
# 16. 当前用户支出汇总
# ============================================================

@app.get("/transactions/report")
def generate_report(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    expense_summary: dict[str, float] = {}

    transactions = session.exec(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
    ).all()

    for transaction in transactions:
        if transaction.t_type == "支出":
            expense_summary[transaction.category] = (
                expense_summary.get(transaction.category, 0.0)
                + transaction.amount
            )

    return {
        "report_type": "支出汇总",
        "data": expense_summary,
    }


# ============================================================
# 17. 启动入口
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "web6_clean:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
