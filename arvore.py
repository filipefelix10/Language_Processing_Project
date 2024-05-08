import re


global n_pushi, dict_var, dict_vars
n_pushi = 0
dict_var = []
dict_vars = {}


class ASTNode:
    def __init__(self) -> None:
        pass

    def generate_code(self):
        return ""
    
    def __str__(self):
        return self.print_tree()

    def print_tree(self, depth=0):
        indent = '  ' * depth
        tree_str = indent + self.__class__.__name__ + '\n'
        for attr, value in self.__dict__.items():
            if isinstance(value, ASTNode):
                tree_str += value.print_tree(depth + 1)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        tree_str += item.print_tree(depth + 1)
                    else:
                        tree_str += indent + '  ' + str(item) + '\n'
            else:
                tree_str += indent + '  ' + str(attr) + ': ' + str(value) + '\n'
        return tree_str


class ProgramNode(ASTNode):
    def __init__(self, instructions):
        self.instructions = instructions

    def generate_code(self):
        code = "start\n"
        for instruction in self.instructions:
            code += instruction.generate_code() # gera codigo do programa
        if (n_pushi > 0 ):
            code = "pushn " + str(n_pushi) + "\n" + code
        code = code + "stop\n\n"
        for func in dict_vars:
            if dict_vars[func]["tipo"] == "FUNC":
                code += dict_vars[func]["instrucoes"]
        return code
    
    def print_lista_variaveis():
        print("VARIAVEIS NO DICT:")
        for key,value in dict_vars.items():
            print(f"key : \n  {key}")
            print("Value :")
            for key2,value2 in value.items():
                print("  "+key2, ":", value2)

    def get_dict_vars():
        return dict_vars
    

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def generate_code(self):
        return "pushi " + str(self.value) + "\n"


class SignalNode(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def generate_code(self):
        match self.value:
            case '+': res = 'add'
            case '-': res = 'sub'
            case '*': res = 'mul'
            case '/': res = 'div'
            case '>': res = 'sup'
            case '<': res = 'inf'
            case '<=': res = 'infeq'
            case '>=': res = 'supeq'
        return res + "\n"


class WordNodeExec(ASTNode):
    def __init__(self, value):
        self.value = value

    def generate_code(self):
        global n_pushi, dict_var, dict_vars
        print_s = self.value.split(".")
        valor = self.value.split(" ")
        match valor[0].upper():
            case '.': res = 'writei\n' + 'pushs " "\n' + 'writes'
            case 'EMIT': res = 'writechr'
            case 'CR': res = 'writeln'
            case 'DUP': res = 'dup 1'
            case 'SWAP': res = 'swap'
            case _ if len(valor) == 1:
                    if valor[0] in dict_vars:
                        res = "pusha " + str(valor[0]) + "\n" + "call\n"
                    else: res = ""
            case _ if len(valor) > 1:
                    if(len(print_s)) > 1: print_s = re.sub(r"(^'|'$)", "", print_s[1])
                    print(print_s)
                    if valor[0] in dict_vars and valor[1] == "@":
                        posicao = dict_vars[valor[0]]["pos"]
                        res = "pushg " + str(posicao)
                    elif re.match(r'(\.)?"\s(\w+\s*)*"', print_s):
                        res = 'pushs ' + print_s + "\n" + "writes" + "\n"
                    else: res = ""
        return res + "\n"
    

class WordNodeDec(ASTNode):
    def __init__(self, value):
        self.value = value

    def generate_code(self):
        global n_pushi, dict_var, dict_vars
        valor = self.value.split(" ")
        print(valor)
        match valor[0]:
            case 'VARIABLE':
                if len(valor) > 1:
                    dict_temp = {"tipo": "VARIABLE", "pos": n_pushi}
                    dict_var.append(dict_temp)
                    dict_vars[valor[1]] = dict_temp
                    n_pushi += 1
                res = ""
            case _ if len(valor) > 1:
                    if valor[0] in dict_vars and valor[1] == "!":
                        posicao = dict_vars[valor[0]]["pos"]
                        res = "storeg " + str(posicao)
                    elif valor[0] == ":":
                        dict_temp = {"tipo": "FUNC", "pos": n_pushi, "instrucoes": get_intrucoes(valor)}
                        dict_var.append(dict_temp)
                        dict_vars[valor[1]] = dict_temp
                        res = ""
                    else: res = ""
        return res + "\n"


class ConditionNode(ASTNode):
    def __init__(self, condition1, if_count, condition2=None):
        self.condition1 = condition1
        self.condition2 = condition2
        self.if_count = if_count
    
    def generate_code(self):
        code = "jz else" + str(self.if_count) + "\n"
        for i in self.condition1:
            code += i.generate_code()
        code += "jump endif" + str(self.if_count) + "\n"
        code += "else" + str(self.if_count) + ":\n"
        for i in self.condition2:
            code += i.generate_code()
        code += "endif" + str(self.if_count) + ":\n"

        return code



def get_intrucoes(valor):
    instr = valor[1] + ":\n"
    valor = " ".join(valor)
    valor = valor.split(")")
    list_n = valor[0].split("(")[1].split(" ")
    n_numbers = list_n.count("n")
    valor = valor[1].split(" ")

    for n in range(0,n_numbers):
        instr += "pushfp\n" + "load " + str(-1-n) + "\n"

    for i in range(0,len(valor)-1):
        match valor[i].upper():
            case '.': 
                instr += 'writei\n' + 'pushs " "\n' + 'writes\n'
            case 'PRINT_S':
                instr += 'writes\n'
            case 'EMIT':
                instr += 'writeln\n'
            case 'CR':
                instr += 'writeln\n'
            case 'DUP':
                instr += 'dup 1\n'
            case 'SWAP':
                instr += 'swap\n'
            case '+':
                instr += 'add\n'
            case '-':
                instr += 'sub\n'
            case '*':
                instr += 'mul\n'
            case '/':
                instr += 'div\n'
            case '>':
                instr += 'sup\n'
            case '<':
                instr += 'inf\n'
            case '<=':
                instr += 'infeq\n'
            case '>=':
                instr += 'supeq\n'
            case _ if valor[i] in dict_vars:
                if dict_vars[valor[i]]["tipo"] == "FUNC":
                    instr += "pusha " + str(valor[i]) + "\n" + "call\n"
                elif valor[i] in dict_vars and dict_vars[valor[i]]["tipo"] == "VARIABLE":
                    posicao = dict_vars[valor[i]]["pos"]
                    instr += "pushg " + str(posicao) + "\n"
                else:
                    instr += ""
            case _:  # Default case to handle anything not matched specifically
                if re.match(r'\d+', valor[i]):  # Checking if the item is all digits
                    instr += "pushi " + valor[i] + "\n"
                else:
                    instr += ""

    instr += "return\n\n"  
    return instr





