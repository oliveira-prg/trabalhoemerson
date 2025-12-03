from tabela_verdade import tabela_verdade
from formas_argumento import identificar_forma
from avaliador_predicados import avaliar_predicados
from utils import clear_screen

CASOS_TESTE = [
    {
        "id": 1,
        "nome": "Modus Ponens",
        "tipo": "prop",
        "premissas": ["P -> Q", "P"],
        "conclusao": "Q",
        "desc": "P -> Q, P |- Q (VÁLIDO)"
    },
    {
        "id": 2,
        "nome": "Falácia da Afirmação do Consequente",
        "tipo": "prop",
        "premissas": ["P -> Q", "Q"],
        "conclusao": "P",
        "desc": "P -> Q, Q |- P (INVÁLIDO)"
    },
    {
        "id": 3,
        "nome": "Silogismo Disjuntivo",
        "tipo": "prop",
        "premissas": ["P v Q", "~P"],
        "conclusao": "Q",
        "desc": "P v Q, ~P |- Q (VÁLIDO)"
    },
    {
        "id": 4,
        "nome": "Dilema Construtivo",
        "tipo": "prop",
        "premissas": ["(P->Q) & (R->S)", "P v R"],
        "conclusao": "Q v S",
        "desc": "(P->Q) & (R->S), P v R |- Q v S (VÁLIDO)"
    },
    {
        "id": 5,
        "nome": "Particularização Universal",
        "tipo": "pred",
        "dominio": ["a"],
        "premissas": ["(∀x)P(x)"],
        "conclusao": "P(a)",
        "desc": "(∀x)P(x) |- P(a) (VÁLIDO)"
    },
    {
        "id": 6,
        "nome": "Generalização Existencial",
        "tipo": "pred",
        "dominio": ["a"],
        "premissas": ["P(a)"],
        "conclusao": "(∃x)P(x)",
        "desc": "P(a) |- (∃x)P(x) (VÁLIDO)"
    },
    {
        "id": 7,
        "nome": "Silogismo de Aristóteles",
        "tipo": "pred",
        "dominio": ["socrates"],
        "premissas": ["(∀x)(H(x)->M(x))", "H(socrates)"],
        "conclusao": "M(socrates)",
        "desc": "(∀x)[H(x)->M(x)], H(s) |- M(s) (VÁLIDO)"
    },
    {
        "id": 8,
        "nome": "Argumento Inválido (Predicados)",
        "tipo": "pred",
        "dominio": ["a", "b"],
        "premissas": ["(∃x)P(x)", "(∃x)Q(x)"],
        "conclusao": "(∃x)(P(x) & Q(x))",
        "desc": "(∃x)P(x) & (∃x)Q(x) |- (∃x)[P(x)&Q(x)] (INVÁLIDO)"
    },
    {
        "id": 9,
        "nome": "Quantificadores Aninhados",
        "tipo": "pred",
        "dominio": ["a", "b"],
        "premissas": ["(∀x)(∃y)P(x,y)"],
        "conclusao": "(∃y)(∀x)P(x,y)",
        "desc": "(∀x)(∃y)P(x,y) |- (∃y)(∀x)P(x,y) (INVÁLIDO)"
    },
    {
        "id": 10,
        "nome": "Equivalência de De Morgan",
        "tipo": "pred",
        "dominio": ["a", "b"],
        "premissas": ["~(∀x)P(x)"],
        "conclusao": "(∃x)~P(x)",
        "desc": "~(∀x)P(x) |- (∃x)~P(x) (VÁLIDO)"
    }
]

def executar_teste(indice):
    if indice < 0 or indice >= len(CASOS_TESTE):
        print("Índice inválido.")
        return

    teste = CASOS_TESTE[indice]
    clear_screen()
    print(f"\n--- EXECUTANDO TESTE {teste['id']}: {teste['nome']} ---")
    print(f"Descrição: {teste['desc']}")
    
    print("\nEntradas:")
    if teste["tipo"] == "pred":
        print(f"Domínio: {', '.join(teste['dominio'])}")
    
    for i, p in enumerate(teste["premissas"]):
        print(f"Premissa {i+1}: {p}")
    print(f"Conclusão: {teste['conclusao']}")
    
    print("\nAnalisando...")
    
    if teste["tipo"] == "prop":
        ok, contra_exemplos = tabela_verdade(teste["premissas"], teste["conclusao"])
        forma = identificar_forma(teste["premissas"], teste["conclusao"])
        
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
                
    elif teste["tipo"] == "pred":
        ok, contra_exemplo = avaliar_predicados(teste["premissas"], teste["conclusao"], teste["dominio"])
        
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
                
    input("\nPressione Enter para voltar...")

if __name__ == "__main__":
    print("Executando todos os testes sequencialmente para validação...")
    # Mock do input para não pausar a execução em massa
    original_input = __builtins__.input
    __builtins__.input = lambda x=None: None
    
    try:
        for i in range(len(CASOS_TESTE)):
            executar_teste(i)
        print("\nTodos os testes executados com sucesso!")
    except Exception as e:
        print(f"\nERRO DURANTE EXECUÇÃO DOS TESTES: {e}")
        raise e
    finally:
        __builtins__.input = original_input
