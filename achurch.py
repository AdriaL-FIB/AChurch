from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor

from arbre import *

macros = dict()

class MacroNoDefinit(Exception):
    pass

class TreeVisitor(lcVisitor):
    def visitAplicacio(self, ctx):
        [terme1, terme2] = list(ctx.getChildren())
        return Aplicacio(self.visit(terme1), self.visit(terme2))
    
    def visitAbstraccio(self, ctx):
        [_, lletres, _, terme] = list(ctx.getChildren())
        return currificacio(lletres.getText(), self.visit(terme))
    
    def visitLletra(self, ctx):
        [lletra] = list(ctx.getChildren())
        return lletra.getText()
    
    def visitParentesis(self, ctx):
        [_, terme, _] = list(ctx.getChildren())
        return self.visit(terme)
    
    def visitMacro(self, ctx):
        [macroName] = list(ctx.getChildren())
        name = macroName.getText()
        if not name in macros:
            raise MacroNoDefinit(f'El macro {name} no està definit')
        return macros[macroName.getText()]

    def visitDefinirmacro(self, ctx):
        [macroName, _, terme] = list(ctx.getChildren())
        macros[macroName.getText()] = (self.visit(terme))

    def visitInfix(self, ctx):
        [terme1, op, terme2] = list(ctx.getChildren())
        opChar = op.getText()
        if not opChar in macros:
            raise MacroNoDefinit(f'El macro {opChar} no està definit')
        return Aplicacio(Aplicacio(macros[op.getText()], self.visit(terme1)), self.visit(terme2))


def currificacio(vars: str, terme: Arbre) -> Arbre:
    if len(vars) == 1:
        return Abstraccio(vars[0], terme)
    var1 = vars[0]
    varss = vars[1:]
    return Abstraccio(var1, currificacio(varss, terme))

def printMacros():
    for [macroName, terme] in macros.items():
        print(macroName + " ≡ " + string(terme))

def parseInput(inp: str):
    input_stream = InputStream(inp)
    lexer = lcLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    return (parser.root(), parser)


if __name__ == "__main__":
    MAX_ITERACIONS = 75
    while True:
        inp = input('? ')
        defmacro = '=' in inp or '≡' in inp
        (tree, parser) = parseInput(inp)
        try:
            if parser.getNumberOfSyntaxErrors() == 0: # True
                visitor = TreeVisitor()
                t = visitor.visit(tree)
                if defmacro:
                    printMacros()
                else:
                    print("Arbre:")
                    print(string(t))

                    trobat = [True]
                    beta_red = t
                    iteracions = 0
                    while trobat[0] and iteracions < MAX_ITERACIONS:
                        trobat = [False]
                        t = beta_red
                        (beta_red, operacions) = beta_reduccio(beta_red, trobat)
                        for op in operacions:
                            if op[0] == "l":
                                print("α-conversió: " + op[1] + " → " + op[2])
                            elif op[0] == "a":
                                print(op[1] + " → " + op[2])
                            else:
                                print("β-reducció:")
                                print(op[1] + " → " + op[2])
                                
                        if trobat[0] and string(t) == string(beta_red):
                            beta_red = "Nothing"
                            print("...")
                            break

                    if iteracions >= MAX_ITERACIONS:
                            beta_red = "Nothing"
                            print("...")
                    print("Resultat:")
                    print(string(beta_red))
            else:
                print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
                print(tree.toStringTree(recog=parser))
        except MacroNoDefinit as error:
            print(error)
        except:
            print("Error, input mal format")
