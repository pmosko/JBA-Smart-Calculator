class CalcStore(dict):
    def evaluate(self, expr):
        if '=' in expr:
            try:
                left, right = expr.replace('=', ' ').split()
                if not left.isalpha():
                    return "Invalid identifier"
                if not right.isalpha() and not right.isdigit():
                    return "Invalid assignment"
                self[left] = eval(right, vars(self), self)
                return
            except ValueError:
                return "Invalid assignment"
            except NameError:
                return "Invalid identifier"
        else:
            try:
                return eval(expr, vars(self), self)
            except NameError:
                return "Unknown variable"


cs = CalcStore()
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
                ret = cs.evaluate(n)
                if ret is not None:
                    print(ret)
                #print("Invalid expression")
print('Bye!')