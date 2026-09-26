def validate_password(password):


    if len(password) < 8:

        raise ValueError("密码的位数必须大于等于8")
    sign1 = any(char.isdigit() for char in password)
    sign2 = any(char.isupper() for char in password)
    if not sign1 or not sign2:

        raise ValueError("必须同时包括大写于数字")
    return True



if __name__ == "__main__":
    print("--- security_util 单元测试 ---")
    test_cases = [
        ("Wang123456", "合法密码"),
        ("123456", "长度不足"),
        ("qwertyuiop", "缺少大写和数字"),
        ("QWERTYUIOP", "缺少数字"),
        ("Valid123", "合法密码")
    ]
    for pwd,desc in test_cases:
        try:
            validate_password(pwd)
            print(f"[通过] 用例 '{desc}' ({pwd}) 校验成功")
        except ValueError as e:
            print(f"[拦截] 用例 '{desc}' ({pwd}) 成功拦截: {e}")

