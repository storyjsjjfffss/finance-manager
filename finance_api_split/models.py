"""数据库表模型：直接对应 SQLite 中的真实表。"""

from sqlmodel import Field, SQLModel


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
