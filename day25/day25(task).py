from abc import  ABC,abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send_notification(self,target:str,content:str):
        pass

class EmailNotifier(Notifier):
    def send_notification(self,target:str,content:str):
        print(f"[邮件发送] 收件人: {target} | 内容: {content}")
class SMSNotifier(Notifier):
    def send_notification(self,target:str,content:str):
        print(f"[短信推送] 手机号: {target} | 内容: {content}")
class DingTalkNotifier(Notifier):
    def send_notification(self,target:str,content:str):
        print(f"[钉钉机器人] Webhook 群: {target} | 内容: {content}")
class faultNotifier(Notifier):
    # def send_notification(self,target:str,content:str):
        print(f"xiaoguoruhe")



def broadcast_message(notifiers:list,targets_and_messages:list):
    for notifier in notifiers:
        for target, message in targets_and_messages:
            notifier.send_notification(target,message)#列表元组




targets_and_messages_list=[("user@test.com", "系统维护提醒"), ("13800000000", "验证码是 1234")]
notifiers=[EmailNotifier(),SMSNotifier(),DingTalkNotifier(),faultNotifier()]
broadcast_message(notifiers,targets_and_messages_list)

