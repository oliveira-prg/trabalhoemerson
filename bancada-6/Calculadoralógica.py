# =============================================================================
# TRABALHO DE MD TOPPISSIMO
# =============================================================================

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import itertools as it
import re

# =============================================================================
# PROPOSICIONAL
# =============================================================================


class MotorLogico:
    """
    Motor principal para lógica proposicional.
    Responsável por parsing, avaliação e identificação de formas de argumento.
    """

    def __init__(self):
        """Inicializa o motor com lista de operadores."""
        self.operadores = ['~', '¬', '&', '^', '∧',
                           'V', 'v', '|', '∨', '->', '→', '<->', '↔']

    def normalizar_formula(self, formula):
        """Normaliza a fórmula para formato padrão."""
        f = formula.strip()
        f = f.replace('¬', '~')
        f = f.replace('∧', '&')
        f = f.replace('^', '&')
        f = f.replace('∨', 'V')
        f = f.replace('|', 'V')
        f = f.replace('→', '->')
        f = f.replace('↔', '<->')
        return f

    def extrair_variaveis(self, formula):
        """Extrai todas as variáveis proposicionais da fórmula."""
        f = self.normalizar_formula(formula)
        f = f.replace('->', ' ').replace('<->', ' ')
        f = f.replace('~', ' ').replace('&', ' ').replace('V', ' ')
        f = f.replace('(', ' ').replace(')', ' ')

        variaveis = set()
        tokens = f.split()
        for token in tokens:
            token = token.strip()
            if token and token[0].isupper() and token not in ['V']:
                variaveis.add(token)

        return sorted(list(variaveis))

    def parse_e_avaliar(self, formula, valores):
        """
        Parser para avaliar fórmulas com precedência correta.
        """
        f = self.normalizar_formula(formula).strip()

        # Remove parênteses externos se forem correspondentes
        while f.startswith('(') and f.endswith(')'):
            nivel = 0
            pode_remover = True
            for i, c in enumerate(f):
                if c == '(':
                    nivel += 1
                elif c == ')':
                    nivel -= 1
                if nivel == 0 and i < len(f) - 1:
                    pode_remover = False
                    break
            if pode_remover:
                f = f[1:-1].strip()
            else:
                break

        # Procura operador de menor precedência fora de parênteses
        nivel = 0
        pos_bic = -1
        pos_imp = -1
        pos_or = -1
        pos_and = -1

        i = 0
        while i < len(f):
            c = f[i]
            if c == '(':
                nivel += 1
            elif c == ')':
                nivel -= 1
            elif nivel == 0:
                if f[i:i+3] == '<->':
                    pos_bic = i
                elif f[i:i+2] == '->' and pos_bic == -1:
                    pos_imp = i
                elif c == 'V' and f[i-1:i] != '-' and pos_bic == -1 and pos_imp == -1:
                    pos_or = i
                elif c == '&' and pos_bic == -1 and pos_imp == -1 and pos_or == -1:
                    pos_and = i
            i += 1

        # Bicondicional
        if pos_bic != -1:
            esq = f[:pos_bic].strip()
            dir = f[pos_bic+3:].strip()
            val_esq = self.parse_e_avaliar(esq, valores)
            val_dir = self.parse_e_avaliar(dir, valores)
            return val_esq == val_dir

        # Implicação
        if pos_imp != -1:
            esq = f[:pos_imp].strip()
            dir = f[pos_imp+2:].strip()
            val_esq = self.parse_e_avaliar(esq, valores)
            val_dir = self.parse_e_avaliar(dir, valores)
            return (not val_esq) or val_dir

        # Disjunção
        if pos_or != -1:
            esq = f[:pos_or].strip()
            dir = f[pos_or+1:].strip()
            val_esq = self.parse_e_avaliar(esq, valores)
            val_dir = self.parse_e_avaliar(dir, valores)
            return val_esq or val_dir

        # Conjunção
        if pos_and != -1:
            esq = f[:pos_and].strip()
            dir = f[pos_and+1:].strip()
            val_esq = self.parse_e_avaliar(esq, valores)
            val_dir = self.parse_e_avaliar(dir, valores)
            return val_esq and val_dir

        # Negação
        if f.startswith('~'):
            operando = f[1:].strip()
            return not self.parse_e_avaliar(operando, valores)

        # Variável
        f = f.strip()
        if f in valores:
            return valores[f]

        return False

    def gerar_tabela_verdade(self, premissas, conclusao):
        """
        Gera tabela verdade completa.

        Returns:
            Tupla (valido, tabela_str, contraexemplo, linhas_dados)
        """
        todas_formulas = premissas + [conclusao]
        variaveis = set()
        for f in todas_formulas:
            variaveis.update(self.extrair_variaveis(f))
        variaveis = sorted(list(variaveis))

        if not variaveis:
            return False, "Erro: Nenhuma variável encontrada", None, []

        combinacoes = list(it.product([True, False], repeat=len(variaveis)))

        # Monta cabeçalho
        linhas = []
        cab_parts = variaveis.copy()
        for p in premissas:
            cab_parts.append(p)
        cab_parts.append(
            f"({' ∧ '.join(['P'+str(i+1) for i in range(len(premissas))])})")
        cab_parts.append(conclusao)
        cab_parts.append("Válido?")

        cab = " | ".join(cab_parts)
        linhas.append(cab)
        linhas.append("-" * len(cab))

        valido = True
        contraexemplo = None
        linhas_dados = []

        for vals in combinacoes:
            mapa = dict(zip(variaveis, vals))

            # Avalia cada premissa
            vals_prems = []
            for p in premissas:
                val = self.parse_e_avaliar(p, mapa)
                vals_prems.append(val)

            # Conjunção das premissas
            conj_prems = all(vals_prems)

            # Avalia conclusão
            val_conc = self.parse_e_avaliar(conclusao, mapa)

            # Verifica validade
            if conj_prems and not val_conc:
                linha_valida = False
                valido = False
                if contraexemplo is None:
                    contraexemplo = mapa.copy()
            else:
                linha_valida = True if conj_prems else None

            # Monta linha
            linha_parts = []
            for v in vals:
                linha_parts.append("V" if v else "F")
            for vp in vals_prems:
                linha_parts.append("V" if vp else "F")
            linha_parts.append("V" if conj_prems else "F")
            linha_parts.append("V" if val_conc else "F")

            if conj_prems:
                linha_parts.append("✓" if linha_valida else "✗")
            else:
                linha_parts.append("-")

            linhas.append(" | ".join(linha_parts))
            linhas_dados.append({
                'valores': mapa,
                'premissas': vals_prems,
                'conjuncao': conj_prems,
                'conclusao': val_conc,
                'valida': linha_valida
            })

        return valido, "\n".join(linhas), contraexemplo, linhas_dados

    def identificar_forma(self, premissas, conclusao):
        """
        Identifica formas conhecidas de argumentos.
        """
        prems = [self.normalizar_formula(p).replace(
            " ", "") for p in premissas if p.strip()]
        conc = self.normalizar_formula(conclusao).replace(" ", "")

        formas = []

        # Analisa cada premissa
        for i, p in enumerate(prems):
            if "->" in p:
                partes = p.split("->")
                if len(partes) == 2:
                    ant = partes[0].strip("()")
                    cons = partes[1].strip("()")

                    for j, outra in enumerate(prems):
                        if i != j:
                            outra_limpa = outra.strip("()")

                            # Modus Ponens
                            if outra_limpa == ant and conc.strip("()") == cons:
                                formas.append("Modus Ponens")

                            # Modus Tollens
                            if outra_limpa == f"~{cons}" and conc.strip("()") == f"~{ant}":
                                formas.append("Modus Tollens")
                            if outra_limpa == f"~({cons})" and conc.strip("()") == f"~({ant})":
                                formas.append("Modus Tollens")

                            # Falácia: Afirmação do Consequente
                            if outra_limpa == cons and conc.strip("()") == ant:
                                formas.append(
                                    "⚠️ Falácia: Afirmação do Consequente")

                            # Falácia: Negação do Antecedente
                            if outra_limpa == f"~{ant}" and conc.strip("()") == f"~{cons}":
                                formas.append(
                                    "⚠️ Falácia: Negação do Antecedente")

        # Silogismo Hipotético
        implicacoes = []
        for p in prems:
            if "->" in p:
                partes = p.split("->")
                if len(partes) == 2:
                    implicacoes.append(
                        (partes[0].strip("()"), partes[1].strip("()")))

        if len(implicacoes) >= 2 and "->" in conc:
            partes_conc = conc.split("->")
            if len(partes_conc) == 2:
                ant_conc = partes_conc[0].strip("()")
                cons_conc = partes_conc[1].strip("()")

                for ant1, cons1 in implicacoes:
                    for ant2, cons2 in implicacoes:
                        if cons1 == ant2 and ant1 == ant_conc and cons2 == cons_conc:
                            formas.append("Silogismo Hipotético")

        # Silogismo Disjuntivo
        for i, p in enumerate(prems):
            if "V" in p and "->" not in p:
                partes = p.replace("(", "").replace(")", "").split("V")
                if len(partes) == 2:
                    d1, d2 = partes[0].strip(), partes[1].strip()
                    for j, outra in enumerate(prems):
                        if i != j:
                            outra_limpa = outra.strip("()")
                            if outra_limpa == f"~{d1}" and conc.strip("()") == d2:
                                formas.append("Silogismo Disjuntivo")
                            if outra_limpa == f"~{d2}" and conc.strip("()") == d1:
                                formas.append("Silogismo Disjuntivo")

        formas = list(dict.fromkeys(formas))

        if not formas:
            return "Forma Genérica"

        return " + ".join(formas)

    def validar_argumento(self, premissas, conclusao):
        """
        Valida um argumento e retorna resultado.
        """
        premissas = [p.strip() for p in premissas if p.strip()]
        conclusao = conclusao.strip()

        if not premissas:
            return {
                'valido': False,
                'erro': 'Nenhuma premissa fornecida',
                'tabela': '',
                'forma': '',
                'contraexemplo': None
            }

        if not conclusao:
            return {
                'valido': False,
                'erro': 'Conclusão não fornecida',
                'tabela': '',
                'forma': '',
                'contraexemplo': None
            }

        valido, tabela, contraexemplo, dados = self.gerar_tabela_verdade(
            premissas, conclusao)
        forma = self.identificar_forma(premissas, conclusao)

        return {
            'valido': valido,
            'erro': None,
            'tabela': tabela,
            'forma': forma,
            'contraexemplo': contraexemplo,
            'dados': dados,
            'premissas': premissas,
            'conclusao': conclusao
        }


