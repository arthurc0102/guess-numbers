import random
import string

from itertools import permutations

NUMBER_LENGTH = 4


def compare(guess_number, answer_number):  # 根據猜的數字跟答案返回幾 A 幾 B
    a = b = 0

    for i, j in zip(guess_number, answer_number):
        if i == j:
            a += 1
        elif i in answer_number:
            b += 1

    return a, b


# 建立可能性答案
# 列出排列：P10 取 4 共 5040 種可能 (10! / (10 - 4)!) = 5040
possible_answers = list(permutations(string.digits, NUMBER_LENGTH))
possible_answers = [''.join(ans) for ans in possible_answers]

# 猜了幾次
guess_count = 0

# 開始猜測
while True:
    guess_number = random.choice(possible_answers)

    print(f'電腦猜：{guess_number}')
    guess_count += 1

    guess_result = input('猜測結果：')
    a, b = guess_result[:3:2]  # 取得幾 A 幾 B（從 0 開始取到 2 (3 - 1) 間隔為 2
    a, b = int(a), int(b)  # 轉成數字

    if a == NUMBER_LENGTH:
        print()
        print(f"猜對了！共猜了 {guess_count} 次")
        break

    new_possible_answers = []  # 取得有可能的答案，淘汰不可能出現結果的數字（不可能出現那個數量的 A 跟 B）
    for possible_answer in possible_answers:
        if guess_number == possible_answer:  # 跳過這次猜的這個（因為不可能是答案，不用浪費時間比對）
            continue

        if (a, b) != compare(guess_number, possible_answer):
            continue

        new_possible_answers.append(possible_answer)

    print()
    print(f'原本共有 {len(possible_answers)} 個可能的數字')
    print(f'猜了 {guess_number} 後得到 {guess_result} 的結果')
    print(f'經比對排除 {len(possible_answers) - len(new_possible_answers)} 個')
    print(f'剩餘 {len(new_possible_answers)} 個。')
    print()

    possible_answers = new_possible_answers  # 更新 possible_answers 讓下次迴圈從新的可能當中挑
