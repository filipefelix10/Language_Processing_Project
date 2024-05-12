import re
import json
from fun_predefinidas import lista_predefinidas

global  dict_vars
dict_vars = {}

def func_predefinidas(lista):
    global dict_vars
    for func in lista:
        inst = ""
        for n in range(0,func[2]):
            inst += "pushfp\n" + "load " + str(-1-n) + "\n"
        
        inst += func[1]
        dict_temp = {"tipo": "FUNC", "pos": -1, "instrucoes":inst,"Is_call": False}
        dict_vars[func[0]] = dict_temp


func_predefinidas(lista_predefinidas)

def preenche_json():
    global dict_vars
    # Convert and write JSON object to file
    with open("dict_vars.json", "w") as outfile: 
        json.dump(dict_vars, outfile)


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
    def __init__(self, instructions, n_pushi):
        self.instructions = instructions
        self.n_pushi = n_pushi

    def generate_code(self):
        code = "start\n"
        for instruction in self.instructions:
            code += instruction.generate_code() # gera codigo do programa
        if (self.n_pushi > 0 ):
            code = "pushn " + str(self.n_pushi) + "\n" + code
        code = code + "stop\n\n"
        for func in dict_vars:
            if dict_vars[func]["tipo"] == "FUNC" and dict_vars[func]["Is_call"] == True:
                code+= func + ":\n"
                code += dict_vars[func]["instrucoes"]
        preenche_json()
        return code
       

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
            case '=' : res = 'equal'
        return res + "\n"


class WordNodeExec(ASTNode):
    def __init__(self, value):
        self.value = value


    def generate_code(self):
        global dict_vars

        print_s = self.value.split(".")
        valor = self.value.split(" ")
        match valor[0].upper():
            case '.': res = 'writei\n' + 'pushs " "\n' + 'writes'
            case 'EMIT': res = 'writechr'
            case 'CR': res = 'writeln'
            case 'DUP': res = 'dup 1'
            case '2DUP': res = 'pushsp load -1' + '\n' + 'pushsp load -1' + '\n'
            case 'SWAP': res = 'swap'
            case 'DROP': res = 'pop 1'
            case _ if valor[0] in dict_vars and dict_vars[valor[0]]["tipo"] == "FUNC":
                        dict_vars[valor[0]]["Is_call"] = True # Afirma que a função foi chamada
                        res = "pusha " + str(valor[0]) + "\n" + "call\n"
            case _ if len(valor) > 1:
                    if(len(print_s)) > 1: print_s = re.sub(r"(^'|'$)", "", print_s[1])
                    if valor[0] in dict_vars and valor[1] == "@":
                        posicao = dict_vars[valor[0]]["pos"]
                        res = "pushg " + str(posicao)
                    elif not isinstance(print_s,list):
                        res = 'pushs ' + print_s + "\n" + "writes" + "\n"
                    else: res = ""
        return res + "\n"
    

class WordNodeDec(ASTNode):
    def __init__(self, value, n_pushi, instrucoes=None):
        self.value = value
        self.n_pushi = n_pushi
        self.instrucoes = instrucoes

    def generate_code(self):
        global dict_vars
        valor = self.value.split(" ")
        match valor[0]:
            case 'VARIABLE':
                if len(valor) > 1:
                    dict_temp = {"tipo": "VARIABLE", "pos": self.n_pushi}
                    dict_vars[valor[1]] = dict_temp
                res = ""
            case _ if len(valor) > 1:
                    if valor[0] in dict_vars and valor[1] == "!":
                        posicao = dict_vars[valor[0]]["pos"]
                        res = "storeg " + str(posicao)
                    elif valor[0] == ":":
                        res = ''
                        valor = " ".join(valor)
                        valor = valor.split(")")
                        list_n = valor[0].split("(")[1].split(" ")
                        n_numbers = list_n.count("n")

                        inst = ""
                        for n in range(0,n_numbers):
                            inst += "pushfp\n" + "load " + str(-1-n) + "\n" 
                        
                        for i in self.instrucoes:
                            inst += i.generate_code()
                        inst += "return\n\n"
                        dict_temp = {"tipo": "FUNC", "pos": self.n_pushi, "instrucoes":inst,"Is_call": True}
                        dict_vars[valor[0].split(' ')[1]] = dict_temp
                      
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
        if self.condition2:
            for i in self.condition2:
                code += i.generate_code()
        code += "endif" + str(self.if_count) + ":\n"

        return code


class LoopNodeUntil(ASTNode):
    def __init__(self, condition1, if_count):
        self.condition1 = condition1
        self.if_count = if_count
    
    def generate_code(self):
        code = ""
        code += "while" + str(self.if_count) + ":\n"
        for i in self.condition1:
            code += i.generate_code()
        code += "jz endwhile" + str(self.if_count) + "\n"
        code += "jump while" + str(self.if_count) + "\n"
        code += "endwhile" + str(self.if_count) + ":\n"

        return code
    
class LoopNodeAgain(ASTNode):
    def __init__(self, condition1, if_count):
        self.condition1 = condition1
        self.if_count = if_count
    
    def generate_code(self):
        code = "while" + str(self.if_count) + ":\n"
        for i in self.condition1:
            code += i.generate_code()
        code += "jump while" + str(self.if_count) + "\n"

        return code
    
class LoopNodeWhile(ASTNode):
    def __init__(self, condition1, if_count, condition2=None):
        self.condition1 = condition1
        self.condition2 = condition2
        self.if_count = if_count
    
    def generate_code(self):
        code = "while" + str(self.if_count) + ":\n"
        for i in self.condition1:
            code += i.generate_code()
        code += "jz endwhile" + str(self.if_count) + "\n"
        for i in self.condition2:
            code += i.generate_code()
        code += "jump while" + str(self.if_count) + "\n"
        code += "endwhile" + str(self.if_count) + ":\n"

        return code
    
class LoopNodeDO(ASTNode):
    def __init__(self, condition1, if_count, n_pushi, isPlus=False):
        self.condition1 = condition1
        self.if_count = if_count
        self.n_pushi = n_pushi
        self.isPlus = isPlus
    
    def generate_code(self):
        code = "storeg " + str(self.n_pushi+1) + "\n" 
        code += "storeg " + str(self.n_pushi) + "\n"
        code += "while" + str(self.if_count) + ":\n"
        for i in self.condition1:
            code += i.generate_code()
        code += "pushg " + str(self.n_pushi+1) + "\n"
        if self.isPlus:
            code += str(self.condition1[-1].generate_code())
        else:
            code += "pushi 1\n"
        code += "add\n"
        code += "storeg " + str(self.n_pushi+1) + "\n"
        code += "pushg " + str(self.n_pushi+1) + "\n"
        code += "pushg " + str(self.n_pushi) + "\n"
        code += "inf\n"
        code += "jz endwhile" + str(self.if_count) + "\n"
        code += "jump while" + str(self.if_count) + "\n"
        code += "endwhile" + str(self.if_count) + ":\n"

        return code
    
