from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel  # <-- 新增导入

# ==========================================
# 1. 定义数据模型 (继承 Pydantic 的 BaseModel)
# 它的作用类似于你之前写的 Transaction 类，但更强大
# ==========================================
class TransactionCreate(BaseModel):
    amount: float          # 必填项，且必须是数字
    category: str          # 必填项，必须是字符串
    t_type: str = "支出"   # 选填项，默认值为 "支出"

# 1. 创建 FastAPI 实例（这就是你的服务器大骨架）
app = FastAPI()

# 2. 路由（Routing）：定义网址与函数的对应关系
# @app.get("/") 意味着当用户在浏览器访问根目录时，触发下方的函数
@app.get("/")
def read_root():
    # 以前我们用 print()，现在直接 return 字典，FastAPI 会自动将其转换为 JSON 发给浏览器
    return {"message": "Hello World! 欢迎来到 Web 开发的世界！"}


# ==========================================
# 2. 定义 POST 路由（注意这里是 @app.post 而不是 get）
# ==========================================
@app.post("/transactions")
def create_transaction(transaction: TransactionCreate):
    # 当浏览器/客户端发来 JSON 数据时，FastAPI 会自动拦截并校验：
    # 如果传的 amount 是 "abc"，直接拦截报错 422。
    # 如果校验通过，会自动转换成 transaction 对象，供你用点号直接调用！

    # 模拟把数据存入数据库的逻辑
    saved_data = {
        "record_id": 1001,
        "saved_amount": transaction.amount,
        "saved_category": transaction.category,
        "saved_type": transaction.t_type,
        "status": "插入数据库成功！"
    }

    return saved_data

@app.get("/api/status")
def check_status():
    return {
        "status": "success",
        "version": "1.0",
        "active_users": 150
    }
# 尖括号 {user_id} 表示这是一个动态变化的路径变量
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "message": f"正在查询第 {user_id} 号用户的详细信息"
    }

# 搜索接口，keyword 是必传参数，page 有默认值所以是可选参数
@app.get("/search")
def search_items(keyword: str, page: int = 1):
    return {
        "search_keyword": keyword,
        "current_page": page,
        "results": [f"{keyword} 款式A", f"{keyword} 款式B"]
    }
# 3. 启动服务器
if __name__ == "__main__":
    # 运行当前的 app，开放本地 8000 端口，开启热更新（reload=True）
    uvicorn.run("day31_api:app", host="127.0.0.1", port=8000, reload=True)