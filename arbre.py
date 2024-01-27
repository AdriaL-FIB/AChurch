from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Aplicacio:
    esq: Arbre
    dre: Arbre

@dataclass
class Abstraccio:
    lletra: str
    terme: Arbre

    
Arbre = Aplicacio | Abstraccio | str

# funció per pasar de arbre a string
def string(a: Arbre) -> str:
    match a:
        case Aplicacio(esq, dre):
            return "(" + string(esq) + string(dre) + ")"
        case Abstraccio(lletra, terme):
            return "(λ" + lletra + "." + string(terme) + ")"
        case str(s):
            return s

# Retorna una tupla de dos elements amb l'arbre resultat de fer la beta reducció,
# i una llista de les operacions realitzades: (nom operacio, abans de realitar la operació, després de realitzar la operació)   
def beta_reduccio(a: Arbre, trobat: list[bool]) -> tuple[Arbre, list[(str, str, str)]]:
    if trobat[0]:
        return (a, [])
    match a:
        case Aplicacio(Abstraccio(lletra, terme), dre):
            trobat[0] = True
            (abstraccio, operacions) = alfa_conversio(lletra, terme, dre)
            match abstraccio:
                case Abstraccio(lletra, terme):
                    beta_red = replace(terme, lletra, dre)
                    operacions.append(("b", string(Aplicacio(Abstraccio(lletra, terme), dre)), string(beta_red)))
                    return (beta_red, operacions)
                case _:
                    print("Error al hacer beta")
                    return (a, [])
        case Aplicacio(esq, dre):
            (nouEsq, ops1) = beta_reduccio(esq, trobat)
            (nouDre, ops2) = beta_reduccio(dre, trobat)
            return (Aplicacio(nouEsq, nouDre), ops1 + ops2)
        case Abstraccio(lletra, terme):
            (nou, ops) = beta_reduccio(terme, trobat)
            return (Abstraccio(lletra, nou), ops)
        case str(s):
            return (s, [])
        
# Retorna una tupla de dos elements amb l'arbre resultat l'alfa conversió,
# i una llista de les operacions realitzades: (nom operacio, abans de realitar la operació, després de realitzar la operació)
def alfa_conversio(ll: str, a1: Arbre, a2: Arbre) -> tuple[Arbre, list[(str, str, str)]]:
    lletres1 = lletres_usades(a1)
    lletres2 = lletres_usades(a2)

    #print("Buscant variables lligades a " + string(a1))
    var_lligades = variables_lligades(a1)
    #print("Variables lligades: " + str(var_lligades))

    operacions = []

    t = a1
    for lletra in lletres2:
        if lletra in var_lligades: # hay que hacer alfa conv
            #print("Lletra: " + lletra)
            #print("Vars lligades: " + str(var_lligades))
            nova_lletra = chr((((ord(lletra) - ord('a')) + 1) % 26) + ord('a'))
            while nova_lletra in lletres1:
                nova_lletra = chr((((ord(nova_lletra) - ord('a')) + 1) % 26) + ord('a'))

            #print("α-conversió: " + lletra + " → " + nova_lletra)
            operacions.append(("l", lletra, nova_lletra))
            t = replace(a1, lletra, nova_lletra)
            lletres1.add(nova_lletra)
            #print(string(Abstraccio(ll, a1)) + " → " + string(Abstraccio(ll, t)))
            operacions.append(("a", string(Abstraccio(ll, a1)), string(Abstraccio(ll, t))))
            a1 = t

    return (Abstraccio(ll, a1), operacions)


# Si ho faig d'aquesta manera (amb la funció comentada, fent la intersecció de vars lligades a la esq amb 
# vars lliures a la dreta), per exemple
#
# N2≡λs.λz.s(s(z))
# N3≡λs.λz.s(s(s(z)))
# +≡λp.λq.λx.λy.(px(qxy))
# (N2)+(N2)+(N3)+(N2)
#
# dona malament


# def alfa_conversio(ll: str, a1: Arbre, a2: Arbre) -> tuple[Arbre, list[(str, str, str)]]:
#     lletres1 = lletres_usades(a1)
#     lletres2 = lletres_usades(a2)

#     var_lligades = variables_lligades(a1)
#     var_lliures_dre = lletres2.difference(variables_lligades(a2))

#     operacions = []

#     conflictes = var_lligades.intersection(var_lliures_dre)

#     t = a1
#     for lletra in conflictes:
#         nova_lletra = chr((((ord(lletra) - ord('a')) + 1) % 26) + ord('a'))
#         while nova_lletra in lletres1:
#             nova_lletra = chr((((ord(nova_lletra) - ord('a')) + 1) % 26) + ord('a'))
#         operacions.append(("l", lletra, nova_lletra))
#         t = replace(a1, lletra, nova_lletra)
#         lletres1.add(nova_lletra)
#         operacions.append(("a", string(Abstraccio(ll, a1)), string(Abstraccio(ll, t))))
#         a1 = t

#     return (Abstraccio(ll, a1), operacions)

def lletres_usades(a: Arbre) -> set[str]:
    match a:
        case Aplicacio(esq, dre):
            return lletres_usades(esq).union(lletres_usades(dre))
        case Abstraccio(lletra, terme):
            return set(lletra).union(lletres_usades(terme))
        case str(s):
            return set(s)
        
def variables_lligades(a: Arbre) -> set[str]:
    match a:
        case Aplicacio(esq, dre):
            return variables_lligades(esq).union(variables_lligades(dre))
        case Abstraccio(lletra, terme):
            return set(lletra).union(variables_lligades(terme))
        case str(s):
            return set()

# Reemplaça totes les ocurrències de 'old' per l'arbre 'new' (que pot ser un str també)
def replace(a: Arbre, old: str, new: Arbre) -> Arbre:
    match a:
        case str(s):
            if s == old:
                return new
            else:
                return s
        case Aplicacio(esq, dre):
            return Aplicacio(replace(esq, old, new), replace(dre, old, new))
        case Abstraccio(lletra, terme):
            if type(new) is str:
                lletra = replace(lletra, old, new)
            return Abstraccio(lletra, replace(terme, old, new))
