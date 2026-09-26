from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from collections import defaultdict
import uvicorn

app = FastAPI()


class Transaction(BaseModel):
    amount: float
    category: str
    t_type: str = "支出"


# 1. 升级版模拟数据库：使用字典，格式为 {账单ID: Transaction对象}
fake_db = {}
# 用于自动生成递增的账单 ID
current_id = 1


@app.post("/transactions")
def create_transaction(transaction: Transaction):
    global current_id
    # 将生成的 ID 作为键，存入字典
    fake_db[current_id] = transaction
    current_id += 1  # ID 自增，为下一次做准备

    return {
        "message": "✅ 账单记录成功！",
        "transaction_id": current_id - 1
    }


@app.get("/transactions")
def get_all_transactions():
    # 直接返回字典，FastAPI 会自动转换为 {"1": {...}, "2": {...}} 格式的 JSON
    return fake_db


# ==========================================
# 新增接口：根据 ID 删除特定账单 (DELETE)
# ==========================================
@app.delete("/transactions/{t_id}")
def delete_transaction(t_id: int):
    # 2. 异常防御：如果试图删除的 ID 根本不存在于字典中
    if t_id not in fake_db:
        # 主动抛出 HTTP 404 错误，不让服务器崩溃
        raise HTTPException(
            status_code=404,
            detail=f"哎呀，ID 为 {t_id} 的账单不存在！"
        )

    # 3. 正常删除逻辑
    deleted_t = fake_db.pop(t_id)
    return {
        "message": "🗑️ 删除成功！",
        "deleted_data": deleted_t
    }


@app.get("/report")
def generate_report():
    expense_summary = defaultdict(float)
    # 遍历字典的 values (即 Transaction 对象)
    for t in fake_db.values():
        if t.t_type == "支出":
            expense_summary[t.category] += t.amount

    return {
        "report_type": "支出汇总",
        "data": expense_summary
    }


if __name__ == "__main__":
    uvicorn.run("web 4:app", host="127.0.0.1", port=8000, reload=True)