#########################################################
# Funções pré-definidas

lista_predefinidas = [("max",
"""
pushfp
load -1
pushfp
load -2
pushsp 
load -1
pushsp 
load -1
sup
jz else1
swap
jump endif1
else1:
endif1:
return\n\n""",2),
("min",
 """
pushfp
load -1
pushfp
load -2
pushsp 
load -1
pushsp 
load -1
inf
jz else1
swap
jump endif1
else1:
endif1:
return\n\n""",2)]