# =============================================================================
# PREDICADOS
# =============================================================================

class MotorPredicados:
    """
    Motor para lógica de predicados com domínio finito.
    """

    def __init__(self, motor_prop):
        self.motor_prop = motor_prop
        self.passos = []

    def expandir(self, formula, dominio):
        """Expande quantificadores para domínio finito."""
        formula = formula.strip()
        formula = formula.replace('∀', 'A').replace('∃', 'E')

        # Quantificador Universal (Ax) -> Conjunção (&)
        match_univ = re.match(r'\(?\s*A\s*([a-z])\s*\)?\s*(.+)', formula)
        if match_univ:
            var = match_univ.group(1)
            corpo = match_univ.group(2).strip()
            corpo = self._limpar_parenteses(corpo)

            partes = []
            for d in dominio:
                instancia = self._substituir(corpo, var, str(d))
                instancia_expandida = self.expandir(instancia, dominio)
                partes.append(f"({instancia_expandida})")

            resultado = " & ".join(partes)
            return resultado

        # Quantificador Existencial (Ex) -> Disjunção (V)
        match_exist = re.match(r'\(?\s*E\s*([a-z])\s*\)?\s*(.+)', formula)
        if match_exist:
            var = match_exist.group(1)
            corpo = match_exist.group(2).strip()
            corpo = self._limpar_parenteses(corpo)

            partes = []
            for d in dominio:
                instancia = self._substituir(corpo, var, str(d))
                instancia_expandida = self.expandir(instancia, dominio)
                partes.append(f"({instancia_expandida})")

            resultado = " V ".join(partes)
            return resultado

        # Tratamento para negações de quantificadores (De Morgan)
        if formula.startswith('~'):
            match_neg_univ = re.match(r'~\s*\(?\s*A\s*([a-z])\s*\)?\s*(.+)', formula)
            if match_neg_univ:
                var = match_neg_univ.group(1)
                corpo = match_neg_univ.group(2)
                return self.expandir(f"(E{var})~({corpo})", dominio)

            match_neg_exist = re.match(r'~\s*\(?\s*E\s*([a-z])\s*\)?\s*(.+)', formula)
            if match_neg_exist:
                var = match_neg_exist.group(1)
                corpo = match_neg_exist.group(2)
                return self.expandir(f"(A{var})~({corpo})", dominio)

        return formula

    def _limpar_parenteses(self, corpo):
        if corpo.startswith("(") and corpo.endswith(")"):
            nivel = 0
            for i, c in enumerate(corpo):
                if c == "(":
                    nivel += 1
                elif c == ")":
                    nivel -= 1
                if nivel == 0 and i < len(corpo) - 1:
                    return corpo
            return corpo[1:-1]
        return corpo

    def _substituir(self, formula, var, valor):
        resultado = []
        i = 0
        while i < len(formula):
            if i + 1 < len(formula) and formula[i].isupper() and formula[i+1] == '(':
                j = i + 2
                nivel = 1
                while j < len(formula) and nivel > 0:
                    if formula[j] == '(':
                        nivel += 1
                    elif formula[j] == ')':
                        nivel -= 1
                    j += 1
                predicado = formula[i:j]
                novo_predicado = re.sub(rf'\b{var}\b', valor, predicado)
                resultado.append(novo_predicado)
                i = j
            else:
                resultado.append(formula[i])
                i += 1
        return "".join(resultado)

    def _detectar_regra(self, premissas_orig, conclusao_orig):
        """
        Detecta qual regra de inferência está sendo aplicada.
        """
        prem_norm = [p.replace('∀', 'A').replace('∃', 'E').strip() for p in premissas_orig]
        conc_norm = conclusao_orig.replace('∀', 'A').replace('∃', 'E').strip()
        
        # Caso: (Ax)P(x) |- P(a) - Particularização Universal
        if len(prem_norm) == 1:
            match_prem = re.match(r'\(A([a-z])\)(.+)', prem_norm[0])
            if match_prem:
                var = match_prem.group(1)
                corpo = match_prem.group(2).strip()
                # Verifica se conclusão é uma instância do corpo
                match_conc = re.match(r'([A-Z])\(([^)]+)\)', conc_norm)
                if match_conc:
                    return f"Se (∀{var}){corpo} então {conc_norm} para qualquer constante"
        
        # Caso: (Ax)P(x) |- (Ex)P(x) - Universal implica Existencial
        if len(prem_norm) == 1:
            match_prem = re.match(r'\(A([a-z])\)(.+)', prem_norm[0])
            match_conc = re.match(r'\(E([a-z])\)(.+)', conc_norm)
            if match_prem and match_conc:
                var_p = match_prem.group(1)
                corpo_p = match_prem.group(2).strip()
                var_c = match_conc.group(1)
                corpo_c = match_conc.group(2).strip()
                if corpo_p == corpo_c:
                    return f"Se (∀{var_p})P({var_p}) então P(c) para qualquer c, logo (∃{var_c})P({var_c})"
        
        # Caso: P(a) |- (Ex)P(x) - Generalização Existencial
        if len(prem_norm) == 1:
            match_conc = re.match(r'\(E([a-z])\)(.+)', conc_norm)
            if match_conc and '(A' not in prem_norm[0] and '(E' not in prem_norm[0]:
                var = match_conc.group(1)
                return f"Se P(c) para alguma constante c, então (∃{var})P({var})"
        
        return "Enumeração em domínio finito"

    def validar(self, premissas, conclusao, dominio_str):
        """
        Valida o argumento e retorna um DICIONÁRIO.
        """
        try:
            # 1. Processar Domínio
            dom = [x.strip() for x in dominio_str.replace("{", "").replace("}", "").split(",") if x.strip()]
            if not dom:
                dom = ['a', 'b']

            self.passos = []

            # 2. Expansão
            premissas_exp = []
            for p in premissas:
                if p.strip():
                    exp = self.expandir(p.strip(), dom)
                    premissas_exp.append(exp)

            conclusao_exp = self.expandir(conclusao.strip(), dom)

            # 3. Validação usando motor proposicional
            res_prop = self.motor_prop.validar_argumento(premissas_exp, conclusao_exp)

            valido = res_prop['valido']
            contra = res_prop['contraexemplo']

            # 4. Detectar regra aplicada
            regra = self._detectar_regra(premissas, conclusao)

            # 5. Montar o Relatório.
            relatorio = []
            relatorio.append("Saída:")
            
            if valido:
                relatorio.append("✓ ARGUMENTO VÁLIDO")
            else:
                relatorio.append("✗ ARGUMENTO INVÁLIDO")
            
            relatorio.append("Método: Enumeração em domínio finito")
            relatorio.append(f"Regra aplicada: {regra}")
            relatorio.append("")
            relatorio.append("Verificação:")
            
            # Gerar a verificação.
            
            # Extrair predicado base
            pred_match = re.search(r'([A-Z])\(', premissas[0] if premissas else conclusao)
            pred_nome = pred_match.group(1) if pred_match else 'P'
            
            # Verificar tipo de argumento
            prem_norm = premissas[0].replace('∀', 'A').replace('∃', 'E').strip() if premissas else ""
            conc_norm = conclusao.replace('∀', 'A').replace('∃', 'E').strip()
            
            if re.match(r'\(A[a-z]\)', prem_norm):
                # Premissa universal
                instancias = [f"{pred_nome}({d})=V" for d in dom]
                relatorio.append(f"Se {', '.join(instancias)} (para satisfazer ∀x{pred_nome}(x))")
                
                if re.match(r'\(E[a-z]\)', conc_norm):
                    # Conclusão existencial
                    if valido:
                        relatorio.append(f"Então existe pelo menos um x com {pred_nome}(x)=V ✓")
                    else:
                        relatorio.append(f"Mas não existe x com {pred_nome}(x)=V ✗")
                else:
                    # Conclusão é instância específica
                    if valido:
                        relatorio.append(f"Então {conclusao.strip()} é verdadeiro ✓")
                    else:
                        relatorio.append(f"Mas {conclusao.strip()} pode ser falso ✗")
            
            elif re.match(r'\(E[a-z]\)', prem_norm):
                # Premissa existencial
                instancias = [f"{pred_nome}({d})" for d in dom]
                relatorio.append(f"Se existe pelo menos um x tal que {pred_nome}(x)=V")
                if valido:
                    relatorio.append(f"Então a conclusão {conclusao.strip()} é satisfeita ✓")
                else:
                    relatorio.append(f"Não garante que {conclusao.strip()} seja verdadeiro ✗")
            else:
                # Premissa é instância específica
                if valido:
                    relatorio.append(f"A partir de {premissas[0] if premissas else 'premissa'}, a conclusão segue ✓")
                else:
                    relatorio.append(f"A partir de {premissas[0] if premissas else 'premissa'}, a conclusão não segue ✗")

            if not valido and contra:
                relatorio.append("")
                relatorio.append("Contraexemplo encontrado:")
                for k, v in contra.items():
                    relatorio.append(f"  {k} = {'V' if v else 'F'}")

            return {
                'valido': valido,
                'relatorio_texto': "\n".join(relatorio),
                'tabela': res_prop['tabela'],
                'contraexemplo': contra,
                'passos': self.passos,
                'dominio': dom,
                'formula_expandida': f"({' & '.join(premissas_exp)}) -> {conclusao_exp}" if premissas_exp else conclusao_exp
            }

        except Exception as e:
            return {
                'valido': False,
                'relatorio_texto': f"Erro durante a validação: {str(e)}",
                'tabela': "",
                'contraexemplo': None,
                'passos': [],
                'dominio': [],
                'formula_expandida': "Erro"
            }


