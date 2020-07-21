def eval_op(op):
    if op[-1] == '-':
        return '-' if len(op) % 2 == 1 else '+'
    else:
        return op[-1]


while True:
    n = input().strip()
    if n:
        if n == '/exit':
            break
        elif n == '/help':
            print('The program calculates the operations on numbers')
        else:
            ops = [s if s[-1].isdigit() else eval_op(s) for s in n.split()]
            print(eval(' '.join(ops)))
print('Bye!')