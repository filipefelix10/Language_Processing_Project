import ply.lex as lex
import re

tokens = (
    'NUM',
    'ID',
    'VARIABLE',
    'CR',
    'EMIT',
    'PRINT_S',
    'DOT',
    'DUP',
    'DEC_VAR',
    'USE_VAR',
)

literals = [';','/','*','+','"','-','(',')','=','<','>']

def t_CR(t):
    r'(?i:(cr))'
    return t

def t_EMIT(t):
    r'(?i:(EMIT))'
    return t

def t_DUP(t):
    r'(?i:(DUP))'
    return t

def t_DEC_VAR(t):
    r'(([a-zA-Z]+\w*)?)\s!'
    return t

def t_USE_VAR(t):
    r'(([a-zA-Z]+\w*)?)\s@'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VARIABLE(t):
    r'VARIABLE(\s[a-zA-Z]+\w*)?'
    return t

def t_PRINT_S(t):
    r'\." [a-zA-Z0-9_ ]*"'
    #remover o poonto e as aspas
    t.value = t.value[2:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

t_ignore = '\t\r\n '

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Ilegal: {t.value[0]} na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def read_input_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

# Lendo o conteúdo do arquivo
data = read_input_file('input.txt')


lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
print("Fim da análise léxica.\n")







