# import random
# secret = random.randint(1,100)
# count=0
#
# while True:
#     guess = int(input("Guess a number(0-100）: "))
#     count +=1;
#     if guess==secret:
#         print("You guessed right!\n",f"你用了{count}次")
#         break
#     elif guess<secret:
#         print("你输入的数字太小了")
#     else:
#         print("你输入的数字太大了")
# 比较数字

#猜数字的挑战
import random
secret = random.randint(1,50)
count=0
while True:
    guess=int(input("Guess a number between 1 and 50: "))
    count+=1

    if guess == secret:
        print("Correct!")
        break
    elif guess > secret:
        print("Too high!")
    elif guess < secret:
        print("Too low!")

    if count==6:
        print("You lose!")
        break

# import random
# GEMINI提供的代码
# secret = random.randint(1, 50)
# total_attempts = 6
#
# for attempt in range(1, total_attempts + 1):
#     guess = int(input(f"第 {attempt} 次尝试（剩余 {total_attempts - attempt} 次），请输入数字: "))
#
#     if guess == secret:
#         print(f"恭喜！你在第 {attempt} 次猜中了！")
#         break
#     elif guess > secret:
#         print("太大了！")
#     else:
#         print("太小了！")
# else:
#     # 只有当 6 次循环完整走完且没有 break 时，才会执行这里
#     print(f"遗憾，机会已耗尽！正确答案是: {secret}")