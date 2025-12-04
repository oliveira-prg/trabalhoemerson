import itertools #itertools para gerar todas as combinações possiveis de V e F
import re
import os
import sys
from itertools import product

# ==============================================================================
# PARTE 1: MOTOR DE TABELA VERDADE (Proposicional)
# ==============================================================================

class MotorProposicional:
    def __init__(self):
        #define os elementos que são lidos que não são operadores por um dicionário
        self.mapa_ops = {
            '->': ' <= ', '<->': ' == ', '&': ' and ', '^': ' and ',
            'V': ' or ', 'v': ' or ', '~': ' not '
        }

    def traduzir(self, formula):
        texto = formula.strip().replace(" ", "") #Remove espaços
        tokens = re.findall(r"<->|->|[A-Z][a-zA-Z0-9_]*|V|v|\^|&|~|\(|\)", texto) #elementos aceitos transformados em tokens
        cod_py = [] #array que vai receber o a fórmula traduzida em python
        vars_found = set() #define um objeto para receber as variáveis
        for t in tokens: #para cada token lido
            if t in self.mapa_ops: #se for um operador
                cod_py.append(self.mapa_ops[t])
            elif t[0].isupper() and t != 'V' and t not in self.mapa_ops: #se não for um operador
                cod_py.append(t)
                vars_found.add(t)
            elif t.lower() == 'v': #caso extra pra reconhecer 'ou'
                cod_py.append(' or ')
            else:
                cod_py.append(t)
        return "".join(cod_py), sorted(list(vars_found)) #retorna uma string formatada com as variáveis e os operadores
    
    def identificar_forma(self, premissas, conclusao):
        # Identifica o nome da regra usada
        p_txt = " ".join(premissas) # Junta tudo em uma string gigante
        qtd_setas = p_txt.count("->") #Conta a quantidade ed setas usadas (implicações)

        #Vai ler e se identificar o padrão dentro dos lens de setas vai dar o processo usado        
        if len(premissas) >= 3 and qtd_setas >= 2 and "->" not in conclusao:
            return "Silogismo Hipotético + Modus Ponens"
        if len(premissas) == 2 and qtd_setas == 2 and "->" in conclusao:
            return "Silogismo Hipotético"
        if len(premissas) == 2 and qtd_setas == 1:
            if "~" not in conclusao and conclusao in p_txt and "->" not in conclusao:
                return "Modus Ponens"
        if len(premissas) == 2 and qtd_setas == 1 and "~" in conclusao:
            return "Modus Tollens"
        if len(premissas) == 2 and ("V" in p_txt or "v" in p_txt) and "~" in p_txt:
            return "Silogismo Disjuntivo"

        return "Argumento Dedutivo (Geral)" #caso não seja nada do que está acima

    #gera a tabela verdade
    def gerar_tabela(self, premissas, conclusao): 
        try:
            # Traduz premissas e conclusão
            py_prems, vars_p = [], set()
            for p in premissas: #para cada premissa anteriormente adquirida
                c, v = self.traduzir(p)
                py_prems.append(c)
                vars_p.update(v)
            
            c_conc, vars_c = self.traduzir(conclusao) #traduz a conclusão
            vars_p.update(vars_c)
            
            lista_vars = sorted(list(vars_p)) #organiza as premissa encontradas (como variáveis)
            if not lista_vars: return {'erro': "Nenhuma variável encontrada."}

            # Gera combinações Verdadeiro ou Falso
            combinacoes = list(itertools.product([True, False], repeat=len(lista_vars)))
            linhas = []
            valido = True
            
            for vals in combinacoes:
                ctx = dict(zip(lista_vars, vals)) #cria contexto com o valor das variáveis
                
                # Avalia validade
                res_p = []
                tudo_p = True
                for p in py_prems:
                    v = eval(p, {}, ctx) #modifica o valor se a premissa retorna valor True ou False
                    res_p.append(v)
                    if not v: tudo_p = False
                
                res_c = eval(c_conc, {}, ctx) #armazena o valor de veracidade da conclusão a partir da análise das premissas
                
                status = "-"
                if tudo_p: #Se é válido ou não
                    if res_c: status = "SIM" 
                    else: status = "NÃO"; valido = False
                
                linhas.append({ #cria as linhas com os respectivos valores de verdadeiro ou falso das premissas (com base na quantidade de variaveis n, 2^n)
                    'vars': vals, 'premissas': res_p, 'conclusao': res_c,
                    'conj': tudo_p, 'status': status
                })

            return { #Retorno final da tabela (a própria tabela)
                'tipo': 'proposicional',
                'valido': valido, 'vars': lista_vars, 
                'prems_txt': premissas, 'conc_txt': conclusao,
                'linhas': linhas, 'metodo': 'Tabela Verdade',
                'forma': self.identificar_forma(premissas, conclusao)
            }
        except Exception as e: return {'erro': str(e)}


