while True:
    n = input().strip()
    if n:
        if n == '/exit':
            break
        elif n == '/help':
            print('The program calculates the operations on numbers')
        elif n.startswith('/'):
            print('Unknown command')
        else:
            try:
                print(eval(n))
            except (SyntaxError, NameError):
                print("Invalid expression")
print('Bye!')