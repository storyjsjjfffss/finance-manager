def transfer_money(user,from_id,to_id,amount):
    try:
        sign_from=None
        sign_to=None
        for u in user:
            if u['id']==from_id:
                sign_from=True;
        for u in user:
            if u['id']==to_id:
                sign_to=True;

        if amount<=0:
            raise ValueError("Amount must be greater than zero")
        elif not sign_from or not sign_to:
            raise LookupError("User and user ids do not match")
        elif next(u for u in user if u["id"]==from_id)["balance"]<amount:
            raise ArithmeticError("付款方余额不足！")
        else:
            for u in user:
                if u["id"]==to_id:
                    u["balance"]+=amount
                if u['id']==from_id:
                    u["balance"]-=amount
    except ValueError:
        print("输入有问题")
    else:
        print('交易成功')
        print(user)

users = [
    {"id": 1, "name": "Alex", "balance": 150.0},
    {"id": 2, "name": "Bob",  "balance": 50.0},
    {"id": 3, "name": "Kasai","balance": 0.0}
]

transfer_money(users,1,2,100)

#下面的才是对的，上面太麻烦
def transfer_money(users, from_id, to_id, amount):
    """
    执行转账业务逻辑
    若校验不通过，直接向上抛出对应异常，交由上层调用方捕获
    """
    # 1. 校验金额
    if amount <= 0:
        raise ValueError("转账金额必须大于 0！")

    # 2. 一次遍历定位转账双方的对象引用
    sender = None
    receiver = None
    for u in users:
        if u["id"] == from_id:
            sender = u
        elif u["id"] == to_id:
            receiver = u

    # 3. 校验用户是否存在
    if sender is None or receiver is None:
        raise LookupError("付款方或收款方账户不存在！")

    # 4. 校验余额是否充足
    if sender["balance"] < amount:
        raise ArithmeticError(f"付款方余额不足！当前余额: {sender['balance']:.2f}, 转账金额: {amount:.2f}")

    # 5. 校验通过，原子扣减与增加
    sender["balance"] -= amount
    receiver["balance"] += amount

users = [
    {"id": 1, "name": "Alex", "balance": 150.0},
    {"id": 2, "name": "Bob",  "balance": 50.0},
    {"id": 3, "name": "Kasai","balance": 0.0}
]

def execute_transfer_test(users, from_id, to_id, amount):
    print(f"\n[开始转账] 尝试从用户 {from_id} 转账 {amount} 元至用户 {to_id}...")
    try:
        transfer_money(users, from_id, to_id, amount)
    except ValueError as e:
        print(f"❌ 参数错误拦截: {e}")
    except LookupError as e:
        print(f"❌ 账户查询异常: {e}")
    except ArithmeticError as e:
        print(f"❌ 资金结算异常: {e}")
    else:
        print("✅ 交易成功！当前用户列表:")
        for u in users:
            print(f"   - {u['name']} (ID: {u['id']}): ¥{u['balance']:.2f}")

# 测试 1: 正常转账（Alex 转 100 给 Bob）
execute_transfer_test(users, from_id=1, to_id=2, amount=100.0)

# 测试 2: 余额不足（Alex 仅剩 50，再转 100）
execute_transfer_test(users, from_id=1, to_id=2, amount=100.0)

# 测试 3: 金额非法（金额为负数）
execute_transfer_test(users, from_id=2, to_id=1, amount=-20.0)

# 测试 4: 账户不存在（用户 ID 999 不存在）
execute_transfer_test(users, from_id=999, to_id=1, amount=10.0)