# 総当たり法による列挙（自動生成データ）
from itertools import permutations
import random
import math
from pprint import pprint


# 人・職の数を自由に設定
n = 10
# 75~100のランダム値で適性の表を作る
aptitude = [[random.randint(75, 100) for _ in range(n)] for _ in range(n)]
pprint(aptitude)
print('試行回数{}回'.format(math.factorial(n)))

max_sum = 0
max_p = 0
for p in permutations(range(n), n):
    sum_ = 0
    for job, person in enumerate(p):
        sum_ += aptitude[job][person]
    if sum_ > max_sum:
        max_sum = sum_
        max_p = p

print(max_sum, max_p)
