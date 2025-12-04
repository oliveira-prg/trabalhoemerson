# Calculadora Lógica

## 📋 Descrição

Sistema desenvolvido em Python para verificação de argumentos em lógica proposicional e de predicados, implementando diferentes técnicas de prova e fornecendo justificativas para suas conclusões.

**Disciplina:** Matemática Discreta  
**Autores:** Chrysthyan, Marcos V. Gonzaga, Thiago Willian, Eric Gabriel

---

## Checklist

### Lógica Proposicional
- ✅ Parser de fórmulas proposicionais
- ✅ Verificação por tabela verdade completa
- ✅ Identificação de formas de argumento (Modus Ponens, Modus Tollens, etc.)
- ✅ Detecção de falácias (Afirmação do Consequente, Negação do Antecedente)

### Lógica de Predicados
- ✅ Parser de quantificadores (∀x), (∃x)
- ✅ Identificação de predicados P(x), Q(x,y), etc.
- ✅ Verificador com domínio finito
- ✅ Aplicação de regras básicas (Particularização/Generalização)
- ✅ Exibição de contraexemplos quando inválido

### Técnicas Avançadas
- ✅ **Opção C:** Forma Normal Prenex (FNP) e Skolemização
- ✅ Interface gráfica com Tkinter
- ✅ Exportação de provas em LaTeX

---

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Tkinter (geralmente incluído no Python)

### Dependências Opcionais
```bash
# Para parsing avançado (opcional)
pip install pyparsing
```

### Executando o Sistema
```bash
# python calculadora_lógica.py
```

---

## Sintaxe Suportada

### Lógica Proposicional

| Operador | Símbolo | Descrição |
|----------|---------|-----------|
| Negação | `~` ou `¬` | NÃO |
| Conjunção | `&` ou `∧` | E |
| Disjunção | `V` ou `∨` | OU |
| Implicação | `->` ou `→` | SE...ENTÃO |
| Bicondicional | `<->` ou `↔` | SE E SOMENTE SE |

**Exemplos:**
```
P -> Q
(P & Q) -> R
P V ~Q
(P -> Q) & (Q -> R)
```

### Lógica de Predicados

| Quantificador | Símbolo | Descrição |
|---------------|---------|-----------|
| Universal | `(Ax)` ou `(∀x)` | Para todo x |
| Existencial | `(Ex)` ou `(∃x)` | Existe x |

**Predicados:** P(x), Q(x,y), H(a), M(s), etc.

**Domínio:** {a, b, c} ou {1, 2, 3}

**Exemplos:**
```
(Ax)P(x)
(Ax)(P(x) -> Q(x))
(Ex)(P(x) & Q(x))
(Ax)(Ey)R(x,y)
```

---

## Exemplos de Uso

### Exemplo 1: Modus Ponens (Proposicional)
```
Premissas:
  P -> Q
  P
Conclusão: Q

Resultado: ✓ VÁLIDO
Forma: Modus Ponens
```

### Exemplo 2: Particularização Universal (Predicados)
```
Domínio: {1, 2, 3}
Premissa: (∀x)P(x)
Conclusão: (∃x)P(x)

Resultado: ✓ ARGUMENTO VÁLIDO
Método: Enumeração em domínio finito
Regra aplicada: Se (∀x)P(x) então P(c) para qualquer c, logo (∃x)P(x)
```

### Exemplo 3: Skolemização
```
Entrada: (∀x)P(x) -> (∃y)Q(y)

Passo 1 - Eliminar implicação:
-(∀x)P(x) v (∃y)Q(y)

Passo 2 - Mover negação:
(∃x)-P(x) v (∃y)Q(y)

Passo 3 - Forma Normal Prenex:
(∃x)(∃y)[-P(x) v Q(y)]

Passo 4 - Skolemização:
-P(c₁) v Q(c₂)
onde c₁, c₂ são constantes de Skolem
```

---

### Casos de Teste

## Video demonstração dos Casos de Teste
```link:
https://drive.google.com/file/d/1qGnB-3yNGkhUmPpnDnA3cD9fpDZZXKfT/view?usp=drive_link
```

### Lógica Proposicional

| Teste | Premissas | Conclusão | Esperado |
|-------|-----------|-----------|----------|
| Modus Ponens | P -> Q, P | Q | VÁLIDO |
| Modus Tollens | P -> Q, ~Q | ~P | VÁLIDO |
| Silogismo Disjuntivo | P V Q, ~P | Q | VÁLIDO |
| Silogismo Hipotético | P -> Q, Q -> R | P -> R | VÁLIDO |
| Falácia Afirmação Consequente | P -> Q, Q | P | INVÁLIDO |
| Falácia Negação Antecedente | P -> Q, ~P | ~Q | INVÁLIDO |
| Dilema Construtivo | (P->Q) & (R->S), P V R | Q V S | VÁLIDO |

### Lógica de Predicados

