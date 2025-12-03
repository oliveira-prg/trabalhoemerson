import re

def parse_predicado(expr):
    expr = expr.replace(" ", "")
    predicados = re.findall(r"[A-Za-z]+\([A-Za-z0-9,]+\)", expr)
    return predicados

def extrair_predicados_info(exprs):
    info = {}
    for expr in exprs:
        matches = re.finditer(r"([A-Z][a-zA-Z0-9]*)\(([^)]+)\)", expr)
        for m in matches:
            nome = m.group(1)
            args = m.group(2).split(",")
            aridade = len(args)
            if nome not in info:
                info[nome] = aridade
            else:
                if info[nome] != aridade:
                    pass 
    return info
