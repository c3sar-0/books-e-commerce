for i in range(100):
    if i == 0 or i == 1:
        continue
    isPrime = True
    for j in range(i):
        if j == 0 or j == 1 or j == i:
            continue
        if i % j == 0:
            isPrime = False
            break
    if isPrime:
        print(i)
