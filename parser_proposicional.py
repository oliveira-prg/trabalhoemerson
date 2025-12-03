import re

def get_variables(expr: str):
    expr_temp = expr.replace(" v ", " ")
    vars_found = re.findall(r"[A-Za-z]", expr_temp)
    unique_vars = []
    for v in vars_found:
        if v == "v": 
            continue
        existe = False
        for u in unique_vars:
            if u == v:
                existe = True
                break
        if not existe:
            unique_vars.append(v)
    return sorted(unique_vars)

def parse_expr(expr: str):
    expr = expr.strip()    
    expr = expr.replace("<->", " == ")
    expr = expr.replace("->", " <= ")
    expr = expr.replace("~", " not ")
    expr = expr.replace("&", " and ")
    expr = expr.replace("∧", " and ")
    expr = expr.replace("|", " or ")
    expr = expr.replace("∨", " or ")
    expr = expr.replace(" v ", " or ")
    expr = expr.replace("not", " not ")
    expr = expr.replace("and", " and ")
    expr = expr.replace("or", " or ")
    expr = expr.replace("==", " == ")
    expr = expr.replace("<=", " <= ")
    return expr
