import sys
import ply.yacc as yacc
import arvore
from forth2vm_lex import tokens

global if_count
if_count = 1
n_pushi = 0

"""
VM : instructions

instructions : instructions instruction
             | instruction

instruction : NUM
            | SINAL
            | WORD
            | CONDITION
            | LOOPs

LOOPs : BEGIN instructions UNTIL
     | BEGIN instructions AGAIN
     | BEGIN instructions WHILE instructions REPEAT            
     | DO instructions LOOP
     | DO instructions +LOOP   

CONDITION : COND1
          | COND2

WORD : WORD_EXEC
     | WORD_DEC

WORD_EXEC : DOT
          | PRINT_S
          | EMIT
          | CR
          | DUP
          | SWAP
          | USE_VAR

WORD_DEC : DEC_WORD
         | ATRB_VAR
         | DEC_VAR

SINAL : '+'
      | '-'
      | '*' 
      | '/'
      | INF
      | SUP
      | INFEQ
      | SUPEQ
"""


def p_VM(p):
    """VM : instructions"""
    global n_pushi
    p[0] = arvore.ProgramNode(p[1],n_pushi)

def p_instructions(p):
    """instructions : instructions instruction"""
    p[0] = p[1] + [p[2]] 

def p_instructions_single(p):
    """instructions : instruction"""
    p[0] = [p[1]]

def p_instruction(p):
    """instruction : CONDITION"""
    p[0] = p[1]        

def p_instruction2(p):
    """instruction : WORD"""
    p[0] = p[1]

def p_instruction3(p):
    """instruction : NUM"""
    p[0] = arvore.NumberNode(p[1]) 

def p_instruction4(p):
    """instruction : SINAL"""
    p[0] = p[1]

def p_instruction5(p):
    """instruction : LOOPTYPE"""
    p[0] = p[1]

def p_LOOP(p):
    """LOOPTYPE : BEGIN instructions UNTIL"""
    global if_count
    p[0] = arvore.LoopNodeUntil(p[2],if_count)
    if_count += 1
    
def p_LOOP2(p):
    """LOOPTYPE : BEGIN instructions AGAIN"""
    global if_count
    p[0] = arvore.LoopNodeAgain(p[2],if_count)
    if_count += 1

def p_LOOP3(p):
    """LOOPTYPE : BEGIN instructions WHILE instructions REPEAT"""
    global if_count
    p[0] = arvore.LoopNodeWhile(p[2],if_count,p[4])
    if_count += 1

def p_LOOP4(p):
    """LOOPTYPE : DO instructions LOOP"""
    global if_count,n_pushi
    p[0] = arvore.LoopNodeDO(p[2],if_count,n_pushi,False)
    if_count += 1
    n_pushi += 2

def p_LOOP5(p):
    """LOOPTYPE : DO instructions PLUSLOOP"""
    global if_count, n_pushi
    p[0] = arvore.LoopNodeDO(p[2],if_count,n_pushi,True)
    if_count += 1
    n_pushi += 2

def p_CONDITION(p):
    """CONDITION : IF instructions ELSE instructions THEN """
    global if_count
    p[0] = arvore.ConditionNode(p[2],if_count,p[4])
    if_count += 1


def p_CONDITION2(p):
    """CONDITION : IF instructions THEN"""
    global if_count
    p[0] = arvore.ConditionNode(p[2],if_count)
    if_count += 1

def p_WORD(p):
    """WORD : WORD_EXEC
            | WORD_DEC"""
    p[0] = p[1]

def p_WORD_EXEC(p):
    """WORD_EXEC : PRINT_S
                 | DOT
                 | EMIT
                 | CR
                 | DUP
                 | 2DUP
                 | SWAP
                 | DROP
                 | USE_VAR
                 | USE_WORD"""
    p[0] = arvore.WordNodeExec(p[1])

def p_WORD_DEC(p):
    """WORD_DEC : DEC_WORD instructions ';' """     
    global n_pushi
    p[0] = arvore.WordNodeDec(p[1],n_pushi,p[2])

def p_WORD_DEC1(p):
    """ WORD_DEC : ATRB_VAR """
    global n_pushi
    p[0] = arvore.WordNodeDec(p[1],n_pushi)


def p_WORD_DEC2(p):
    """WORD_DEC : DEC_VAR"""
    global n_pushi
    p[0] = arvore.WordNodeDec(p[1],n_pushi)
    n_pushi += 1

def p_SINAL(p):
    """SINAL : '+'
             | '-'
             | '*'
             | '/'
             | INF
             | SUP
             | INFEQ
             | SUPEQ
             | EQ"""
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

# Lê o ficheiro de entrada
data = read_input_file('input.txt')

parser = yacc.yacc()
parser.exito = True
parser.count_ciclos = 0

ast = parser.parse(data)  # O parser retorna a raiz da AST

def write_output_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

write_output_file('output.txt', ast.generate_code())  # Gera o código da AST

# fazer a travessia na arvore
#print(ast.generate_code())  # Gera o código da AST
print("Fim da análise sintática.\n")



