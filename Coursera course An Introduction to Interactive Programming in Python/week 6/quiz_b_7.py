n = 1000
numbers = range(2,n)
results = []

while len(numbers) != 0:
    results.append(numbers[0])
    for i in numbers:
        if i % numbers[0] == 0:
            numbers.pop(numbers.index(i))

print len(results)
    