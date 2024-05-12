import ply.lex as lex
import re

tokens = (
    'NUM',
    'CR',
    'EMIT',
    'PRINT_S',
    'DOT',
    'DUP',
    'DEC_VAR',
    'ATRB_VAR',
    'USE_VAR',
    'DEC_WORD',
    'USE_WORD',
    'SWAP',
    'IF',
    'ELSE',
    'THEN',
    'SUP',
    'INF',
    'EQ',
    'INFEQ',
    'SUPEQ',
    'BEGIN',
    'UNTIL',
    'WHILE',
    'REPEAT',
    'AGAIN',
    'DROP',
    'LOOP',
    'PLUSLOOP',
    'DO',
    '2DUP',
)

literals = ['/','*','+','"','-',';']


def t_INFEQ(t):
    r'<='
    return t

def t_SUPEQ(t):
    r'>='
    return t

def t_SUP(t):
    r'>'
    return t

def t_INF(t):
    r'<'
    return t

def t_EQ(t):
    r'='
    return t

def t_DO(t):
    r'(?i:(DO))'
    return t

def t_PLUSLOOP(t):
    r'(?i:(\+LOOP))'
    return t

def t_LOOP(t):
    r'(?i:(LOOP))'
    return t

def t_DROP(t):
    r'(?i:(DROP))'
    return t

def t_BEGIN(t):
    r'(?i:(BEGIN))'
    return t

def t_UNTIL(t):
    r'(?i:(UNTIL))'
    return t

def t_WHILE(t):
    r'(?i:(WHILE))'
    return t

def t_REPEAT(t):
    r'(?i:(REPEAT))'
    return t

def t_AGAIN(t):
    r'(?i:(AGAIN))'
    return t

def t_IF(t):
    r'(?i:(IF))'
    return t

def t_ELSE(t):
    r'(?i:(ELSE))'
    return t

def t_THEN(t):
    r'(?i:(THEN))'
    return t

def t_2DUP(t):
    r'(?i:(2DUP))'
    return t

def t_CR(t):
    r'(?i:(cr))'
    return t

def t_EMIT(t):
    r'(?i:(EMIT))'
    return t

def t_DUP(t):
    r'(?i:(DUP))'
    return t

def t_SWAP(t):
    r'(?i:(SWAP))'
    return t

def t_DEC_WORD(t):
    r':\s\w+\w*\s\(\sn(\sn)*\s\)'
    return t

def t_PRINT_S(t):
    r'\.".*?"'
    return t

def t_ATRB_VAR(t):
    r'(([a-zA-Z]+\w*)?)\s!'
    return t

def t_USE_VAR(t):
    r'(([a-zA-Z]+\w*)?)\s@'
    return t

def t_DEC_VAR(t):
    r'VARIABLE(\s[a-zA-Z]+\w*)?'
    return t

def t_USE_WORD(t):
    r'([a-zA-Z]+\w*)'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

t_ignore = '\t\r\n '
t_ignore_COMMENT = r'\(.*?\)'

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







