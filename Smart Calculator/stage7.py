from collections import namedtuple
import operator

OnpMap = namedtuple("OnpMap", "operator func weight")


class Stack(list):
    def push(self, *args):
        self.append(*args)


class ONP:
    onp_map = {
        '(': OnpMap('(', True, 0),
        '+': OnpMap('+', operator.add, 1),
        '-': OnpMap('-', operator.sub, 1),
        ')': OnpMap(')', False, 1),
        '*': OnpMap('*', operator.mul, 2),
        '/': OnpMap('/', operator.floordiv, 2),
        '%': OnpMap('%', operator.mod, 2),
        '^': OnpMap('^', operator.pow, 3),
    }

    @classmethod
    def postfix(cls, expr):
        stack = Stack()
        result = Stack()
        for op in expr:
            if op not in cls.onp_map:
                result.push(op)
                continue
            op_type = cls.onp_map[op]
            while True:
                if not stack:
                    stack.push(op_type)
                    break
                last = stack.pop()
                if not op_type.weight or op_type.weight > last.weight:
                    if isinstance(op_type.func, bool) and isinstance(last.func, bool):
                        break
                    stack.push(last)
                    stack.push(op_type)
                    break
                result.push(last)
        for op in reversed(stack):
            result.push(op)
        return result


    @staticmethod
    def print_stack(stack):
        print(' '.join(str(op) if not isinstance(op, OnpMap) else op.operator for op in stack))


class Calc(ONP, dict):
    def calc(self, stack):
        result = Stack()
        for op in stack:
            if isinstance(op, str):
                try:
                    result.push(int(eval(op, vars(self), self)))
                except NameError:
                    raise ValueError("Unknown variable")
            elif isinstance(op, int):
                result.push(op)
            else:
                a, b = result.pop(), result.pop()
                result.push(op.func(b, a))
        return result.pop()

    def evaluate_assignment(self, input_):
        if input_.count('=') > 1:
            raise ValueError("Invalid assignment")
        try:
            left, right = input_.replace('=', ' ').split()
            if not left.isalpha():
                raise ValueError("Invalid identifier")
            self[left] = eval(right, vars(self), self)
        except ValueError:
            raise ValueError("Invalid assignment")
        except NameError:
            raise ValueError("Unknown variable")


def sanitize_operator(operator_):
    operators = ('+', '-', '*', '/', '^', '(', ')')
    ops = {op: operator_.count(op) for op in operators}
    if ops['*'] > 1 or ops['/'] > 1 or ops['/'] > 1:
        raise ValueError('Invalid expression')
    if ops['-'] > 0:
        return '-' if ops['-'] % 2 == 1 else '+'
    return operator_[0] if operator_[0] in operators else operator_


def split_input(input_):
    if not input_:
        return
    _input = input_.replace('(', ' ( ').replace(')', ' ) ').split()
    result = Stack()
    for input_ in _input:
        try:
            result.push(str(int(input_)))
        except ValueError:
            isnum = input_[0].isalnum()
            isspace = True
            tmp = Stack()
            for c in input_:
                if c.isalnum() == isnum and not c.isspace():
                    tmp.push(c)
                else:
                    result.push(''.join(tmp))
                    tmp = Stack([c])
                    isnum = c.isalnum()
            else:
                result.push(''.join(tmp))
    return list(filter(None, map(str.strip, result)))


def sanitize_input(input_):
    if input_.count('(') != input_.count(')'):
        raise ValueError('Invalid expression')

    input_ = split_input(input_)
    result = Stack()
    for i in input_:
        try:
            result.push(int(i))
        except ValueError:
            result.push(sanitize_operator(i))
    return result


def print_help():
    print('Program help')


def exit_application():
    print('Bye!')
    raise SystemExit


def parse_commands(input_):
    cmd_map = {
        '/help': print_help,
        '/exit': exit_application
    }
    try:
        cmd_map[input_]()
    except KeyError:
        raise ValueError('Unknown command')


calc = Calc()
while True:
    try:
        input_ = input().strip()
        if input_:
            if input_.startswith('/'):
                parse_commands(input_)
            elif '=' in input_:
                calc.evaluate_assignment(input_)
            else:
                sane_input = sanitize_input(input_)
                print(calc.calc(calc.postfix(sane_input)))
    except SystemExit:
        break
    except ValueError as e:
        print(e.args[0])