# =============================================================================
# SKOLEMIZAÇÃO E FNP
# =============================================================================

class Skolemizador:
    """
    Implementa conversão para Forma Normal Prenex (FNP) e Skolemização.
    """

    def __init__(self):
        self.contador_skolem = 0
        self.passos_detalhados = []

    def processar(self, formula):
        """
        Entrada:
        (∀x)P(x) -> (∃y)Q(y)
        
        Saída:
        Passo 1 - Eliminar implicação:
        -(∀x)P(x) v (∃y)Q(y)
        
        Passo 2 - Mover negação:
        (∃x)-P(x) v (∃y)Q(y)
        
        Passo 3 - Forma Normal Prenex:
        (∃x)(∃y)[-P(x) v Q(y)]
        
        Passo 4 - Skolemização:
        -P(c₁) v Q(c₂)
        onde c₁, c₂ são constantes de Skolem
        """
        self.passos_detalhados = []
        self.contador_skolem = 0
        linhas = []

        # Cabeçalho
        linhas.append("Entrada:")
        linhas.append(formula)
        linhas.append("")
        linhas.append("Saída:")

        # Normaliza símbolos internamente
        f = formula.replace('∀', 'A').replace('∃', 'E').replace('¬', '-')
        f = f.replace('→', '->').replace('↔', '<->')
        f = f.replace('~', '-')

        # =================================================================
        # PASSO 1: ELIMINAR IMPLICAÇÃO
        # =================================================================
        f1 = self._eliminar_implicacao(f)
        
        linhas.append("Passo 1 - Eliminar implicação:")
        linhas.append(self._formatar_saida(f1))
        linhas.append("")
        self.passos_detalhados.append(("Eliminar Implicação", f1))

        # =================================================================
        # PASSO 2: MOVER NEGAÇÕES
        # =================================================================
        f2 = self._mover_negacoes(f1)
        
        linhas.append("Passo 2 - Mover negação:")
        linhas.append(self._formatar_saida(f2))
        linhas.append("")
        self.passos_detalhados.append(("Mover Negação", f2))

        # =================================================================
        # PASSO 3: FORMA NORMAL PRENEX
        # =================================================================
        f3, quantificadores, matriz = self._forma_normal_prenex(f2)
        
        linhas.append("Passo 3 - Forma Normal Prenex:")
        linhas.append(self._formatar_saida(f3))
        linhas.append("")
        self.passos_detalhados.append(("Forma Normal Prenex", f3))

        # =================================================================
        # PASSO 4: SKOLEMIZAÇÃO
        # =================================================================
        f4, constantes_usadas = self._skolemizar(quantificadores, matriz)
        
        linhas.append("Passo 4 - Skolemização:")
        linhas.append(self._formatar_saida(f4))
        
        # Adiciona explicação das constantes de Skolem
        if constantes_usadas:
            linhas.append(f"onde {', '.join(constantes_usadas)} são constantes de Skolem")
        
        self.passos_detalhados.append(("Skolemização", f4))

        return "\n".join(linhas)

    def _eliminar_implicacao(self, formula):
        """
        Elimina implicações: P -> Q  =>  -P v Q
        """
        f = formula.strip()
        f = self._processar_parenteses_impl(f)
        f = self._substituir_implicacoes_nivel(f)
        return f

    def _processar_parenteses_impl(self, formula):
        """Processa conteúdo dentro de parênteses recursivamente."""
        resultado = []
        i = 0
        
        while i < len(formula):
            # Quantificadores (Ax) ou (Ex) - não processar
            if formula[i] == '(' and i + 3 < len(formula):
                if formula[i+1] in 'AE' and formula[i+2].islower() and formula[i+3] == ')':
                    resultado.append(formula[i:i+4])
                    i += 4
                    continue
            
            # Predicados P(x) - não processar argumentos
            if formula[i].isupper() and i + 1 < len(formula) and formula[i+1] == '(':
                resultado.append(formula[i])
                i += 1
                if i < len(formula) and formula[i] == '(':
                    nivel = 1
                    resultado.append('(')
                    i += 1
                    while i < len(formula) and nivel > 0:
                        if formula[i] == '(':
                            nivel += 1
                        elif formula[i] == ')':
                            nivel -= 1
                        resultado.append(formula[i])
                        i += 1
                continue
            
            # Parênteses de agrupamento - processar conteúdo
            if formula[i] == '(':
                nivel = 1
                inicio = i + 1
                i += 1
                while i < len(formula) and nivel > 0:
                    if formula[i] == '(':
                        nivel += 1
                    elif formula[i] == ')':
                        nivel -= 1
                    i += 1
                fim = i - 1
                conteudo = formula[inicio:fim]
                conteudo_processado = self._eliminar_implicacao(conteudo)
                resultado.append('(' + conteudo_processado + ')')
                continue
            
            resultado.append(formula[i])
            i += 1
        
        return ''.join(resultado)

    def _substituir_implicacoes_nivel(self, formula):
        """Substitui implicações no nível atual."""
        nivel = 0
        pos_impl = -1
        i = 0
        
        while i < len(formula) - 1:
            c = formula[i]
            
            # Pula quantificadores
            if c == '(' and i + 3 < len(formula):
                if formula[i+1] in 'AE' and formula[i+2].islower() and formula[i+3] == ')':
                    i += 4
                    continue
            
            # Pula predicados
            if c.isupper() and i + 1 < len(formula) and formula[i+1] == '(':
                i += 1
                pnivel = 1
                i += 1
                while i < len(formula) and pnivel > 0:
                    if formula[i] == '(':
                        pnivel += 1
                    elif formula[i] == ')':
                        pnivel -= 1
                    i += 1
                continue
            
            if c == '(':
                nivel += 1
            elif c == ')':
                nivel -= 1
            elif nivel == 0 and formula[i:i+2] == '->':
                pos_impl = i
            
            i += 1

        if pos_impl < 0:
            return formula

        antecedente = formula[:pos_impl].strip()
        consequente = formula[pos_impl+2:].strip()
        consequente = self._substituir_implicacoes_nivel(consequente)
        
        # P -> Q  =>  -P v Q
        return f"-{antecedente} v {consequente}"

    def _mover_negacoes(self, formula):
        """
        Move negações para dentro usando De Morgan:
        -(Ax)P => (Ex)-P
        -(Ex)P => (Ax)-P
        --P => P
        """
        f = formula
        mudou = True
        max_iter = 100
        iter_count = 0
        
        while mudou and iter_count < max_iter:
            mudou = False
            iter_count += 1
            
            # Dupla negação
            while '--' in f:
                f = f.replace('--', '')
                mudou = True
            
            # -(Ax) => (Ex)-
            match = re.search(r'-\(A([a-z])\)', f)
            if match:
                var = match.group(1)
                pos_inicio = match.start()
                pos_quant_fim = match.end()
                escopo, pos_fim = self._encontrar_escopo(f, pos_quant_fim)
                novo = f"(E{var})-{escopo}"
                f = f[:pos_inicio] + novo + f[pos_fim:]
                mudou = True
                continue
            
            # -(Ex) => (Ax)-
            match = re.search(r'-\(E([a-z])\)', f)
            if match:
                var = match.group(1)
                pos_inicio = match.start()
                pos_quant_fim = match.end()
                escopo, pos_fim = self._encontrar_escopo(f, pos_quant_fim)
                novo = f"(A{var})-{escopo}"
                f = f[:pos_inicio] + novo + f[pos_fim:]
                mudou = True
                continue
        
        return f

    def _encontrar_escopo(self, formula, pos):
        """Encontra o escopo de um quantificador."""
        if pos >= len(formula):
            return "", pos
        
        while pos < len(formula) and formula[pos].isspace():
            pos += 1
        
        if pos >= len(formula):
            return "", pos
        
        inicio = pos
        
        # Outro quantificador
        if formula[pos] == '(' and pos + 3 < len(formula):
            if formula[pos+1] in 'AE' and formula[pos+2].islower() and formula[pos+3] == ')':
                sub_escopo, pos = self._encontrar_escopo(formula, pos + 4)
                return formula[inicio:pos], pos
        
        # Parênteses
        if formula[pos] == '(':
            nivel = 1
            pos += 1
            while pos < len(formula) and nivel > 0:
                if formula[pos] == '(':
                    nivel += 1
                elif formula[pos] == ')':
                    nivel -= 1
                pos += 1
            return formula[inicio:pos], pos
        
        # Negação
        if formula[pos] == '-':
            pos += 1
            sub, fim = self._encontrar_escopo(formula, pos)
            return '-' + sub, fim
        
        # Predicado
        if formula[pos].isupper():
            pos += 1
            if pos < len(formula) and formula[pos] == '(':
                nivel = 1
                pos += 1
                while pos < len(formula) and nivel > 0:
                    if formula[pos] == '(':
                        nivel += 1
                    elif formula[pos] == ')':
                        nivel -= 1
                    pos += 1
            return formula[inicio:pos], pos
        
        return formula[pos], pos + 1

    def _forma_normal_prenex(self, formula):
        """Move todos os quantificadores para o início."""
        f = formula
        
        quantificadores = []
        padrao = re.compile(r'\(([AE])([a-z])\)')
        
        for m in padrao.finditer(f):
            quantificadores.append((m.group(1), m.group(2)))
        
        matriz = padrao.sub('', f).strip()
        matriz = re.sub(r'\s+', ' ', matriz)
        
        if quantificadores:
            quant_str = "".join([f"({t}{v})" for t, v in quantificadores])
            fnp = f"{quant_str}[{matriz}]"
        else:
            fnp = matriz
        
        return fnp, quantificadores, matriz

    def _skolemizar(self, quantificadores, matriz):
        """
        Aplica Skolemização eliminando quantificadores existenciais.
        Retorna (resultado, lista_de_constantes_usadas)
        """
        resultado = matriz
        constantes_usadas = []
        vars_universais = []
        
        for tipo, var in quantificadores:
            if tipo == 'A':
                vars_universais.append(var)
            elif tipo == 'E':
                self.contador_skolem += 1
                
                if vars_universais:
                    # Função de Skolem
                    args = ','.join(vars_universais)
                    skolem = f"f{self.contador_skolem}({args})"
                else:
                    # Constante de Skolem
                    skolem = f"c{self.contador_skolem}"
                    # Usar subscrito para formato da imagem
                    constantes_usadas.append(f"c{self._subscrito(self.contador_skolem)}")
                
                resultado = self._substituir_variavel(resultado, var, skolem)
        
        # Formatar constantes para exibição
        resultado = self._formatar_constantes(resultado)
        
        return resultado, constantes_usadas

    def _subscrito(self, num):
        """Converte número para subscrito unicode."""
        subscripts = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
                      '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'}
        return ''.join(subscripts.get(c, c) for c in str(num))

    def _formatar_constantes(self, formula):
        """Formata c1, c2 para c₁, c₂."""
        resultado = formula
        for i in range(1, 10):
            resultado = resultado.replace(f"c{i}", f"c{self._subscrito(i)}")
            resultado = resultado.replace(f"f{i}", f"f{self._subscrito(i)}")
        return resultado

    def _substituir_variavel(self, formula, var, valor):
        """Substitui variável por valor dentro de predicados."""
        resultado = []
        i = 0
        
        while i < len(formula):
            if formula[i].isupper() and i + 1 < len(formula) and formula[i+1] == '(':
                pred = formula[i]
                i += 2
                args = ""
                nivel = 1
                while i < len(formula) and nivel > 0:
                    if formula[i] == '(':
                        nivel += 1
                    elif formula[i] == ')':
                        nivel -= 1
                    if nivel == 0:
                        break
                    args += formula[i]
                    i += 1
                i += 1
                
                novos_args = []
                for arg in args.split(','):
                    arg = arg.strip()
                    if arg == var:
                        novos_args.append(valor)
                    else:
                        novos_args.append(arg)
                
                resultado.append(f"{pred}({','.join(novos_args)})")
            else:
                resultado.append(formula[i])
                i += 1
        
        return ''.join(resultado)

    def _formatar_saida(self, formula):
        """
        Usa - para negação e v para disjunção (minúsculo).
        """
        f = formula
        # Quantificadores
        f = re.sub(r'\(A([a-z])\)', r'(∀\1)', f)
        f = re.sub(r'\(E([a-z])\)', r'(∃\1)', f)
        # Mantém - para negação (como na imagem)
        # Mantém v minúsculo para disjunção (como na imagem)
        f = f.replace(' V ', ' v ')
        f = f.replace('V', ' v ')
        # Remove espaços extras
        f = re.sub(r'\s+', ' ', f).strip()
        return f

    def get_latex(self, formula):
        """Gera representação LaTeX."""
        self.processar(formula)

        latex = []
        latex.append("\\documentclass{article}")
        latex.append("\\usepackage{amsmath, amssymb}")
        latex.append("\\usepackage[utf8]{inputenc}")
        latex.append("\\begin{document}")
        latex.append("")
        latex.append("\\section*{Skolemização e Forma Normal Prenex}")
        latex.append("")
        latex.append("\\textbf{Fórmula Original:}")
        latex.append(f"\\[ {self._para_latex(formula)} \\]")
        latex.append("")

        for i, (nome, resultado) in enumerate(self.passos_detalhados, 1):
            latex.append(f"\\textbf{{Passo {i}: {nome}}}")
            latex.append(f"\\[ {self._para_latex(resultado)} \\]")
            latex.append("")

        latex.append("\\end{document}")
        return "\n".join(latex)

    def _para_latex(self, formula):
        """Converte para LaTeX."""
        f = formula
        f = re.sub(r'\(A([a-z])\)', r'\\forall \1\\,', f)
        f = re.sub(r'\(E([a-z])\)', r'\\exists \1\\,', f)
        f = f.replace("->", "\\rightarrow ")
        f = f.replace("<->", "\\leftrightarrow ")
        f = f.replace("-", "\\neg ")
        f = f.replace("~", "\\neg ")
        f = f.replace("&", "\\land ")
        f = f.replace(" v ", " \\lor ")
        f = f.replace(" V ", " \\lor ")
        return f


