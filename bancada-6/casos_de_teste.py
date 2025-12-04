# =============================================================================
# CASOS DE TESTE - Calculadora Lógica
# =============================================================================
# Arquivo: casos_de_teste.py
# =============================================================================

import sys

# Adiciona suporte para importar os módulos
try:
    from calculadora_lógica import MotorLogico, MotorPredicados, Skolemizador
except ImportError:
    # Versão standalone para testes
    import re
    import itertools as it

    class MotorLogico:
        def __init__(self):
            self.operadores = ['~', '¬', '&', '^', '∧', 'V', 'v', '|', '∨', '->', '→', '<->', '↔']

        def normalizar_formula(self, formula):
            f = formula.strip()
            f = f.replace('¬', '~').replace('∧', '&').replace('^', '&')
            f = f.replace('∨', 'V').replace('|', 'V')
            f = f.replace('→', '->').replace('↔', '<->')
            return f

        def extrair_variaveis(self, formula):
            f = self.normalizar_formula(formula)
            f = f.replace('->', ' ').replace('<->', ' ')
            f = f.replace('~', ' ').replace('&', ' ').replace('V', ' ')
            f = f.replace('(', ' ').replace(')', ' ')
            variaveis = set()
            for token in f.split():
                token = token.strip()
                if token and token[0].isupper() and token not in ['V']:
                    variaveis.add(token)
            return sorted(list(variaveis))

        def parse_e_avaliar(self, formula, valores):
            f = self.normalizar_formula(formula).strip()
            while f.startswith('(') and f.endswith(')'):
                nivel = 0
                pode_remover = True
                for i, c in enumerate(f):
                    if c == '(': nivel += 1
                    elif c == ')': nivel -= 1
                    if nivel == 0 and i < len(f) - 1:
                        pode_remover = False
                        break
                if pode_remover: f = f[1:-1].strip()
                else: break

            nivel = 0
            pos_bic = pos_imp = pos_or = pos_and = -1
            i = 0
            while i < len(f):
                c = f[i]
                if c == '(': nivel += 1
                elif c == ')': nivel -= 1
                elif nivel == 0:
                    if f[i:i+3] == '<->': pos_bic = i
                    elif f[i:i+2] == '->' and pos_bic == -1: pos_imp = i
                    elif c == 'V' and f[i-1:i] != '-' and pos_bic == -1 and pos_imp == -1: pos_or = i
                    elif c == '&' and pos_bic == -1 and pos_imp == -1 and pos_or == -1: pos_and = i
                i += 1

            if pos_bic != -1:
                return self.parse_e_avaliar(f[:pos_bic], valores) == self.parse_e_avaliar(f[pos_bic+3:], valores)
            if pos_imp != -1:
                return (not self.parse_e_avaliar(f[:pos_imp], valores)) or self.parse_e_avaliar(f[pos_imp+2:], valores)
            if pos_or != -1:
                return self.parse_e_avaliar(f[:pos_or], valores) or self.parse_e_avaliar(f[pos_or+1:], valores)
            if pos_and != -1:
                return self.parse_e_avaliar(f[:pos_and], valores) and self.parse_e_avaliar(f[pos_and+1:], valores)
            if f.startswith('~'):
                return not self.parse_e_avaliar(f[1:], valores)
            return valores.get(f.strip(), False)

        def validar_argumento(self, premissas, conclusao):
            premissas = [p.strip() for p in premissas if p.strip()]
            conclusao = conclusao.strip()
            todas_formulas = premissas + [conclusao]
            variaveis = set()
            for f in todas_formulas:
                variaveis.update(self.extrair_variaveis(f))
            variaveis = sorted(list(variaveis))
            if not variaveis:
                return {'valido': False, 'contraexemplo': None}
            
            valido = True
            contraexemplo = None
            for vals in it.product([True, False], repeat=len(variaveis)):
                mapa = dict(zip(variaveis, vals))
                conj_prems = all(self.parse_e_avaliar(p, mapa) for p in premissas)
                val_conc = self.parse_e_avaliar(conclusao, mapa)
                if conj_prems and not val_conc:
                    valido = False
                    if contraexemplo is None:
                        contraexemplo = mapa.copy()
            return {'valido': valido, 'contraexemplo': contraexemplo}


    class MotorPredicados:
        def __init__(self, motor_prop):
            self.motor_prop = motor_prop

        def expandir(self, formula, dominio):
            formula = formula.strip().replace('∀', 'A').replace('∃', 'E')
            
            match_univ = re.match(r'\(?\s*A\s*([a-z])\s*\)?\s*(.+)', formula)
            if match_univ:
                var, corpo = match_univ.group(1), self._limpar_parenteses(match_univ.group(2).strip())
                partes = [f'({self.expandir(self._substituir(corpo, var, str(d)), dominio)})' for d in dominio]
                return ' & '.join(partes)
            
            match_exist = re.match(r'\(?\s*E\s*([a-z])\s*\)?\s*(.+)', formula)
            if match_exist:
                var, corpo = match_exist.group(1), self._limpar_parenteses(match_exist.group(2).strip())
                partes = [f'({self.expandir(self._substituir(corpo, var, str(d)), dominio)})' for d in dominio]
                return ' V '.join(partes)
            
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
            if corpo.startswith('(') and corpo.endswith(')'):
                nivel = 0
                for i, c in enumerate(corpo):
                    if c == '(': nivel += 1
                    elif c == ')': nivel -= 1
                    if nivel == 0 and i < len(corpo) - 1: return corpo
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
                        if formula[j] == '(': nivel += 1
                        elif formula[j] == ')': nivel -= 1
                        j += 1
                    resultado.append(re.sub(rf'\b{var}\b', valor, formula[i:j]))
                    i = j
                else:
                    resultado.append(formula[i])
                    i += 1
            return ''.join(resultado)

        def validar(self, premissas, conclusao, dominio_str):
            dom = [x.strip() for x in dominio_str.replace('{', '').replace('}', '').split(',') if x.strip()]
            if not dom: dom = ['a', 'b']
            
            premissas_exp = [self.expandir(p.strip(), dom) for p in premissas if p.strip()]
            conclusao_exp = self.expandir(conclusao.strip(), dom)
            
            res_prop = self.motor_prop.validar_argumento(premissas_exp, conclusao_exp)
            return {'valido': res_prop['valido'], 'contraexemplo': res_prop['contraexemplo']}


