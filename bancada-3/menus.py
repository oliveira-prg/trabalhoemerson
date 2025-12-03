from tabela_verdade import tabela_verdade
from formas_argumento import identificar_forma
from avaliador_predicados import avaliar_predicados
from utils import clear_screen
from testes_logica import CASOS_TESTE, executar_teste

def menu_proposicional():
    clear_screen()
    print("\n--- Lógica Proposicional ---")
    try:
        n = int(input("Número de premissas: "))
    except ValueError:
        print("Entrada inválida.")
        input("Pressione Enter para voltar...")
        return

    premissas = []
    for i in range(n):
        p = input(f"Premissa {i+1}: ")
        premissas.append(p)
    conclusao = input("Conclusão: ")
    
    print("\nAnalisando...")
    ok, contra_exemplos = tabela_verdade(premissas, conclusao)
    forma = identificar_forma(premissas, conclusao)
    
    print("\n-------------------------------------------------")
    print("SAÍDA:")
    if ok:
        print("✓ ARGUMENTO VÁLIDO")
    else:
        print("✗ ARGUMENTO INVÁLIDO")
    
    print("Método: Tabela Verdade")
    print("Forma detectada:", forma)
    
    if ok:
        print("Justificativa: Em todas as linhas onde as premissas são verdadeiras, a conclusão também é verdadeira.")
    else:
        print("Justificativa: Existe pelo menos uma linha onde as premissas são verdadeiras mas a conclusão é falsa.")
        if len(contra_exemplos) > 0:
            print("Contra-exemplo encontrado:", contra_exemplos[0])
    input("\nPressione Enter para voltar ao menu...")

def menu_predicados():
    clear_screen()
    print("\n--- Lógica de Predicados (Básico) ---")
    dominio_str = input("Domínio (ex: a,b,c): ")
    dominio = dominio_str.replace(" ", "").split(",")
    
    try:
        n = int(input("Número de premissas: "))
    except ValueError:
        print("Entrada inválida.")
        input("Pressione Enter para voltar...")
        return

    premissas = []
    for i in range(n):
        p = input(f"Premissa {i+1}: ")
        premissas.append(p)
    conclusao = input("Conclusão: ")
    
    ok, contra_exemplo = avaliar_predicados(premissas, conclusao, dominio)
    
    print("\n-------------------------------------------------")
    print("SAÍDA:")
    if ok:
        print("✓ ARGUMENTO VÁLIDO")
    else:
        print("✗ ARGUMENTO INVÁLIDO")
    
    print("Método: Enumeração em domínio finito")
    print("Justificativa: Para todas as interpretações possíveis no domínio dado, a conclusão segue das premissas.")
    print("Regra aplicada: Verificação exaustiva de modelos.")
    if not ok:
        print("Justificativa: Encontrada uma interpretação onde as premissas são verdadeiras e a conclusão é falsa.")
        if contra_exemplo:
            pass
    input("\nPressione Enter para voltar ao menu...")

def menu_ajuda():
    clear_screen()
    print("\n=== AJUDA E EXEMPLOS ===")
    print("1 - Sintaxe e Exemplos: Lógica Proposicional")
    print("2 - Sintaxe e Exemplos: Lógica de Predicados")
    print("3 - Voltar")
    
    op = input("> ")
    
    if op == "1":
        clear_screen()
        print("\n--- LÓGICA PROPOSICIONAL ---")
        print("Operadores Suportados:")
        print("  ~      : Negação (NÃO)")
        print("  & ou ∧ : Conjunção (E)")
        print("  | ou ∨ : Disjunção (OU)")
        print("  ->     : Implicação (Se... então)")
        print("  <->    : Bicondicional (Se e somente se)")
        print("\nExemplo de Argumento Válido (Modus Ponens):")
        print("  Premissa 1: P -> Q")
        print("  Premissa 2: P")
        print("  Conclusão : Q")
        print("\nExemplo de Argumento Inválido (Falácia da Afirmação do Consequente):")
        print("  Premissa 1: P -> Q")
        print("  Premissa 2: Q")
        print("  Conclusão : P")
        input("\nPressione Enter para voltar...")
        
    elif op == "2":
        clear_screen()
        print("\n--- LÓGICA DE PREDICADOS ---")
        print("Sintaxe:")
        print("  Predicados: Letras maiúsculas seguidas de argumentos entre parênteses. Ex: P(x), G(a,b)")
        print("  Quantificadores:")
        print("    (∀x) : Universal (Para todo x)")
        print("    (∃x) : Existencial (Existe um x)")
        print("  Nota: Os quantificadores devem estar entre parênteses e usar as variáveis do domínio.")
        print("  Domínio: Lista de elementos separados por vírgula. Ex: a,b,c")
        print("\nExemplo (Sócrates):")
        print("  Domínio   : socrates, platao")
        print("  Premissa 1: (∀x)(H(x) -> M(x))  [Todo homem é mortal]")
        print("  Premissa 2: H(socrates)         [Sócrates é homem]")
        print("  Conclusão : M(socrates)         [Sócrates é mortal]")
        input("\nPressione Enter para voltar...")

def menu_testes_obrigatorios():
    while True:
        clear_screen()
        print("\n=== CASOS DE TESTE OBRIGATÓRIOS ===")
        print("Lógica Proposicional:")
        for teste in CASOS_TESTE:
            if teste["tipo"] == "prop":
                print(f" {teste['id']}. {teste['nome']}")
                print(f"    {teste['desc']}")
        
        print("\nLógica de Predicados:")
        for teste in CASOS_TESTE:
            if teste["tipo"] == "pred":
                print(f" {teste['id']}. {teste['nome']}")
                print(f"    {teste['desc']}")
                
        print("\n0. Voltar")
        
        op = input("\nEscolha um teste (número): ")
        
        if op == "0":
            break
            
        try:
            idx = int(op)
            encontrado = False
            for i, t in enumerate(CASOS_TESTE):
                if t["id"] == idx:
                    executar_teste(i)
                    encontrado = True
                    break
            
            if not encontrado:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
        except ValueError:
            print("Entrada inválida!")
            input("Pressione Enter para continuar...")
