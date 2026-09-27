"""个人记账 FastAPI：多用户 + JWT + 完整 CRUD"""

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
sqlite_url = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    echo=True,
)


# ============================================================
# 2. 数据库模型：真正对应数据库表
# ============================================================

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: float
    category: str
    t_type: str = "支出"
    user_id: int = Field(foreign_key="user.id", index=True)


# ============================================================
# 3. API 数据模型：前端提交什么，由这些模型控制
# ============================================================

class UserCreate(BaseModel):
    username: str
    password: str


class TransactionCreate(BaseModel):
    amount: float
    category: str
    t_type: str = "支出"


class TransactionUpdate(BaseModel):
    amount: float
    category: str
    t_type: str = "支出"


# ============================================================
# 4. 数据库初始化
# ============================================================

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# ============================================================
# 5. 密码处理
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# 6. JWT
# ============================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-only-change-this-secret-key",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ============================================================
# 7. Session 依赖
# ============================================================

def get_session():
    with Session(engine) as session:
        yield session


# ============================================================
# 8. JWT 身份验证依赖
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="身份验证失败，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

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
# 9. FastAPI
# ============================================================

app = FastAPI(
    title="Personal Finance API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 10. 用户注册
# ============================================================

@app.post("/register")
def register_user(user: UserCreate):
    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(User.username == user.username)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="用户名已被注册",
            )

        new_user = User(
            username=user.username,
            password_hash=get_password_hash(user.password),
        )

        session.add(new_user)
        session.commit()

    return {"message": "注册成功"}


# ============================================================
# 11. 登录
# ============================================================

@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    with Session(engine) as session:
        db_user = session.exec(
            select(User).where(User.username == form_data.username)
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
# 12. C — Create：新增账单
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
        "message": "账单创建成功",
        "data": transaction,
    }


# ============================================================
# 13. R — Read：查询当前用户全部账单
# ============================================================

@app.get("/transactions")
def get_all_transactions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    transactions = session.exec(
        select(Transaction).where(
            Transaction.user_id == current_user.id
        )
    ).all()

    return transactions


# ============================================================
# 14. R — Read：按 ID 查询当前用户的一条账单
# ============================================================
@app.get("/transactions/report")
def generate_report(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    expense_summary: dict[str, float] = {}

    transactions = session.exec(
        select(Transaction).where(
            Transaction.user_id == current_user.id
        )
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

@app.get("/transactions/{t_id}")
def get_transaction(
    t_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    transaction = session.get(Transaction, t_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="账单不存在",
        )

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="无权访问其他用户的账单",
        )

    return transaction


# ============================================================
# 15. U — Update：修改当前用户的一条账单
# ============================================================

@app.put("/transactions/{t_id}")
def update_transaction(
    t_id: int,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    transaction = session.get(Transaction, t_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="账单不存在",
        )

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="无权修改其他用户的账单",
        )

    transaction.amount = transaction_data.amount
    transaction.category = transaction_data.category
    transaction.t_type = transaction_data.t_type

    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return {
        "message": "账单修改成功",
        "data": transaction,
    }


# ============================================================
# 16. D — Delete：删除当前用户的一条账单
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
            detail="账单不存在",
        )

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="无权删除其他用户的账单",
        )

    session.delete(transaction)
    session.commit()

    return {"message": "账单删除成功"}


# ============================================================
# 17. 报表：当前用户支出分类汇总
# ============================================================

#转移到GET /transactions/id之前了


# ============================================================
# 18. 启动
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "web6_crud_final:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
