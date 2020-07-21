while True:
    n = input().strip()
    if n:
        if n == '/exit':
            break
        elif n == '/help':
            print('The program calculates the sum of numbers')
        else:
            print(sum(map(int, n.split())))
print('Bye!')