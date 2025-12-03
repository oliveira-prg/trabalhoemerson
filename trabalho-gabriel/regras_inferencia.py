def particularizacao_universal(expressao, constante):
    return expressao.replace("x", constante)

def generalizacao_existencial(expressao, variavel):
    return f"(∃{variavel}){expressao}"
