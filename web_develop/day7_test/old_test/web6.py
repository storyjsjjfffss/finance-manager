from contextlib import asynccontextmanager
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware  # <-- 1. 新增导入
from fastapi import FastAPI, HTTPException
from collections import defaultdict
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError


# ==========================================
# 1. 数据库模型定义
# ==========================================
# 新增：用户表
class User(SQLModel, table=True):
    # 👇 补上这行核心代码：告诉底层如果表已存在于内存，直接复用，别报错
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True) # unique=True 确保用户名不能重复
    password_hash: str  # ⚠️ 极其重要：只存哈希乱码，绝不存明文密码！

class Transaction(SQLModel, table=True):
    # 核心修复点：告诉底层，如果表已经在内存里了，就直接复用，不要报错

    __table_args__ = {'extend_existing': True}

    id: int | None = Field(default=None, primary_key=True)#主键通常是数据库自动生成
    amount: float
    category: str
    t_type: str = "支出"

    user_id: int | None = Field(default=None, foreign_key="user.id")


sqlite_url = "sqlite:///finance.db"
engine = create_engine(sqlite_url, echo=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 这是一个将明文密码转化为乱码的辅助函数
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 这个函数会在底层把传进来的明文用同样的盐值加密，再与数据库里的哈希比对
    return pwd_context.verify(plain_password, hashed_password)

# 定义前端发来的注册数据格式（前端发的是明文 password，不是 hash）
class UserCreate(BaseModel):
    username: str
    password: str
class UserLogin(BaseModel):
    username: str
    password: str
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ==========================================
# JWT 令牌配置
# ==========================================
# ⚠️ 密钥：这是你服务器的“私章”，绝对不能泄露。有了它别人才无法伪造手环。
SECRET_KEY = "my_super_secret_finance_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 手环有效期30分钟

def create_access_token(data: dict):
    to_encode = data.copy()
    # 计算过期时间
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # 盖上私章，生成防伪字符串
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ==========================================
# 身份验证门禁系统 (Depends)
# ==========================================
# 告诉 FastAPI：前端需要在 HTTP 的 Header 里携带手环
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    # 提前准备好拦截话术
    credentials_exception = HTTPException(
        status_code=401,
        detail="身份验证失败，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. 验真伪：用我们的服务器私章解密手环
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # 提取名字
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        # 如果手环被伪造、或者过期了，直接报错拦截
        raise credentials_exception

    # 2. 查户口：根据手环上的名字，去数据库核实这人还在不在
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise credentials_exception

        # 3. 验票通过，直接把这个人的数据库信息 (User 对象) 移交给下一个环节
        return user

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
def create_transaction(transaction: Transaction, current_user: User = Depends(get_current_user)):    # Session 是你与数据库通话的“对讲机”
    with Session(engine) as session:
        # 核心魔法：强行给这笔账单打上当前操作者的 ID 钢印！
        # 无论前端传什么，这笔账只属于持有当前手环的人
        transaction.user_id = current_user.id
        session.add(transaction)  # 把对象加入对讲机通道
        session.commit()  # 正式提交（写入硬盘）
        session.refresh(transaction)  # 把数据库生成的自增 ID 刷新回对象里
        return {"message": "✅ 写入数据库成功", "data": transaction}


@app.post("/register")
def register_user(user: UserCreate):
    with Session(engine) as session:
        # 第一关：去数据库里搜一搜，这个名字是不是被人用过了？
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="抱歉，用户名已被注册")

        # 第二关：把用户传过来的明文密码，送进粉碎机变成乱码
        hashed_pwd = get_password_hash(user.password)

        # 第三关：把新用户（携带用户名和已经变异的密码串）正式存入数据库
        new_user = User(username=user.username, password_hash=hashed_pwd)
        session.add(new_user)
        session.commit()

        return {"message": f"✅ 欢迎 {user.username}，注册成功！"}


@app.post("/login")
# 👇 注意这里：把 user: UserLogin 换成了专门接表单的工具
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        # 👇 对应的，用 form_data.username 和 form_data.password 来验证
        db_user = session.exec(select(User).where(User.username == form_data.username)).first()

        if not db_user:
            raise HTTPException(status_code=400, detail="用户名或密码错误")

        if not verify_password(form_data.password, db_user.password_hash):
            raise HTTPException(status_code=400, detail="用户名或密码错误")

        access_token = create_access_token(data={"sub": db_user.username})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "message": "登录成功"
        }
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