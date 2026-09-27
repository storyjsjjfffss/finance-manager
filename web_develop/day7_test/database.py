"""数据库配置与 Session 管理。"""
import os

#from pathlib import Path
from dotenv import load_dotenv

from sqlmodel import Session, SQLModel, create_engine


# 数据库文件和代码放在同一个项目目录，避免工作目录变化导致找错数据库。
#BASE_DIR = Path(__file__).resolve().parent
#DB_PATH = BASE_DIR / "finance.db"
#SQLITE_URL = f"sqlite:///{DB_PATH.as_posix()}"

load_dotenv()#读取.env,把变量存进环境变量

DATABASE_URL = os.getenv(
    "DATABASE_URL"
    "sqlite:///finance.db"#找不到就默认
)  # 得到真实的数据库地址

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)


def create_db_and_tables() -> None:
    """创建尚不存在的数据库表。"""
    # 导入 models 的目的：确保 User / Transaction 已经注册到 metadata。
    from models import User, Transaction  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session():
    """为每个请求提供一个独立的数据库 Session。"""
    with Session(engine) as session:
        yield session