# =============================================================================
# EXPORTADOR LATEX
# =============================================================================

class ExportadorLatex:
    """Exporta provas para formato LaTeX."""

    @staticmethod
    def gerar_prova_proposicional(premissas, conclusao, valido, forma, tabela, contraexemplo=None):
        latex = []
        latex.append("\\documentclass[12pt]{article}")
        latex.append("\\usepackage[utf8]{inputenc}")
        latex.append("\\usepackage[brazil]{babel}")
        latex.append("\\usepackage{amsmath, amssymb, amsthm}")
        latex.append("\\usepackage{array}")
        latex.append("")
        latex.append("\\title{Verificação de Argumento Lógico}")
        latex.append("\\date{\\today}")
        latex.append("")
        latex.append("\\begin{document}")
        latex.append("\\maketitle")
        latex.append("")
        latex.append("\\section{Argumento}")
        latex.append("\\textbf{Premissas:}")
        latex.append("\\begin{enumerate}")
        for p in premissas:
            if p.strip():
                latex.append(f"  \\item ${ExportadorLatex._converter_formula(p)}$")
        latex.append("\\end{enumerate}")
        latex.append(f"\\textbf{{Conclusão:}} ${ExportadorLatex._converter_formula(conclusao)}$")
        latex.append("")
        latex.append("\\section{Resultado}")
        status = "VÁLIDO" if valido else "INVÁLIDO"
        latex.append(f"\\textbf{{Status:}} {status}")
        latex.append(f"\\textbf{{Forma identificada:}} {forma}")

        if not valido and contraexemplo:
            latex.append("")
            latex.append("\\subsection{Contraexemplo}")
            latex.append("\\begin{itemize}")
            for var, val in contraexemplo.items():
                latex.append(f"  \\item ${var} = {'V' if val else 'F'}$")
            latex.append("\\end{itemize}")

        latex.append("\\end{document}")
        return "\n".join(latex)

    @staticmethod
    def gerar_prova_predicados(premissas, conclusao, dominio, valido, passos):
        latex = []
        latex.append("\\documentclass[12pt]{article}")
        latex.append("\\usepackage[utf8]{inputenc}")
        latex.append("\\usepackage{amsmath, amssymb}")
        latex.append("")
        latex.append("\\title{Verificação - Lógica de Predicados}")
        latex.append("\\date{\\today}")
        latex.append("")
        latex.append("\\begin{document}")
        latex.append("\\maketitle")
        latex.append(f"\\textbf{{Domínio:}} ${dominio}$")
        latex.append("")
        latex.append("\\textbf{Premissas:}")
        latex.append("\\begin{enumerate}")
        for p in premissas:
            if p.strip():
                latex.append(f"  \\item ${ExportadorLatex._converter_formula(p)}$")
        latex.append("\\end{enumerate}")
        latex.append(f"\\textbf{{Conclusão:}} ${ExportadorLatex._converter_formula(conclusao)}$")
        status = "VÁLIDO" if valido else "INVÁLIDO"
        latex.append(f"\\textbf{{Resultado:}} {status}")

        if passos:
            latex.append("")
            latex.append("\\section{Passos}")
            latex.append("\\begin{enumerate}")
            for p in passos:
                latex.append(f"  \\item {p}")
            latex.append("\\end{enumerate}")

        latex.append("\\end{document}")
        return "\n".join(latex)

    @staticmethod
    def _converter_formula(formula):
        f = formula
        f = f.replace("(Ax)", "\\forall x\\,")
        f = f.replace("(Ay)", "\\forall y\\,")
        f = f.replace("(Ex)", "\\exists x\\,")
        f = f.replace("(Ey)", "\\exists y\\,")
        f = f.replace("->", "\\rightarrow ")
        f = f.replace("<->", "\\leftrightarrow ")
        f = f.replace("~", "\\neg ")
        f = f.replace("&", "\\land ")
        f = f.replace(" V ", " \\lor ")
        return f


