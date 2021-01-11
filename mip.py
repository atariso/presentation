import time

from ortools.linear_solver import pywraplp
import pandas as pd

cost_limit = 2000  # 一日何円までか
protein_lower_limit = 120  # タンパク質の摂取目標
fat_lower_limit = 50  # 脂質の摂取目標
calorie_limit = 1500  # カロリー制限
repeat_limit = 3  # 同じものを一日何度まで食べるか

df = pd.read_csv('meal.csv')
names = df.name
cost = df.yen
protein = df.P
fat = df.F
carbohydrate = df.C
calorie = df.cal
satisfaction = df.satisfaction  # 独断と偏見で決めた満足度

# 食事候補の数
meal_num = len(df)

solver = pywraplp.Solver.CreateSolver('SCIP')
x = {}
for i in range(meal_num):
    # 一日三食
    for j in range(3):
        x[i, j] = solver.IntVar(0, 1, '')

# 一日の食事代の合計に関する制約
solver.Add(solver.Sum([x[i, j] * cost[i] for i in range(meal_num) for j in range(3)]) <= cost_limit)

# 一日のタンパク質摂取量に関する制約
solver.Add(solver.Sum([x[i, j] * protein[i] for i in range(meal_num) for j in range(3)]) >= protein_lower_limit)

# 一日の脂質摂取量に関する制約
solver.Add(solver.Sum([x[i, j] * fat[i] for i in range(meal_num) for j in range(3)]) >= fat_lower_limit)

# 一日のカロリーに関する制約
solver.Add(solver.Sum([x[i, j] * calorie[i] for i in range(meal_num) for j in range(3)]) <= calorie_limit)

# 任意の食材は一日に1度までしか食べられない（飽きるので）
for i in range(meal_num):
    solver.Add(solver.Sum([x[i, j] for j in range(3)]) <= repeat_limit)

# 任意の食事は300kcal以上を摂取する（腹が減るので）
for j in range(3):
    solver.Add(solver.Sum([x[i, j] * calorie[i] for i in range(meal_num)]) >= 300)

solver.Maximize(solver.Sum([satisfaction[i] * x[i, j] for i in range(meal_num) for j in range(3)]))

start = time.time()
sol = solver.Solve()

p, f, c, cal = 0, 0, 0, 0

print('最大満足度 = {}'.format(int(solver.Objective().Value())))
for j in range(3):
    meal_name = '朝食'
    if j == 1:
        meal_name = '昼食'
    elif j == 2:
        meal_name = '夕食'
    print('======== ' + meal_name + ' ========')
    for i in range(meal_num):
        if x[i, j].solution_value() > 0:
            print('Meal', i, '  Name = ', names[i])
            p += protein[i]
            f += fat[i]
            c += carbohydrate[i]
            cal += calorie[i]
print()
print('摂取した栄養素')
print('protein:{:.2f} [g], fat:{:.2f} [g], carbo:{:.2f} [g], cal:{:.2f} [kcal]'.format(p, f, c, cal))
end = time.time()
print()
print("Time = ", round(end - start, 4), "seconds")
