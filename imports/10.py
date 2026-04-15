import random
print(random.random())
print(random.randrange(0, 20, 2))
print(random.uniform(1, 5))
names = ["Nurda", "Miras", "Roma", "Tima"]
print(random.choice(names))
for i in dir(random):
    if not i.startswith("_"):
        print(i)
random.seed(1)
print(random.randint(20, 30))
print(random.randint(20, 30))