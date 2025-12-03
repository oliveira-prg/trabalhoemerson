def limpar(s):
    return s.replace(" ", "").replace("(", "").replace(")", "")

def identificar_forma(premissas, conclusao):
    p_limpas = []
    for p in premissas:
        p_limpas.append(limpar(p))
    c_limpa = limpar(conclusao)

    if len(premissas) == 2:
        p1 = p_limpas[0]
        p2 = p_limpas[1]
        
        if "->" in p1:
            partes = p1.split("->")
            if len(partes) == 2:
                ant = partes[0]
                cons = partes[1]
                
                if p2 == ant and c_limpa == cons:
                    return "Modus Ponens"
                
                neg_cons = "~" + cons
                neg_ant = "~" + ant
                if cons.startswith("~"):
                    neg_cons = cons[1:]
                if ant.startswith("~"):
                    neg_ant = ant[1:]

                if (p2 == "~" + cons or p2 == neg_cons) and (c_limpa == "~" + ant or c_limpa == neg_ant):
                    return "Modus Tollens"

                if p2 == cons and c_limpa == ant:
                    return "Falácia da Afirmação do Consequente"
                
                if (p2 == "~" + ant or p2 == neg_ant) and (c_limpa == "~" + cons or c_limpa == neg_cons):
                    return "Falácia da Negação do Antecedente"
                
                if "->" in p2:
                    partes2 = p2.split("->")
                    if len(partes2) == 2:
                        ant2 = partes2[0]
                        cons2 = partes2[1]
                        if cons == ant2:
                            if "->" in c_limpa:
                                partes_c = c_limpa.split("->")
                                if partes_c[0] == ant and partes_c[1] == cons2:
                                    return "Silogismo Hipotético"

        or_op = ""
        if "v" in p1: or_op = "v"
        elif "|" in p1: or_op = "|"
        elif "∨" in p1: or_op = "∨"
        
        if or_op != "":
            partes = p1.split(or_op)
            if len(partes) == 2:
                lado1 = partes[0]
                lado2 = partes[1]
                
                neg_lado1 = "~" + lado1
                if lado1.startswith("~"): neg_lado1 = lado1[1:]
                
                if (p2 == "~" + lado1 or p2 == neg_lado1) and c_limpa == lado2:
                    return "Silogismo Disjuntivo"

                neg_lado2 = "~" + lado2
                if lado2.startswith("~"): neg_lado2 = lado2[1:]
                
                if (p2 == "~" + lado2 or p2 == neg_lado2) and c_limpa == lado1:
                    return "Silogismo Disjuntivo"

    if len(premissas) == 3:
        imps = []
        ous = []
        for p in p_limpas:
            if "->" in p:
                imps.append(p)
            elif "v" in p or "|" in p or "∨" in p:
                ous.append(p)
        
        if len(imps) == 2 and len(ous) == 1:
            return "Dilema Construtivo (provável)"

    return "Forma não reconhecida ou complexa"
