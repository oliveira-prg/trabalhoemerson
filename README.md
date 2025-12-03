# **README – Sistema Automatizado de Verificação de Argumentos Lógicos**
### Projeto acadêmico desenvolvido em Python.

Este projeto implementa um verificador para lógica proposicional e lógica de predicados com domínio finito. Utiliza análise sintática, avaliação semântica e enumeração de interpretações para determinar a validade de argumentos fornecidos pelo usuário.

## **Bibliotecas Utilizadas:**
* sympy.logic

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
**verificador/**
- main.py


**proposicional/**
- ast.py

- parser.py

- eval.py

- tabela_verdade.py

- forms.py


**predicados/**
- ast.py

- parser.py

- evaluator.py

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
* Antonio Kássio(),
* Eduardo Bandeira(https://github.com/devBandas),
* Hamilton Isaac(),
* Mario Silva(),
* Matheus Oliviera (https://github.com/oliveira-prg),
* Victoria Miranda(https://github.com/ViMirand)
