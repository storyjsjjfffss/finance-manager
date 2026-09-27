"""API 输入模型：控制前端可以提交什么数据。"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """注册请求。"""

    username: str
    password: str


class TransactionCreate(BaseModel):
    """新增账单请求。"""

    amount: float
    category: str
    t_type: str = "支出"


class TransactionUpdate(BaseModel):
    """修改账单请求。"""

    amount: float
    category: str
    t_type: str = "支出"
