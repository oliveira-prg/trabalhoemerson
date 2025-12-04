# Casos de Teste - Trabalho de MD Toppissimo

## Lógica Proposicional

### Teste 1: Modus Ponens 

| Campo | Valor |
|-------|-------|
| **Premissas** | `P -> Q`, `P` |
| **Conclusão** | `Q` |
| **Resultado Esperado** | VÁLIDO |
| **Forma Identificada** | Modus Ponens |

**Justificativa:** Se P implica Q e P é verdadeiro, então Q deve ser verdadeiro.


### Teste 2: Falácia da Afirmação do Consequente

| Campo | Valor |
|-------|-------|
| **Premissas** | `P -> Q`, `Q` |
| **Conclusão** | `P` |
| **Resultado Esperado** | INVÁLIDO |
| **Forma Identificada** | Falácia: Afirmação do Consequente |

**Justificativa:** Afirmar o consequente não garante a verdade do antecedente.

**Contraexemplo:** P = F, Q = V → Premissas verdadeiras, conclusão falsa.


### Teste 3: Silogismo Disjuntivo

| Campo | Valor |
|-------|-------|
| **Premissas** | `P V Q`, `~P` |
| **Conclusão** | `Q` |
| **Resultado Esperado** | VÁLIDO |
| **Forma Identificada** | Silogismo Disjuntivo |

**Justificativa:** Se P ou Q é verdadeiro e P é falso, então Q deve ser verdadeiro.


### Teste 4: Dilema Construtivo

| Campo | Valor |
|-------|-------|
| **Premissas** | `(P->Q) & (R->S)`, `P V R` |
| **Conclusão** | `Q V S` |
| **Resultado Esperado** | VÁLIDO |
| **Forma Identificada** | Dilema Construtivo |

**Justificativa:** Dadas duas implicações e a disjunção dos antecedentes, segue a disjunção dos consequentes.


### Teste 5: Modus Tollens 

| Campo | Valor |
|-------|-------|
| **Premissas** | `P -> Q`, `~Q` |
| **Conclusão** | `~P` |
| **Resultado Esperado** | VÁLIDO |
| **Forma Identificada** | Modus Tollens |

**Justificativa:** Se P implica Q e Q é falso, então P deve ser falso.


### Teste 6: Falácia da Negação do Antecedente 

| Campo | Valor |
|-------|-------|
| **Premissas** | `P -> Q`, `~P` |
| **Conclusão** | `~Q` |
| **Resultado Esperado** | INVÁLIDO |
| **Forma Identificada** | Falácia: Negação do Antecedente |

**Justificativa:** Negar o antecedente não garante a falsidade do consequente.

**Contraexemplo:** P = F, Q = V → Premissas verdadeiras, conclusão falsa.


### Teste 7: Silogismo Hipotético 

| Campo | Valor |
|-------|-------|
| **Premissas** | `P -> Q`, `Q -> R` |
| **Conclusão** | `P -> R` |
| **Resultado Esperado** | VÁLIDO |
| **Forma Identificada** | Silogismo Hipotético |

**Justificativa:** Transitividade da implicação.


## Lógica de Predicados

### Teste 8: Particularização Universal 

| Campo | Valor |
|-------|-------|
| **Domínio** | `{a, b, c}` |
| **Premissas** | `(Ax)P(x)` |
| **Conclusão** | `P(a)` |
| **Resultado Esperado** | VÁLIDO |

**Justificativa:** Se P(x) vale para todo x do domínio, então vale para qualquer elemento específico.


### Teste 9: Generalização Existencial 

| Campo | Valor |
|-------|-------|
| **Domínio** | `{a, b}` |
| **Premissas** | `P(a)` |
| **Conclusão** | `(Ex)P(x)` |
| **Resultado Esperado** | VÁLIDO |

**Justificativa:** Se existe um elemento para o qual P vale, então existe x tal que P(x).


### Teste 10: Silogismo de Aristóteles 

