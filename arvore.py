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
        return code + "stop\n"
    
    def print_lista_variaveis():
        print("VARIAVEIS NO DICT:")
        for key,value in dict_vars.items():
            print(f"key : \n  {key}")
            print("Value :")
            for key2,value2 in value.items():
                print("  "+key2, ":", value2)

    

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
        return res + "\n"


class FuncNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def generate_code(self):
        global n_pushi, dict_var, dict_vars
        valor = self.value.split(" ")
        print(valor)
        match valor[0]:
            case '.': res = 'writei\n' + 'pushs " "\n' + 'writes'
            case 'PRINT_S': res = 'writes'
            case 'EMIT': res = 'writechr'
            case 'CR': res = 'writeln'
            case 'DUP': res = 'dup 1'
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
                        res = "storeg " + str(posicao) + "\n"
                    elif valor[0] in dict_vars and valor[1] == "@":
                        posicao = dict_vars[valor[0]]["pos"]
                        res = "pushg " + str(posicao) + "\n"
                    else: res = ""
        return res + "\n"



