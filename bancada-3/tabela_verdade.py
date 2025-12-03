from parser_proposicional import parse_expr, get_variables

def avaliar(expr, valores):
    expr_py = parse_expr(expr)
    for k in valores:
        v = valores[k]
        expr_py = expr_py.replace(k, str(v))
    return eval(expr_py)

def gerar_combinacoes(n):
    total = 2 ** n
    resultado = []
    for i in range(total):
        linha = []
        temp = i
        for j in range(n):
            bit = temp % 2
            if bit == 1:
                linha.insert(0, True)
            else:
                linha.insert(0, False)
            temp = temp // 2
        resultado.append(linha)
    return resultado

def tabela_verdade(premissas, conclusao):
    todas = []
    for p in premissas:
        todas.append(p)
    todas.append(conclusao)

    vars_list = []
    for x in todas:
        vars_expr = get_variables(x)
        for v in vars_expr:
            existe = False
            for u in vars_list:
                if u == v:
                    existe = True
                    break
            if not existe:
                vars_list.append(v)
    
    vars = sorted(vars_list)
    
    header = ""
    for v in vars:
        if header != "":
            header = header + " | "
        header = header + v
    
    header_extra = ""
    for p in premissas:
        header_extra = header_extra + " | " + p
    header_extra = header_extra + " | " + conclusao
    
    print("\nTabela-verdade:")
    print(header + header_extra + " | Válido?")

    valido_em_todos = True
    contra_exemplos = []
    
    combinacoes = gerar_combinacoes(len(vars))

    for bits in combinacoes:
        vals = {}
        for i in range(len(vars)):
            vals[vars[i]] = bits[i]

        premissas_val = True
        vals_premissas = []
        for p in premissas:
            valor_p = avaliar(p, vals)
            vals_premissas.append(valor_p)
            if not valor_p:
                premissas_val = False
        
        concl_val = avaliar(conclusao, vals)

        vals_str = ""
        for i in range(len(vars)):
            v = vars[i]
            val = vals[v]
            s = "F"
            if val:
                s = "V"
            if vals_str != "":
                vals_str = vals_str + " | "
            vals_str = vals_str + s
            
        for vp in vals_premissas:
            s = "F"
            if vp: s = "V"
            vals_str = vals_str + " | " + s
            
        s_concl = "F"
        if concl_val: s_concl = "V"
        vals_str = vals_str + " | " + s_concl

        marcador = ""
        if premissas_val and not concl_val:
            valido_em_todos = False
            contra_exemplos.append(vals)
            marcador = " * INVALIDO *"
        elif premissas_val and concl_val:
            marcador = " OK"
        else:
            marcador = " -" 

        print(vals_str + " |" + marcador)

    return valido_em_todos, contra_exemplos