| Campo | Valor |
|-------|-------|
| **Domínio** | `{s}` |
| **Premissas** | `(Ax)(H(x)->M(x))`, `H(s)` |
| **Conclusão** | `M(s)` |
| **Resultado Esperado** | VÁLIDO |

**Justificativa:** "Todos os homens são mortais. Sócrates é homem. Logo, Sócrates é mortal."


### Teste 11: Argumento Inválido com Existenciais 

| Campo | Valor |
|-------|-------|
| **Domínio** | `{a, b}` |
| **Premissas** | `(Ex)P(x) & (Ex)Q(x)` |
| **Conclusão** | `(Ex)(P(x) & Q(x))` |
| **Resultado Esperado** | INVÁLIDO |

**Justificativa:** A existência separada não implica existência conjunta no mesmo elemento.

**Contraexemplo:** P(a)=V, P(b)=F, Q(a)=F, Q(b)=V


### Teste 12: Quantificadores Aninhados 

| Campo | Valor |
|-------|-------|
| **Domínio** | `{1, 2}` |
| **Premissas** | `(Ax)(Ey)P(x,y)` |
| **Conclusão** | `(Ey)(Ax)P(x,y)` |
| **Resultado Esperado** | INVÁLIDO |

**Justificativa:** A ordem dos quantificadores afeta o significado. "Para todo x existe y" ≠ "Existe y para todo x".


### Teste 13: Equivalência de De Morgan 

| Campo | Valor |
|-------|-------|
| **Domínio** | `{a, b}` |
| **Premissas** | `~(Ax)P(x)` |
| **Conclusão** | `(Ex)~P(x)` |
| **Resultado Esperado** | VÁLIDO |

**Justificativa:** Lei de De Morgan para quantificadores: ¬∀x P(x) ≡ ∃x ¬P(x)


## Skolemização

### Teste 14: Constante de Skolem

| Campo | Valor |
|-------|-------|
| **Entrada** | `(Ex)P(x)` |
| **FNP** | `(Ex)P(x)` |
| **Skolemizada** | `P(c1)` |

**Justificativa:** Quantificador existencial sem universais precedentes → constante de Skolem.


### Teste 15: Função de Skolem

| Campo | Valor |
|-------|-------|
| **Entrada** | `(Ax)(Ey)P(x,y)` |
| **FNP** | `(Ax)(Ey)P(x,y)` |
| **Skolemizada** | `P(x, f1(x))` |

**Justificativa:** Quantificador existencial no escopo de universal → função de Skolem.


## Resumo dos Resultados

| # | Teste | Tipo | Resultado Esperado |
|---|-------|------|-------------------|
| 1 | Modus Ponens | Proposicional | VÁLIDO |
| 2 | Afirmação do Consequente | Proposicional | INVÁLIDO |
| 3 | Silogismo Disjuntivo | Proposicional | VÁLIDO |
| 4 | Dilema Construtivo | Proposicional | VÁLIDO |
| 5 | Modus Tollens | Proposicional | VÁLIDO |
| 6 | Negação do Antecedente | Proposicional | INVÁLIDO |
| 7 | Silogismo Hipotético | Proposicional | VÁLIDO |
| 8 | Particularização Universal | Predicados | VÁLIDO |
| 9 | Generalização Existencial | Predicados | VÁLIDO |
| 10 | Silogismo de Aristóteles | Predicados | VÁLIDO |
| 11 | Existenciais Separados | Predicados | INVÁLIDO |
| 12 | Quantificadores Aninhados | Predicados | INVÁLIDO |
| 13 | De Morgan Quantificadores | Predicados | VÁLIDO |
| 14 | Constante de Skolem | Skolem | - |
| 15 | Função de Skolem | Skolem | - |

---

**Total:** 15 casos de teste
- **Proposicionais:** 7 testes (5 válidos, 2 inválidos)
- **Predicados:** 6 testes (4 válidos, 2 inválidos)
- **Skolemização:** 2 testes
