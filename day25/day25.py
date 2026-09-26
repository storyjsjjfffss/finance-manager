from abc import ABC, abstractmethod

# 1. 定义抽象基类（接口规范）
class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount: float):
        """支付行为规范"""
        pass


# 2. 两个具体的支付实现类
class AliPay(PaymentGateway):
    def pay(self, amount: float):
        print(f"[支付宝] 成功扣款 ¥{amount:.2f}")

class WechatPay(PaymentGateway):
    def pay(self, amount: float):
        print(f"[微信支付] 成功扣款 ¥{amount:.2f}")


# 3. 业务消费方：只认接口，不关心具体是哪种支付渠道
def checkout(gateway: PaymentGateway, total_price: float):
    print("--- 正在发起结算 ---")
    gateway.pay(total_price)


# 实例化调用
checkout(AliPay(), 199.0)
checkout(WechatPay(), 88.5)