# PARTE 2: MOTOR DE PREDICADOS (Expansão Recursiva - Sem Pyparsing)
#usando a técnica chamada instanciação em domínio finito.

class MotorPredicados:
    def __init__(self):
        self.motor_prop = MotorProposicional()

    def expandir_formula(self, formula, dominio):
        # Tenta achar um quantificador (Ax) ou (Ex)
        match = re.search(r'\(([AE∀∃]).*?\)\s*(.*)', formula)
        
        if not match:
            # Caso Base: Não tem mais quantificador.
            # Precisa converter Predicados P(a) em variáveis Python P_a
            # Regex: Pega LetraMaiuscula(conteudo)
            return re.sub(r'([A-Z][a-zA-Z0-9_]*)\((.*?)\)', r'\1_\2', formula)

        tipo_quant = match.group(1) # 'A' ou 'E'
        corpo = match.group(2)      # O resto da fórmula
        
        # Descobre qual variável está sendo quantificada (ex: x)
        # Assume-se x na primeira posição após parenteses
        var_match = re.search(r'\(([AE∀∃]).*?([a-z])\)', formula)
        var = var_match.group(2) if var_match else 'x'

        # loop de Expansão
        partes = []
        for elemento in dominio:
            # Substitui a variável pelo elemento do domínio
            # Ex: H(x) vira H(a)
            nova_formula = corpo.replace(f"({var})", f"({elemento})")
            
            # Recursão: Se houver mais quantificadores dentro, expande de novo
            partes.append(self.expandir_formula(nova_formula, dominio))
        
        # Junta as partes
        if tipo_quant in ['A', '∀']:
            return f"({' & '.join(partes)})" # Universal = E
        else:
            return f"({' v '.join(partes)})" # Existencial = ou

    def gerar_explicacao(self, dominio, premissa, conclusao):
        """Gera o texto pedagógico 'Se P(1)=V...'"""
        txt = ""
        
        # analisa Premissa
        if "(A" in premissa or "(∀" in premissa:
            # Pega a bse da premissa para mostrar
            match = re.search(r'\)\s*(.*)', premissa)
            miolo = match.group(1) if match else premissa
            
            # gera exemplos visuais
            exs = []
            for d in dominio:
                # Substitui (x) por (domínio) visualmente
                vis = re.sub(r'\([a-z]\)', f'({d})', miolo)
                exs.append(f"{vis}=V")
            
            txt += f"Se {', '.join(exs)} (para satisfazer {premissa})"
        else:
            txt += f"Se {premissa} é Verdadeiro"

        txt += " Então "

        # Analisa Conclusão
        if "(E" in conclusao or "(∃" in conclusao:
            txt += "existe pelo menos um x tal que a conclusão é V"
        else:
            txt += f"{conclusao} deve ser V" # Caso simples P(a)

        return txt

    def verificar(self, dominio, premissas, conclusao):
        if not dominio: return {'erro': 'Domínio vazio.'}
        
        try:
            # expandir todas as fórmulas para Lógica Proposicional
            novas_premissas = [self.expandir_formula(p, dominio) for p in premissas]
            nova_conclusao = self.expandir_formula(conclusao, dominio)
            
            # usar o Motor Proposicional para validar a expansão
            res_prop = self.motor_prop.gerar_tabela(novas_premissas, nova_conclusao)
            
            if 'erro' in res_prop: return res_prop

            # montar dados para exibição
            regra_nome = "Regra Desconhecida"
            if "(A" in premissas[0] or "(∀" in premissas[0]:
                regra_nome = "Particularização Universal"
                if "(E" in conclusao or "(∃" in conclusao:
                    # Caso especial do seu exemplo
                    regra_nome = f"Se {premissas[0]} então P(c) para qualquer c, logo {conclusao}"
            elif "(E" in premissas[0] or "(∃" in premissas[0]:
                regra_nome = "Particularização Existencial"

            # Gera texto de verificação e validação final
            txt_verif = self.gerar_explicacao(dominio, premissas[0], conclusao)
            if res_prop['valido']:
                txt_verif += " Correto!"
            else:
                txt_verif += " Falso!"

            return {
                'tipo': 'predicados',
                'valido': res_prop['valido'],
                'metodo': 'Enumeração em domínio finito',
                'regra_aplicada': regra_nome,
                'txt_verificacao': txt_verif,
                # Se for inválido, pega a primeira linha da tabela que deu ruim
                'contra': next((l for l in res_prop['linhas'] if l['status'] == "NÃO"), None)
            }

        except Exception as e:
            return {'erro': f"Erro na Expansão: {e}"}
        
