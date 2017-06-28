from queue import Queue
import re


class Token:
    LEFT_BLACKETS = 'LEFT_BLACKETS'
    RIGHT_BLACKETS = 'RIGHT_BLACKETS'
    SYMBOL = 'SYMBOL'
    EXPRESSION = 'EXPRESSION'
    SYMBOLS = '&|!'

    def __init__(self, value, types):
        self.value = value
        self.types = types

    def __str__(self):
        return '{0}<{1}>'.format(self.value, self.types)

    def __repr__(self):
        return self.__str__()


# produce an expression with tokens
def tokenize(origin):
    tokens = []
    is_expr = False
    expr = []
    for c in origin:
        if c == '#':
            if not is_expr:
                is_expr = True
            else:
                is_expr = False
                token = Token(''.join(expr), Token.EXPRESSION)
                tokens.append(token)
                expr = []
        elif c in Token.SYMBOLS and not is_expr:
            token = Token(c, Token.SYMBOL)
            tokens.append(token)
        elif c == '(' and not is_expr:
            token = Token(c, Token.LEFT_BLACKETS)
            tokens.append(token)
        elif c == ')' and not is_expr:
            token = Token(c, Token.RIGHT_BLACKETS)
            tokens.append(token)
        elif is_expr:
            expr.append(c)
    return tokens


class ASTree:
    def __init__(self, token):
        self.root = token
        self.left = None
        self.right = None

    def visit(self):
        ret = []
        q = Queue()
        q.put(self)
        while not q.empty():
            t = q.get()
            ret.append(t.root)
            if t.left:
                q.put(t.left)
            if t.right:
                q .put(t.right)
        return ret


def make_sub_ast(stack, tree):
    current = tree
    while stack and stack[-1].root.types == 'SYMBOL':
        node = stack.pop()
        if node.root.value == '!' and not node.right:
            node.right = current
            if stack[-1].root.types != 'LEFT_BLACKETS':
                raise Exception('{0} is not the expected type{1}'.format(stack[-1].root.value, Token.LEFT_BLACKETS))
        else:
            if not stack[-1]:
                raise Exception('')
            node.right = current
            node.left = stack.pop()
        current = node
    return stack.append(current)


# transform the expression with tokens into astree
def make_ast(token):
    stack = []
    for t in token:
        tree = ASTree(t)
        if tree.root.types == 'LEFT_BLACKETS' or tree.root.types == 'SYMBOL':
            stack.append(tree)
        elif tree.root.types == 'EXPRESSION':
            make_sub_ast(stack, tree)
        elif tree.root.types == 'RIGHT_BLACKETS':
            r = stack.pop()
            if stack[-1] and stack[-1].root.types == 'LEFT_BLACKETS':
                stack.pop()
                make_sub_ast(stack, r)
            else:
                raise Exception('a')
        else:
            raise Exception('')
    return stack.pop()


def cacl(ast, line):
    if ast.root.types != Token.EXPRESSION:
        if ast.root.value == '!':
            return not cacl(ast.right, line)
        elif ast.root.value == '|':
            return cacl(ast.left, line) or cacl(ast.right, line)
        elif ast.root.value == '&':
            return cacl(ast.left, line) and cacl(ast.right, line)
    else:
        return re.search(ast.root.value, line) is not None


class Matcher:
    def __init__(self, name, origin):
        self.name = name
        self.origin = origin
        self.ast = make_ast(tokenize(origin))

    def match(self, line):
        return cacl(self.ast, line)


if __name__ == '__main__':
    e = '#test# & #abc# | (!#123# | #456#)'
    line = 'test cdf 123 568'

    m = Matcher(e)
    print(m.match(line))