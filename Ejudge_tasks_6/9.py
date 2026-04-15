a = int(input())
let = list(map(str, input().split()))
nums = list(map(str, input(). split()))
result = zip(let, nums)
a = 0
q = input()
for word, index in list(result):
        if word == q:
            print(index)
            a += 1
if a == 0:
    print("Not found")