import subprocess
import sys
import time
import os
from testes_logica import CASOS_TESTE

def run_simulation_test(test_case):
    print(f"\n=== TESTANDO CASO {test_case['id']}: {test_case['nome']} ===")
    cmd = [sys.executable, "main.py"]
    
    # Force UTF-8 environment
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Start process
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        env=env
    )
    
    def write_input(text):
        if process.poll() is not None:
             return
        try:
            process.stdin.write(text + "\n")
            process.stdin.flush()
            time.sleep(0.2) # Small delay for stability
        except Exception as e:
            print(f"Erro ao escrever input: {e}")

    try:
        time.sleep(1) # Wait for startup
        
        # Navigate menus based on type
        if test_case["tipo"] == "prop":
            write_input("1") # Menu Prop
            write_input(str(len(test_case["premissas"])))
            for p in test_case["premissas"]:
                write_input(p)
            write_input(test_case["conclusao"])
            
        elif test_case["tipo"] == "pred":
            write_input("2") # Menu Pred
            write_input(",".join(test_case["dominio"]))
            write_input(str(len(test_case["premissas"])))
            for p in test_case["premissas"]:
                write_input(p)
            write_input(test_case["conclusao"])
            
        # Wait for calculation
        time.sleep(0.5)
        
        # Exit sequence
        write_input("") # Enter to return to main menu
        write_input("5") # Exit option
        
        stdout, stderr = process.communicate(timeout=5)
        
        # Verify Logic
        # Determine expected result from description string
        is_expected_valid = "(VÁLIDO)" in test_case["desc"]
        
        # Check actual output
        # We use the new markers [OK] and [X] set in menus.py
        got_valid = "[OK] ARGUMENTO VÁLIDO" in stdout
        got_invalid = "[X] ARGUMENTO INVÁLIDO" in stdout
        
        if is_expected_valid:
            if got_valid:
                print("✅ SUCESSO: Resultado VÁLIDO identificado corretamente.")
            else:
                print("❌ FALHA: Esperava VÁLIDO, mas não foi identificado.")
                if got_invalid:
                    print("   -> O sistema indicou INVÁLIDO incorretamente.")
                else:
                    print("   -> O sistema não indicou nem válido nem inválido (erro ou crash).")
                    if stderr: print(f"   STDERR: {stderr}")
        else:
            if got_invalid:
                print("✅ SUCESSO: Resultado INVÁLIDO identificado corretamente.")
            else:
                print("❌ FALHA: Esperava INVÁLIDO, mas não foi identificado.")
                if got_valid:
                    print("   -> O sistema indicou VÁLIDO incorretamente.")
                else:
                    print("   -> O sistema não indicou nem válido nem inválido (erro ou crash).")
                    if stderr: print(f"   STDERR: {stderr}")

    except subprocess.TimeoutExpired:
        process.kill()
        print("❌ TIMEOUT: O teste demorou muito.")
    except Exception as e:
        process.kill()
        print(f"❌ ERRO EXCEPCIONAL: {e}")

if __name__ == "__main__":
    print(f"Iniciando bateria de {len(CASOS_TESTE)} testes simulados...\n")
    for t in CASOS_TESTE:
        run_simulation_test(t)
