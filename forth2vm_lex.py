import ply.lex as lex

tokens = (
    'NUM',
    'ID',
    'VARIABLE',
    'CR',
    'EMIT',
    'PRINT_S',
    'DOT',
)

literals = [';','/','*','+','"','-','(',')','=','!']

def t_PRINT_S(t):
    r'\." [a-zA-Z0-9_ ]*"'
    #remover o poonto e as aspas
    t.value = t.value[2:-1]
    return t

def t_VARIABLE(t):
    r'VARIABLE'
    return t

def t_EMIT(t):
    r'EMIT'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_CR(t):
    r'CR'
    return t

t_ignore = '\t\r\n '

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Ilegal: {t.value[0]} na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# Test your lexer
data ="""
2 2 +
3 3 *
4 4 /
5 5 -
"""

"""
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
"""




