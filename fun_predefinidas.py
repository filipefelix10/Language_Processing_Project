#########################################################
# Funções pré-definidas

lista_predefinidas = [("max",
"""pushfp
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
writei
pushs " "
writes
jump endif1
else1:
writei
pushs " "
writes
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
sup
jz else1
writei
pushs " "
writes
jump endif1
else1:
swap
writei
pushs " "
writes
endif1:
return\n\n""",2)]