# =============================================================================
# INTERFACE GRÁFICA
# =============================================================================

class AppVerificador:
    """Interface gráfica principal do sistema."""

    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho de MD Toppissimo")
        self.root.geometry("1000x750")

        self.motor = MotorLogico()
        self.predicados = MotorPredicados(self.motor)
        self.skolem = Skolemizador()

        self.ultimo_resultado = {}

        self.criar_menu()
        self.criar_tabs()

    def criar_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Exportar LaTeX...", command=self.exportar_latex)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Limpar Tudo", command=self.limpar_tudo)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.root.quit)

        ajuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Sintaxe", command=self.mostrar_sintaxe)
        ajuda_menu.add_command(label="Sobre", command=self.mostrar_sobre)

    def criar_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        self.tab3 = ttk.Frame(tab_control)

        tab_control.add(self.tab1, text=' Lógica Proposicional ')
        tab_control.add(self.tab2, text=' Lógica de Predicados ')
        tab_control.add(self.tab3, text=' Skolemização / FNP ')

        tab_control.pack(expand=1, fill="both", padx=5, pady=5)

        self.setup_tab_proposicional()
        self.setup_tab_predicados()
        self.setup_tab_skolem()

    # =========================================================================
    # ABA 1: LÓGICA PROPOSICIONAL
    # =========================================================================

    def setup_tab_proposicional(self):
        tab = self.tab1
        frame_entrada = ttk.LabelFrame(tab, text=" Entrada do Argumento ", padding=10)
        frame_entrada.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_entrada,
                  text="Operadores:  ~ (negação)   & (conjunção)   V (disjunção)   -> (implicação)   <-> (bicondicional)",
                  font=("Arial", 9)).pack(anchor="w", pady=(0, 10))

        ttk.Separator(frame_entrada, orient="horizontal").pack(fill="x", pady=5)

        ttk.Label(frame_entrada, text="Premissas (uma por linha):",
                  font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))

        self.txt_prop_prem = tk.Text(frame_entrada, height=4, width=80,
                                      relief="solid", bd=1, font=("Consolas", 10))
        self.txt_prop_prem.pack(fill="x", pady=(0, 10))

        ttk.Separator(frame_entrada, orient="horizontal").pack(fill="x", pady=5)

        ttk.Label(frame_entrada, text="Conclusão:",
                  font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))

        self.txt_prop_conc = ttk.Entry(frame_entrada, width=80, font=("Consolas", 10))
        self.txt_prop_conc.pack(fill="x", pady=(0, 5))

        frame_btns = ttk.Frame(tab)
        frame_btns.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_btns, text="Verificar",
                   command=self.executar_proposicional).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Exportar LaTeX",
                   command=self.exportar_latex_prop).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Limpar",
                   command=lambda: self.limpar_aba(1)).pack(side="right", padx=5)

        frame_resultado = ttk.LabelFrame(tab, text=" Resultado ", padding=10)
        frame_resultado.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_prop_resultado = scrolledtext.ScrolledText(
            frame_resultado, height=15, font=("Consolas", 10),
            relief="solid", bd=1)
        self.txt_prop_resultado.pack(fill="both", expand=True)

    def executar_proposicional(self):
        premissas = self.txt_prop_prem.get("1.0", tk.END).splitlines()
        conclusao = self.txt_prop_conc.get()

        if not conclusao.strip():
            messagebox.showwarning("Aviso", "Por favor, insira uma conclusão.")
            return

        premissas = [p.strip() for p in premissas if p.strip()]

        resultado = self.motor.validar_argumento(premissas, conclusao)

        self.ultimo_resultado = {
            'tipo': 'proposicional',
            'premissas': premissas,
            'conclusao': conclusao,
            'valido': resultado['valido'],
            'forma': resultado['forma'],
            'tabela': resultado['tabela'],
            'contraexemplo': resultado['contraexemplo']
        }

        linhas = ["═" * 60]
        linhas.append("ANÁLISE DO ARGUMENTO")
        linhas.append("═" * 60)
        linhas.append("")
        linhas.append(f"Forma identificada: {resultado['forma']}")
        linhas.append("")

        if resultado['valido']:
            linhas.append("STATUS: ✓ VÁLIDO (Tautologia)")
        else:
            linhas.append("STATUS: ✗ INVÁLIDO")
            if resultado['contraexemplo']:
                linhas.append("")
                linhas.append("Contraexemplo encontrado:")
                for var, val in resultado['contraexemplo'].items():
                    linhas.append(f"  {var} = {'V' if val else 'F'}")

        linhas.append("")
        linhas.append("═" * 60)
        linhas.append("TABELA VERDADE")
        linhas.append("═" * 60)
        linhas.append(resultado['tabela'])

        self.txt_prop_resultado.delete("1.0", tk.END)
        self.txt_prop_resultado.insert(tk.END, "\n".join(linhas))

    def exportar_latex_prop(self):
        if not self.ultimo_resultado or self.ultimo_resultado.get('tipo') != 'proposicional':
            messagebox.showwarning("Aviso", "Execute uma verificação primeiro.")
            return

        r = self.ultimo_resultado
        latex = ExportadorLatex.gerar_prova_proposicional(
            r['premissas'], r['conclusao'], r['valido'],
            r['forma'], r['tabela'], r['contraexemplo']
        )
        self._salvar_latex(latex)

    # =========================================================================
    # ABA 2: LÓGICA DE PREDICADOS
    # =========================================================================

    def setup_tab_predicados(self):
        tab = self.tab2
        frame_entrada = ttk.LabelFrame(tab, text=" Entrada do Argumento ", padding=10)
        frame_entrada.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_entrada,
                  text="Quantificadores:  (Ax) ou (∀x) = Universal   |   (Ex) ou (∃x) = Existencial",
                  font=("Arial", 9)).pack(anchor="w", pady=(0, 10))

        ttk.Separator(frame_entrada, orient="horizontal").pack(fill="x", pady=5)

        ttk.Label(frame_entrada, text="Domínio:",
                  font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))

        self.txt_pred_dom = ttk.Entry(frame_entrada, width=50, font=("Consolas", 10))
        self.txt_pred_dom.insert(0, "{1, 2, 3}")
        self.txt_pred_dom.pack(anchor="w", pady=(0, 10))

        ttk.Separator(frame_entrada, orient="horizontal").pack(fill="x", pady=5)

        ttk.Label(frame_entrada, text="Premissas (uma por linha):",
                  font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))

        self.txt_pred_prem = tk.Text(frame_entrada, height=4, width=80,
                                      relief="solid", bd=1, font=("Consolas", 10))
        self.txt_pred_prem.pack(fill="x", pady=(0, 10))

        ttk.Separator(frame_entrada, orient="horizontal").pack(fill="x", pady=5)

        ttk.Label(frame_entrada, text="Conclusão:",
                  font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))

        self.txt_pred_conc = ttk.Entry(frame_entrada, width=80, font=("Consolas", 10))
        self.txt_pred_conc.pack(fill="x", pady=(0, 5))

        frame_btns = ttk.Frame(tab)
        frame_btns.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_btns, text="Validar",
                   command=self.executar_predicados).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Exportar LaTeX",
                   command=self.exportar_latex_pred).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Limpar",
                   command=lambda: self.limpar_aba(2)).pack(side="right", padx=5)

        frame_resultado = ttk.LabelFrame(tab, text=" Resultado ", padding=10)
        frame_resultado.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_pred_resultado = scrolledtext.ScrolledText(
            frame_resultado, height=12, font=("Consolas", 10),
            relief="solid", bd=1)
        self.txt_pred_resultado.pack(fill="both", expand=True)

    def executar_predicados(self):
        try:
            dominio = self.txt_pred_dom.get()
            premissas = self.txt_pred_prem.get("1.0", tk.END).splitlines()
            conclusao = self.txt_pred_conc.get()

            if not conclusao.strip():
                messagebox.showwarning("Aviso", "Por favor, insira uma conclusão.")
                return

            premissas = [p.strip() for p in premissas if p.strip()]

            resultado = self.predicados.validar(premissas, conclusao, dominio)

            linhas = []
            linhas.append("Entrada:")
            
            # Parse domínio para exibição
            dom = [x.strip() for x in dominio.replace("{", "").replace("}", "").split(",") if x.strip()]
            linhas.append(f"Domínio: {{{', '.join(dom)}}}")
            
            for i, p in enumerate(premissas):
                linhas.append(f"Premissa {i+1}: {p}")
            linhas.append(f"Conclusão: {conclusao}")
            linhas.append("")
            
            # Adiciona o relatório.
            linhas.append(resultado['relatorio_texto'])

            self.txt_pred_resultado.delete("1.0", tk.END)
            self.txt_pred_resultado.insert(tk.END, "\n".join(linhas))

            self.ultimo_resultado = {
                'tipo': 'predicados',
                'premissas': premissas,
                'conclusao': conclusao,
                'dominio': dominio,
                'valido': resultado['valido'],
                'passos': resultado['passos']
            }

        except Exception as e:
            self.txt_pred_resultado.delete("1.0", tk.END)
            self.txt_pred_resultado.insert(tk.END, f"Erro ao processar: {str(e)}")

    def exportar_latex_pred(self):
        if not self.ultimo_resultado or self.ultimo_resultado.get('tipo') != 'predicados':
            messagebox.showwarning("Aviso", "Execute uma verificação primeiro.")
            return
        r = self.ultimo_resultado
        latex = ExportadorLatex.gerar_prova_predicados(
            r['premissas'], r['conclusao'], r['dominio'],
            r['valido'], r['passos']
        )
        self._salvar_latex(latex)

    # =========================================================================
    # ABA 3: SKOLEMIZAÇÃO
    # =========================================================================

    def setup_tab_skolem(self):
        tab = self.tab3
        frame_entrada = ttk.LabelFrame(tab, text=" Fórmula para Processar ", padding=10)
        frame_entrada.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(frame_entrada,
                  text="Digite uma fórmula com quantificadores (ex: (∀x)P(x) -> (∃y)Q(y)):",
                  font=("Arial", 9)).pack(anchor="w", pady=(0, 5))
        
        self.txt_skolem_entrada = ttk.Entry(frame_entrada, width=80, font=("Consolas", 11))
        self.txt_skolem_entrada.pack(fill="x", pady=5)
        
        frame_btns = ttk.Frame(tab)
        frame_btns.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(frame_btns, text="Processar",
                   command=self.executar_skolem).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Exemplo 1",
                   command=lambda: self.exemplo_skolem(1)).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Exemplo 2",
                   command=lambda: self.exemplo_skolem(2)).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Exportar LaTeX",
                   command=self.exportar_latex_skolem).pack(side="left", padx=5)
        
        frame_resultado = ttk.LabelFrame(tab, text=" Passos da Conversão ", padding=10)
        frame_resultado.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.txt_skolem_resultado = scrolledtext.ScrolledText(
            frame_resultado, height=20, font=("Consolas", 10), relief="solid", bd=1)
        self.txt_skolem_resultado.pack(fill="both", expand=True)

    def executar_skolem(self):
        formula = self.txt_skolem_entrada.get().strip()
        if not formula:
            messagebox.showwarning("Aviso", "Por favor, insira uma fórmula.")
            return
        
        resultado = self.skolem.processar(formula)
        self.txt_skolem_resultado.delete("1.0", tk.END)
        self.txt_skolem_resultado.insert(tk.END, resultado)
        
        self.ultimo_resultado = {
            'tipo': 'skolem',
            'formula': formula
        }

    def exemplo_skolem(self, num):
        self.txt_skolem_entrada.delete(0, tk.END)
        if num == 1:
            self.txt_skolem_entrada.insert(0, "(Ax)P(x) -> (Ey)Q(y)")
        else:
            self.txt_skolem_entrada.insert(0, "(Ax)(Ey)(P(x) -> Q(x,y))")
        self.executar_skolem()

    def exportar_latex_skolem(self):
        if not self.ultimo_resultado or self.ultimo_resultado.get('tipo') != 'skolem':
            messagebox.showwarning("Aviso", "Execute uma Skolemização primeiro.")
            return
        latex = self.skolem.get_latex(self.ultimo_resultado['formula'])
        self._salvar_latex(latex)

    # =========================================================================
    # MÉTODOS AUXILIARES
    # =========================================================================

    def _salvar_latex(self, latex):
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".tex",
            filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")],
            title="Salvar LaTeX"
        )
        if arquivo:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(latex.replace("\\\\", "\\"))
            messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{arquivo}")

    def exportar_latex(self):
        if not self.ultimo_resultado:
            messagebox.showwarning("Aviso", "Execute uma verificação primeiro.")
            return

        tipo = self.ultimo_resultado.get('tipo')
        if tipo == 'proposicional':
            self.exportar_latex_prop()
        elif tipo == 'predicados':
            self.exportar_latex_pred()
        elif tipo == 'skolem':
            self.exportar_latex_skolem()

    def limpar_aba(self, aba):
        if aba == 1:
            self.txt_prop_prem.delete("1.0", tk.END)
            self.txt_prop_conc.delete(0, tk.END)
            self.txt_prop_resultado.delete("1.0", tk.END)
        elif aba == 2:
            self.txt_pred_prem.delete("1.0", tk.END)
            self.txt_pred_conc.delete(0, tk.END)
            self.txt_pred_resultado.delete("1.0", tk.END)

    def limpar_tudo(self):
        self.limpar_aba(1)
        self.limpar_aba(2)
        self.txt_skolem_entrada.delete(0, tk.END)
        self.txt_skolem_resultado.delete("1.0", tk.END)
        self.ultimo_resultado = {}

    def mostrar_sintaxe(self):
        top = tk.Toplevel(self.root)
        top.title("Ajuda - Sintaxe")
        top.geometry("550x500")
        texto = scrolledtext.ScrolledText(top, font=("Consolas", 10))
        texto.pack(fill="both", expand=True, padx=10, pady=10)
        ajuda = """═══ SINTAXE SUPORTADA ═══

LÓGICA PROPOSICIONAL
────────────────────────────────────
Variáveis: P, Q, R, S, ... (letras maiúsculas)

Operadores:
  ~      Negação (NÃO)
  &      Conjunção (E)
  V      Disjunção (OU)
  ->     Implicação (SE...ENTÃO)
  <->    Bicondicional (SE E SOMENTE SE)

Exemplos:
  P -> Q
  (P & Q) -> R
  P V ~Q

LÓGICA DE PREDICADOS
────────────────────────────────────
Quantificador Universal:   (Ax) ou (∀x) - "Para todo x"
Quantificador Existencial: (Ex) ou (∃x) - "Existe x"

Predicados: P(x), Q(x,y), H(a), M(s), etc.
Domínio: {a, b, c} ou {1, 2, 3}

Exemplos:
  (Ax)P(x)
  (Ax)(P(x) -> Q(x))
  (Ex)(P(x) & Q(x))
  (Ax)(Ey)R(x,y)

FORMAS DE ARGUMENTO RECONHECIDAS
────────────────────────────────────
Válidas:
  • Modus Ponens: P->Q, P |- Q
  • Modus Tollens: P->Q, ~Q |- ~P
  • Silogismo Disjuntivo: PVQ, ~P |- Q
  • Silogismo Hipotético: P->Q, Q->R |- P->R

Falácias:
  • Afirmação do Consequente: P->Q, Q |- P
  • Negação do Antecedente: P->Q, ~P |- ~Q
"""
        texto.insert(tk.END, ajuda)
        texto.configure(state="disabled")

    def mostrar_sobre(self):
        sobre = """Trabalho de Implementação
Disciplina: Matemática Discreta

Autores:
  • Chrysthyan
  • Marcos V. Gonzaga
  • Thiago Willian
  • Eric Gabriel

Funcionalidades:
  ✓ Parser de fórmulas proposicionais
  ✓ Verificador por Tabela Verdade
  ✓ Identificador de Forma de Argumento
  ✓ Lógica de Predicados
  ✓ Validação em domínio finito
  ✓ Forma Normal Prenex (FNP)
  ✓ Skolemização
  ✓ Exportação para LaTeX"""
        messagebox.showinfo("Sobre", sobre)


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = AppVerificador(root)
    root.mainloop()
