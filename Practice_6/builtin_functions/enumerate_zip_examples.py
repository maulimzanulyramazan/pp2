names = ["Ali", "Aruzhan", "Dias"]
scores = [85, 90, 78]

# enumerate
print("Using enumerate:")
for index, name in enumerate(names, start=1):
    print(index, name)

# zip
print("\nUsing zip:")
for name, score in zip(names, scores):
    print(name, score)