| Teste | Premissas | Conclusão | Domínio | Esperado |
|-------|-----------|-----------|---------|----------|
| Particularização Universal | (∀x)P(x) | P(a) | {a,b} | VÁLIDO |
| Generalização Existencial | P(a) | (∃x)P(x) | {a,b} | VÁLIDO |
| Silogismo de Aristóteles | (∀x)[H(x)->M(x)], H(s) | M(s) | {s} | VÁLIDO |
| Universal → Existencial | (∀x)P(x) | (∃x)P(x) | {1,2,3} | VÁLIDO |
| De Morgan Quantificadores | ~(∀x)P(x) | (∃x)~P(x) | {a,b} | VÁLIDO |
| Argumento Inválido | (∃x)P(x) & (∃x)Q(x) | (∃x)[P(x)&Q(x)] | {a,b} | INVÁLIDO |
| Quantificadores Aninhados | (∀x)(∃y)P(x,y) | (∃y)(∀x)P(x,y) | {a,b} | INVÁLIDO |

---

## Estrutura do Código

```
trabalhomdd_corrigido.py
├── MotorLogico              # Motor de lógica proposicional
│   ├── normalizar_formula() # Normalização de símbolos
│   ├── extrair_variaveis()  # Extração de variáveis
│   ├── parse_e_avaliar()    # Parser recursivo descendente
│   ├── gerar_tabela_verdade() # Geração de tabela verdade
│   ├── identificar_forma()  # Identificação de formas
│   └── validar_argumento()  # Validação completa
│
├── MotorPredicados          # Motor de lógica de predicados
│   ├── expandir()           # Expansão de quantificadores
│   ├── _substituir()        # Substituição de variáveis
│   ├── _detectar_regra()    # Detecção de regras aplicadas
│   └── validar()            # Validação em domínio finito
│
├── Skolemizador             # Forma Normal Prenex e Skolemização
│   ├── processar()          # Processamento completo
│   ├── _eliminar_implicacao() # Passo 1: P→Q ≡ ¬P∨Q
│   ├── _mover_negacoes()    # Passo 2: De Morgan
│   ├── _fnp()               # Passo 3: Forma Normal Prenex
│   ├── _skolemizar()        # Passo 4: Skolemização
│   └── get_latex()          # Exportação LaTeX
│
├── ExportadorLatex          # Exportação para LaTeX
│   ├── gerar_prova_proposicional()
│   ├── gerar_prova_predicados()
│   └── _converter_formula()
│
└── AppVerificador           # Interface gráfica Tkinter
    ├── setup_tab_proposicional()
    ├── setup_tab_predicados()
    └── setup_tab_skolem()
```

---

## Exportação LaTeX

O sistema permite exportar provas no formato LaTeX. Exemplo de saída:

```latex
\documentclass{article}
\usepackage{amsmath, amssymb}
\begin{document}
\section*{Verificação de Argumento}
\textbf{Premissas:}
\begin{enumerate}
  \item $P \rightarrow Q$
  \item $P$
\end{enumerate}
\textbf{Conclusão:} $Q$
\textbf{Resultado:} VÁLIDO
\textbf{Forma:} Modus Ponens
\end{document}
```

---

## Interface Gráfica

O sistema possui três abas principais:

1. **Lógica Proposicional**
   - Entrada de premissas (uma por linha)
   - Entrada de conclusão
   - Resultado com tabela verdade e identificação de forma

2. **Lógica de Predicados**
   - Definição de domínio
   - Entrada de premissas quantificadas
   - Resultado com regras aplicadas e verificação

3. **Skolemização / FNP**
   - Entrada de fórmula com quantificadores
   - Exibição passo a passo da conversão
   - Resultado final skolemizado

---

## Referências Teóricas

### Formas de Argumento Válidas
- **Modus Ponens:** P→Q, P ⊢ Q
- **Modus Tollens:** P→Q, ¬Q ⊢ ¬P
- **Silogismo Hipotético:** P→Q, Q→R ⊢ P→R
- **Silogismo Disjuntivo:** P∨Q, ¬P ⊢ Q
- **Dilema Construtivo:** (P→Q)∧(R→S), P∨R ⊢ Q∨S

### Falácias Formais
- **Afirmação do Consequente:** P→Q, Q ⊢ P (INVÁLIDO)
- **Negação do Antecedente:** P→Q, ¬P ⊢ ¬Q (INVÁLIDO)

### Regras de Inferência para Predicados
- **Particularização Universal:** (∀x)P(x) ⊢ P(a)
- **Generalização Existencial:** P(a) ⊢ (∃x)P(x)
- **De Morgan para Quantificadores:** ¬(∀x)P(x) ≡ (∃x)¬P(x)

### Skolemização
- Quantificador existencial sem universal anterior → Constante de Skolem (c)
- Quantificador existencial no escopo de universal → Função de Skolem f(x)

---

## Licença

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de Matemática Discreta.

---

## Contribuidores

- Chrysthyan (https://github.com/matheuschrys)
- Marcos V. Gonzaga
- Thiago Willian
- Eric Gabriel
