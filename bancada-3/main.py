from utils import clear_screen
from menus import menu_proposicional, menu_predicados, menu_ajuda, menu_testes_obrigatorios

def main():
    while True:
        clear_screen()
        print("\n=== SISTEMA DE VALIDAÇÃO LÓGICA ===")
        print("1 - Lógica Proposicional")
        print("2 - Lógica de Predicados")
        print("3 - Ajuda / Exemplos")
        print("4 - Casos de Teste Obrigatórios")
        print("5 - Sair")
        op = input("> ")
        if op == "1":
            menu_proposicional()
        elif op == "2":
            menu_predicados()
        elif op == "3":
            menu_ajuda()
        elif op == "4":
            menu_testes_obrigatorios()
        elif op == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
