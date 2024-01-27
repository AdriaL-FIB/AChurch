// Gramàtica per expressions senzilles
grammar lc;
root : terme | defmacro             // l'etiqueta ja és root
     ;

terme : '(' terme ')'               # parentesis
    | terme OPERADOR terme          # infix
    | terme terme                   # aplicacio
    | LAMBDA cap '.' terme          # abstraccio
    | (MACRO|OPERADOR)              # macro
    | LLETRA                        # lletra
    ;

defmacro : (MACRO|OPERADOR) ('='|'≡') terme    # definirmacro
    ;

LLETRA : [a-z] ;
MACRO : [A-Z0-9]+ ;
LAMBDA : [\\λ] ;
OPERADOR : [*+-/] ;
cap : LLETRA+ ;
WS  : [ \t\n\r]+ -> skip ;
