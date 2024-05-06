import sys
import ply.yacc as yacc
import arvore
from forth2vm_lex import tokens

"""
VM : instructions

instructions : instructions instruction
             | instruction

instruction : NUM
            | SINAL
            | WORD

WORD : WORD_EXEC
     | WORD_DEC

WORD_EXEC : DOT
          | PRINT_S
          | EMIT
          | CR
          | DUP
          | USE_VAR

WORD_DEC : DEC_WORD
         | ATRB_VAR
         | DEC_VAR

SINAL : '+'
      | '-'
      | '*' 
      | '/'
"""


def p_VM(p):
    """VM : instructions"""
    p[0] = arvore.ProgramNode(p[1])

def p_instructions(p):
    """instructions : instructions instruction"""
    p[0] = p[1] + [p[2]] 

def p_instructions_single(p):
    """instructions : instruction"""
    p[0] = [p[1]]

def p_instruction1(p):
    """instruction : NUM"""
    p[0] = arvore.NumberNode(p[1]) 

def p_instruction2(p):
    """instruction : WORD"""
    p[0] = p[1]

def p_WORD(p):
    """WORD : WORD_EXEC
            | WORD_DEC"""
    p[0] = p[1]

def p_WORD_EXEC(p):
    """WORD_EXEC : DOT
                 | PRINT_S
                 | EMIT
                 | CR
                 | DUP
                 | USE_VAR
                 | USE_WORD"""
    print(p[1])
    p[0] = arvore.WordNodeExec(p[1])

def p_WORD_DEC(p):
    """WORD_DEC : DEC_WORD
                | ATRB_VAR
                | DEC_VAR"""
    p[0] = arvore.WordNodeDec(p[1])


def p_instruction3(p):
    """instruction : SINAL"""
    p[0] = p[1]

def p_SINAL(p):
    """SINAL : '+'
             | '-'
             | '*'
             | '/'"""
    p[0] = arvore.SignalNode(p[1])

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

###################################

def read_input_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

# Lendo o conteúdo do arquivo
data = read_input_file('input.txt')

parser = yacc.yacc()
parser.exito = True

ast = parser.parse(data)  # O parser retorna a raiz da AST

#print(ast)  # Imprime a AST

# fazer a travessia na arvore
print(ast.generate_code())  # Gera o código da AST
arvore.ProgramNode.print_lista_variaveis()  # Imprime a lista de variáveis



