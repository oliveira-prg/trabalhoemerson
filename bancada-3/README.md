# Sistema de Validação Lógica

Este projeto é uma ferramenta interativa de linha de comando (CLI) desenvolvida em Python para validar argumentos lógicos. Ele suporta tanto a **Lógica Proposicional** quanto a **Lógica de Predicados** (em domínios finitos), permitindo aos usuários testar a validade de argumentos, verificar tabelas-verdade e explorar exemplos clássicos de inferência lógica.

![Interface do Sistema](assets/image.png)

## Funcionalidades

### 1. Lógica Proposicional

- **Validação via Tabela-Verdade**: Gera e exibe a tabela-verdade completa para o conjunto de premissas e conclusão.
- **Identificação de Formas**: Reconhece formas de argumento comuns, como:
  - Modus Ponens
  - Modus Tollens
  - Silogismo Hipotético
  - Silogismo Disjuntivo
  - Dilema Construtivo
  - Falácias (Afirmação do Consequente, Negação do Antecedente)
- **Operadores Suportados**:
  - `~` (Negação)
  - `&` ou `∧` (Conjunção)
  - `|` ou `∨` (Disjunção)
  - `->` (Implicação)
  - `<->` (Bicondicional)

### 2. Lógica de Predicados

- **Validação em Domínio Finito**: Avalia argumentos testando todas as interpretações possíveis dentro de um domínio especificado pelo usuário.
- **Sintaxe Suportada**:
  - Predicados: `P(x)`, `G(a,b)`
  - Quantificadores: `(∀x)` (Universal), `(∃x)` (Existencial)
  - Variáveis e Constantes

### 3. Casos de Teste Obrigatórios

Um menu dedicado com 10 casos de teste pré-configurados para demonstração imediata:

1. **Modus Ponens** (Válido)
2. **Falácia da Afirmação do Consequente** (Inválido)
3. **Silogismo Disjuntivo** (Válido)
4. **Dilema Construtivo** (Válido)
5. **Particularização Universal** (Válido)
6. **Generalização Existencial** (Válido)
7. **Silogismo de Aristóteles** (Válido - "Sócrates é mortal")
8. **Argumento Inválido com Predicados**
9. **Quantificadores Aninhados** (Inválido)
10. **Equivalência de De Morgan** (Válido)

### 4. Ajuda Integrada

- Explicações detalhadas sobre a sintaxe.
- Exemplos de como inserir premissas e conclusões.

## Estrutura do Projeto

O projeto foi modularizado para facilitar a manutenção e leitura:

- `main.py`: Ponto de entrada da aplicação. Gerencia o loop principal.
- `menus.py`: Contém as funções de interface com o usuário (menus e submenus).
- `tabela_verdade.py`: Motor de avaliação para lógica proposicional (gera tabelas-verdade).
- `avaliador_predicados.py`: Motor de avaliação para lógica de predicados (enumeração de modelos).
- `parser_proposicional.py` & `parser_predicados.py`: Responsáveis por interpretar as strings de entrada.
- `formas_argumento.py`: Lógica para identificar padrões de argumentos conhecidos.
- `testes_logica.py`: Definição e execução dos casos de teste obrigatórios.
- `utils.py`: Funções utilitárias (ex: limpeza de tela).

## Como Executar

Certifique-se de ter o Python 3 instalado.

1. Clone o repositório ou baixe os arquivos.
2. Abra o terminal na pasta do projeto.
3. Execute o comando:

```bash
python main.py
```

## Exemplo de Uso

**Validando um Modus Ponens:**

1. Selecione "1 - Lógica Proposicional".
2. Número de premissas: `2`
3. Premissa 1: `P -> Q`
4. Premissa 2: `P`
5. Conclusão: `Q`

**Resultado Esperado:**

- Tabela-verdade exibida.
- Status: **✓ ARGUMENTO VÁLIDO**
- Forma detectada: **Modus Ponens**

## Requisitos

- Python 3.x
- Nenhuma biblioteca externa é necessária (apenas bibliotecas padrão como `re`, `itertools`, `os`).

## Autores

- GABRIEL SOARES COLARES
- ALESSANDRO SILVA LEMOS
- LUIZ PABLO BEZERRA DA SILVA
- DAVI CASTELO BRANCO DO NASCIMENTO
- JAILANE BARBOZA DA SILVA

---

Desenvolvido como trabalho prático para a disciplina de Matemática Discreta.
