"""账单 CRUD 与报表路由。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from auth import get_current_user
from database import get_session
from models import Transaction, User
from schemas import TransactionCreate, TransactionUpdate


router = APIRouter()


@router.post("/transactions")
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


@router.get("/transactions")
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


# 注意：固定路径 /transactions/report 必须放在
# 动态路径 /transactions/{t_id} 前面，避免 report 被当成 t_id。
@router.get("/transactions/report")
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


@router.get("/transactions/{t_id}")
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


@router.put("/transactions/{t_id}")
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


@router.delete("/transactions/{t_id}")
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
