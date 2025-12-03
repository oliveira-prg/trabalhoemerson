from itertools import product
from parser_predicados import extrair_predicados_info
import re

def transpile_predicado(expr):
    expr = expr.replace(" ", "")
    
    expr = expr.replace("∧", " and ").replace("&", " and ")
    expr = expr.replace("∨", " or ").replace("|", " or ")
    expr = expr.replace("->", " <= ")
    expr = expr.replace("<->", " == ")
    expr = expr.replace("~", " not ")
    
    expr = expr.replace("[", "(").replace("]", ")")
    
    pattern_forall = r"\(∀([a-z])\)"
    while re.search(pattern_forall, expr):
        expr = re.sub(pattern_forall, r"forall(lambda \1: ", expr, count=1)
        expr += ")" 
        
    pattern_exists = r"\(∃([a-z])\)"
    while re.search(pattern_exists, expr):
        expr = re.sub(pattern_exists, r"exists(lambda \1: ", expr, count=1)
        expr += ")"
        
    pattern_pred = r"([A-Z][a-zA-Z0-9]*)\(([^)]+)\)"
    expr = re.sub(pattern_pred, r"PRED['\1'](\2)", expr)
    
    return expr

def avaliar_predicados(premissas, conclusao, dominio):
    todas_exprs = premissas + [conclusao]
    info_predicados = extrair_predicados_info(todas_exprs)
    
    sorted_preds = sorted(info_predicados.keys())
    
    total_bits = 0
    pred_offsets = {}
    for p in sorted_preds:
        aridade = info_predicados[p]
        pred_offsets[p] = total_bits
        total_bits += (len(dominio) ** aridade)
        
    interpretacoes = product([False, True], repeat=total_bits)
    
    dominio_list = dominio
    
    def forall(f):
        return all(f(x) for x in dominio_list)
        
    def exists(f):
        return any(f(x) for x in dominio_list)
    
    py_premissas = [transpile_predicado(p) for p in premissas]
    py_conclusao = transpile_predicado(conclusao)
    
    for bits in interpretacoes:
        PRED = {}
        
        for p in sorted_preds:
            aridade = info_predicados[p]
            offset = pred_offsets[p]
            size = len(dominio) ** aridade
            chunk = bits[offset : offset+size]
            
            mapa = {}
            idx = 0
            
            args_comb = product(dominio_list, repeat=aridade)
            for args in args_comb:
                if aridade == 1:
                    key = args[0]
                else:
                    key = args
                mapa[key] = chunk[idx]
                idx += 1
            
            def make_func(m, arity):
                def func(*args):
                    if arity == 1:
                        k = args[0]
                    else:
                        k = args
                    return m.get(k, False)
                return func
                
            PRED[p] = make_func(mapa, aridade)
            
        context = {
            "forall": forall,
            "exists": exists,
            "PRED": PRED,
            "dominio": dominio_list
        }
        
        for d in dominio_list:
            context[d] = d
            
        try:
            premissas_ok = True
            for pp in py_premissas:
                if not eval(pp, context):
                    premissas_ok = False
                    break
            
            if premissas_ok:
                if not eval(py_conclusao, context):
                    return False, bits
        except Exception:
            return False, None

    return True, None
