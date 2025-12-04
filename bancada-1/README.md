# **README – Sistema Automatizado de Verificação de Argumentos Lógicos**


Este projeto implementa um verificador para lógica proposicional e lógica de predicados com domínio finito. Utiliza análise sintática, avaliação semântica e enumeração de interpretações para determinar a validade de argumentos fornecidos pelo usuário.

## **Bibliotecas Utilizadas:**
* itertools
* re
* os
* sys

## **Funcionalidades:**
* Verificação de validade em lógica proposicional via tabela verdade.
* Detecção de contraexemplos.
* Identificação de formas argumentais (Modus Ponens, Silogismo Disjuntivo etc.).
* Parser completo para lógica de predicados com quantificadores.
* Enumeração de interpretações para verificar validade.

## **Como executar:**
1. Acesse a pasta do projeto.
2. Execute: python main.py
3. Escolha a modalidade:
  * Lógica Proposicional
  * Lógica de Predicados
  * Sair
   
## **Estrutura:**
Organizadas em blocos ao invés de arquivos separados.

**PARTE 1 - Motor de Tabela Verdade**

* class MotorProposicional: ***def***(traduzir, identificar_forma e gerar_tabela)

  
**PARTE 2 - Motor de Predicados**
  
* class MotorPredicados: ***def***( expandir_formulas, gerar_eexplicacao e verificar)

  
**PARTE 4 - Interface de Usuário**

* ***def***(limpar, ler_int, exibir_resultado, main)

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
* Crescimento exponencial das interpretações na lógica de predicados.
* Reconhecimento básico de formas argumentais.

## 

### **Autores:** 
* Antonio Kássio(https://github.com/Antonio-Kassio),
* Eduardo Bandeira(https://github.com/devBandas),
* Hamilton Isaac(https://github.com/Skymebr),
* Mario Silva(https://github.com/MarioJuniorcpp),
* Matheus Oliviera (https://github.com/oliveira-prg),
* Victoria Miranda(https://github.com/ViMirand)
