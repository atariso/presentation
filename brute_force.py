# 総当たり法による列挙
from itertools import permutations

aptitude = [[97, 99, 96, 77, 77],
            [81, 83, 91, 97, 89],
            [95, 79, 87, 91, 84],
            [96, 88, 82, 86, 79],
            [92, 92, 78, 93, 84]]

max_sum = 0
max_p = 0
for p in permutations(range(5), 5):
    sum_ = 0
    for job, person in enumerate(p):
        sum_ += aptitude[job][person]
    if sum_ > max_sum:
        max_sum = sum_
        max_p = p

print(max_sum, max_p)
# 465 (2, 3, 4, 0, 1)