# ==============================================================================
# PARTE 4: INTERFACE DE USUÁRIO
# ==============================================================================

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def ler_int(msg):
    while True:
        v = input(msg)
        if v.isdigit(): return int(v)
        print(" > Erro: Digite número.")

def exibir_resultado(dados):
    if 'erro' in dados:
        print(f"\n[ERRO]: {dados['erro']}")
        return

    print("\n" + "="*60)
    
    if dados['tipo'] == 'predicados':
        print(f"Argumento {'Valido' if dados['valido'] else 'Invalido'}")
        print(f"Metodo: {dados['metodo']}")
        print(f"Regra aplicada: {dados['regra_aplicada']}")
        print("\nVerificação:")
        print(dados['txt_verificacao'])
        
        if not dados['valido'] and dados['contra']:
            print("\n(Contraexemplo encontrado na enumeração)")

    else: # Proposicional
        print(f"ARGUMENTO {'VÁLIDO!' if dados['valido'] else 'INVÁLIDO!'}")
        print(f"Método: {dados['metodo']}")
        print(f"Forma: {dados['forma']}")
        
        if dados['valido']:
            print("Justificativa: Em todas as linhas onde as premissas são V,\na conclusão também é V.")
        else:
            print("Justificativa: Existe linha onde Premissas=V e Conclusão=F.")

        print("\nTabela Verdade:")
        str_conj = "(" + "^".join(dados['prems_txt']) + ")"
        headers = dados['vars'] + dados['prems_txt'] + [str_conj] + [dados['conc_txt']] + ["Válido?"]
        
        # Formatação
        col_lens = [max(len(str(h)), 3) for h in headers]
        fmt = " | ".join([f"{{:^{l}}}" for l in col_lens])
        
        print(fmt.format(*headers))
        print("-" * (sum(col_lens) + 3*(len(headers)-1)))

        for l in dados['linhas']:
            vals = ["V" if v else "F" for v in l['vars']] + \
                   ["V" if v else "F" for v in l['premissas']] + \
                   ["V" if l['conj'] else "F"] + \
                   ["V" if l['conclusao'] else "F"] + \
                   [l['status']]
            print(fmt.format(*vals))
    
    print("="*60)
    input("\n[Enter] para voltar...")

def main():
    motor_prop = MotorProposicional()
    motor_pred = MotorPredicados()
    
    while True:
        limpar()
        print("==="*15)
        print("   SISTEMA DE LÓGICA")
        print("==="*15)
        print("1. Lógica Proposicional")
        print("2. Lógica de Predicados")
        print("0. Sair")
        
        try:
            op = input("\nEscolha > ")
            if op == '0': break
            
            if op == '1':
                print("\n--- Proposicional ---")
                qtd = ler_int("Qtd Premissas: ")
                prems = [input(f"Premissa {i+1}: ").strip() for i in range(qtd)]
                conc = input("Conclusão: ").strip()
                res = motor_prop.gerar_tabela(prems, conc)
                exibir_resultado(res)

            elif op == '2':
                print("\n--- Predicados ---")
                print("Ex: (Ax)(H(x)->M(x))")
                dom = input("Domínio (sep. vírgula): ").split(',')
                dominio = [x.strip() for x in dom if x.strip()]
                
                qtd = ler_int("Qtd Premissas: ")
                prems = [input(f"Premissa {i+1}: ").strip() for i in range(qtd)]
                conc = input("Conclusão: ").strip()
                
                print("\nAnalisando...")
                res = motor_pred.verificar(dominio, prems, conc)
                exibir_resultado(res)
        
        except Exception as e:
            print(f"\n[ERRO GERAL]: {e}")
            input("Enter...")

if __name__ == "__main__":
    main()