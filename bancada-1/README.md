# **README – Sistema Automatizado de Verificação de Argumentos Lógicos**


Este projeto implementa um verificador para lógica proposicional e lógica de predicados com domínio finito. Utiliza análise sintática, avaliação semântica e enumeração de interpretações para determinar a validade de argumentos fornecidos pelo usuário.

## **Bibliotecas Utilizadas:**
itertools 
re
os
sys
itertools product

## **Funcionalidades:**
* Verificação de validade em lógica proposicional via tabela verdade.
* Detecção de contraexemplos.
* Identificação de formas argumentais (Modus Ponens, Silogismo Disjuntivo etc.).
* Parser para lógica de predicados com quantificadores.

## **Como executar:**
1. Execute o terminal da máquina.
2. Acesse o diretório do projeto.
3. Execute "python Final.py"
4. Escolha a função:
  1. Lógica Proposicional
  2. Lógica de Predicados
  3. Sair
   
## **Arquivos:**

**Final.py**

## **Estrutura:**

PARTE 1 - Motor de Tabela Verdade 
* classe MotorProposicional
 
PARTE 2 - Motor de Predicados 
* classe MotorPredicados

PARTE 3 - Códigos Avançados (Não concluída)

PARTE 4 - Interface de Usuário 
* funções limpar(), ler_int(msg), exibir_resultado(dados) e main()

## **Exemplo de uso (Proposicional):**
**Premissas:**

- P -> Q

- P

**Conclusão:**

- Q

*Resultado: Válido (Modus Ponens)*

## **Exemplo de uso (Predicados):**
* Domínio: a, b
* Premissas: (∀x)P(x)
* Conclusão: P(a)
* Resultado: Válido

## **Limitações:**
* Conjuntos infinitos.
* Reconhecimento de formas argumentais avançadas.
* Reconhecimento de De Morgan

## 

### **Autores:** 
* Antonio Kássio(https://github.com/Antonio-Kassio),
* Eduardo Bandeira(https://github.com/devBandas),
* Hamilton Isaac(https://github.com/Skymebr/),
* Mario Silva(https://github.com/MarioJuniorcpp),
* Matheus Oliviera (https://github.com/oliveira-prg),
* Victoria Miranda(https://github.com/ViMirand)