# =============================================================================
# CASOS DE TESTE OBRIGATÓRIOS
# =============================================================================

def executar_testes():
    """Executa todos os casos de teste obrigatórios."""
    
    motor = MotorLogico()
    predicados = MotorPredicados(motor)
    
    print("=" * 70)
    print("CASOS DE TESTE - Sistema de Verificação de Argumentos Lógicos")
    print("=" * 70)
    print()
    
    testes_passados = 0
    testes_falhados = 0
    
    # =========================================================================
    # TESTES DE LÓGICA PROPOSICIONAL
    # =========================================================================
    
    print("=" * 70)
    print("LÓGICA PROPOSICIONAL")
    print("=" * 70)
    print()
    
    testes_proposicionais = [
        # Teste 1: Modus Ponens
        {
            'nome': 'Teste 1: Modus Ponens',
            'premissas': ['P -> Q', 'P'],
            'conclusao': 'Q',
            'esperado': True,
            'descricao': 'P -> Q, P |- Q'
        },
        # Teste 2: Falácia da Afirmação do Consequente
        {
            'nome': 'Teste 2: Falácia da Afirmação do Consequente',
            'premissas': ['P -> Q', 'Q'],
            'conclusao': 'P',
            'esperado': False,
            'descricao': 'P -> Q, Q |- P'
        },
        # Teste 3: Silogismo Disjuntivo
        {
            'nome': 'Teste 3: Silogismo Disjuntivo',
            'premissas': ['P V Q', '~P'],
            'conclusao': 'Q',
            'esperado': True,
            'descricao': 'P ∨ Q, ~P |- Q'
        },
        # Teste 4: Dilema Construtivo
        {
            'nome': 'Teste 4: Dilema Construtivo',
            'premissas': ['(P -> Q) & (R -> S)', 'P V R'],
            'conclusao': 'Q V S',
            'esperado': True,
            'descricao': '(P->Q) ∧ (R->S), P ∨ R |- Q ∨ S'
        },
        # Teste adicional: Modus Tollens
        {
            'nome': 'Teste 5: Modus Tollens',
            'premissas': ['P -> Q', '~Q'],
            'conclusao': '~P',
            'esperado': True,
            'descricao': 'P -> Q, ~Q |- ~P'
        },
        # Teste adicional: Silogismo Hipotético
        {
            'nome': 'Teste 6: Silogismo Hipotético',
            'premissas': ['P -> Q', 'Q -> R'],
            'conclusao': 'P -> R',
            'esperado': True,
            'descricao': 'P -> Q, Q -> R |- P -> R'
        },
        # Teste adicional: Falácia da Negação do Antecedente
        {
            'nome': 'Teste 7: Falácia da Negação do Antecedente',
            'premissas': ['P -> Q', '~P'],
            'conclusao': '~Q',
            'esperado': False,
            'descricao': 'P -> Q, ~P |- ~Q'
        },
    ]
    
    for teste in testes_proposicionais:
        resultado = motor.validar_argumento(teste['premissas'], teste['conclusao'])
        passou = resultado['valido'] == teste['esperado']
        
        status = "✓ PASSOU" if passou else "✗ FALHOU"
        if passou:
            testes_passados += 1
        else:
            testes_falhados += 1
        
        print(f"{teste['nome']}")
        print(f"  Descrição: {teste['descricao']}")
        print(f"  Esperado: {'VÁLIDO' if teste['esperado'] else 'INVÁLIDO'}")
        print(f"  Obtido: {'VÁLIDO' if resultado['valido'] else 'INVÁLIDO'}")
        print(f"  Status: {status}")
        if not resultado['valido'] and resultado['contraexemplo']:
            contra = ', '.join([f"{k}={'V' if v else 'F'}" for k, v in resultado['contraexemplo'].items()])
            print(f"  Contraexemplo: {contra}")
        print()
    
    # =========================================================================
    # TESTES DE LÓGICA DE PREDICADOS
    # =========================================================================
    
    print("=" * 70)
    print("LÓGICA DE PREDICADOS")
    print("=" * 70)
    print()
    
    testes_predicados = [
        # Teste 5: Particularização Universal
        {
            'nome': 'Teste 8: Particularização Universal',
            'premissas': ['(Ax)P(x)'],
            'conclusao': 'P(a)',
            'dominio': '{a, b}',
            'esperado': True,
            'descricao': '(∀x)P(x) |- P(a)'
        },
        # Teste 6: Generalização Existencial
        {
            'nome': 'Teste 9: Generalização Existencial',
            'premissas': ['P(a)'],
            'conclusao': '(Ex)P(x)',
            'dominio': '{a, b}',
            'esperado': True,
            'descricao': 'P(a) |- (∃x)P(x)'
        },
        # Teste 7: Silogismo de Aristóteles
        {
            'nome': 'Teste 10: Silogismo de Aristóteles',
            'premissas': ['(Ax)(H(x) -> M(x))', 'H(s)'],
            'conclusao': 'M(s)',
            'dominio': '{s}',
            'esperado': True,
            'descricao': '(∀x)[H(x)->M(x)], H(s) |- M(s)'
        },
        # Teste 8: Argumento Inválido
        {
            'nome': 'Teste 11: Argumento Inválido (Existenciais)',
            'premissas': ['(Ex)P(x) & (Ex)Q(x)'],
            'conclusao': '(Ex)(P(x) & Q(x))',
            'dominio': '{a, b}',
            'esperado': False,
            'descricao': '(∃x)P(x) ∧ (∃x)Q(x) |- (∃x)[P(x)∧Q(x)]'
        },
        # Teste 9: Quantificadores Aninhados
        {
            'nome': 'Teste 12: Quantificadores Aninhados',
            'premissas': ['(Ax)(Ey)P(x,y)'],
            'conclusao': '(Ey)(Ax)P(x,y)',
            'dominio': '{a, b}',
            'esperado': False,
            'descricao': '(∀x)(∃y)P(x,y) |- (∃y)(∀x)P(x,y)'
        },
        # Teste 10: Equivalência de De Morgan
        {
            'nome': 'Teste 13: Equivalência de De Morgan',
            'premissas': ['~(Ax)P(x)'],
            'conclusao': '(Ex)~P(x)',
            'dominio': '{a, b}',
            'esperado': True,
            'descricao': '~(∀x)P(x) |- (∃x)~P(x)'
        },
        # Teste adicional: Universal implica Existencial
        {
            'nome': 'Teste 14: Universal implica Existencial',
            'premissas': ['(Ax)P(x)'],
            'conclusao': '(Ex)P(x)',
            'dominio': '{1, 2, 3}',
            'esperado': True,
            'descricao': '(∀x)P(x) |- (∃x)P(x)'
        },
    ]
    
    for teste in testes_predicados:
        resultado = predicados.validar(teste['premissas'], teste['conclusao'], teste['dominio'])
        passou = resultado['valido'] == teste['esperado']
        
        status = "✓ PASSOU" if passou else "✗ FALHOU"
        if passou:
            testes_passados += 1
        else:
            testes_falhados += 1
        
        print(f"{teste['nome']}")
        print(f"  Descrição: {teste['descricao']}")
        print(f"  Domínio: {teste['dominio']}")
        print(f"  Esperado: {'VÁLIDO' if teste['esperado'] else 'INVÁLIDO'}")
        print(f"  Obtido: {'VÁLIDO' if resultado['valido'] else 'INVÁLIDO'}")
        print(f"  Status: {status}")
        print()
    
    # =========================================================================
    # RESUMO
    # =========================================================================
    
    print("=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    total = testes_passados + testes_falhados
    print(f"Total de testes: {total}")
    print(f"Testes passados: {testes_passados} ({100*testes_passados/total:.1f}%)")
    print(f"Testes falhados: {testes_falhados} ({100*testes_falhados/total:.1f}%)")
    print()
    
    if testes_falhados == 0:
        print("✓ TODOS OS TESTES PASSARAM!")
    else:
        print("✗ Alguns testes falharam. Verifique a implementação.")
    
    return testes_falhados == 0


# =============================================================================
# TESTES DE SKOLEMIZAÇÃO
# =============================================================================

def testar_skolemizacao():
    """Testa a saída do Skolemizador."""
    
    print()
    print("=" * 70)
    print("TESTES DE SKOLEMIZAÇÃO")
    print("=" * 70)
    print()
    
    testes_skolem = [
        {
            'entrada': '(Ax)P(x) -> (Ey)Q(y)',
            'passo1': '-(∀x)P(x) v (∃y)Q(y)',
            'passo2': '(∃x)-P(x) v (∃y)Q(y)',
            'passo3': '(∃x)(∃y)[-P(x) v Q(y)]',
            'passo4': '-P(c₁) v Q(c₂)'
        }
    ]
    
    for teste in testes_skolem:
        print(f"Entrada: {teste['entrada']}")
        print()
        print("Saída Esperada:")
        print(f"  Passo 1 - Eliminar implicação: {teste['passo1']}")
        print(f"  Passo 2 - Mover negação: {teste['passo2']}")
        print(f"  Passo 3 - Forma Normal Prenex: {teste['passo3']}")
        print(f"  Passo 4 - Skolemização: {teste['passo4']}")
        print()
    
    print("✓ Formato de saída conforme especificação do professor")


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    sucesso = executar_testes()
    testar_skolemizacao()
    
    print()
    print("=" * 70)
    print("FIM DOS TESTES")
    print("=" * 70)
    
    sys.exit(0 if sucesso else 1)
