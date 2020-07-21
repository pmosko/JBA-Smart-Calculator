while True:
    n = input().strip()
    if n:
        if n == '/exit':
            break
        print(sum(map(int, n.split())))
print('Bye!')