class SecureAccount:
    bank_name="Pythonic Central Bank"
    def __init__(self,account_no,initial_balance=0.0):
        self.account_no=account_no
        self.__balance=initial_balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self,amount):
        if amount <= 0:
            raise ValueError("存款金额必须大于 0！")
        else:
            self.__balance += amount
            print(f"存款成功。")
    def withdraw(self,amount):
        if amount <= 0:
            raise ValueError('取款金额必须大于 0！')
        elif amount > self.__balance:
            raise ArithmeticError("账户余额不足!")
        else:
            self.__balance-=amount
            print(f"取款成功，卡里余额剩余{self.__balance}。")

    @classmethod
    def from_csv_line(cls,line):
        account_no,initial_balance=line.split(',')
        return cls(account_no,float(initial_balance))#注意float，不然就是字符串了

if __name__=="__main__":
    acc=SecureAccount.from_csv_line("ACC0001,1000002.0")
    print(acc.balance)
    acc.deposit(200)
    try:
        acc.withdraw(100)
        acc.withdraw(100000000)
    except (ValueError,LookupError,ArithmeticError) as e:
        print(e)
