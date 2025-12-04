# RELATÓRIO TÉCNICO

## Sistema Automatizado de Verificação de Argumentos Lógicos

Disciplina: Matemática Discreta

**Autores:**
- Chrysthyan
- Marcos V. Gonzaga
- Thiago Willian
- Eric Gabriel

## 1. Introdução

Este relatório técnico descreve o desenvolvimento de um Sistema Automatizado de Verificação de Argumentos Lógicos, implementado em Python como trabalho da disciplina de Matemática Discreta.

O sistema é capaz de analisar argumentos em lógica proposicional e de predicados, determinando sua validade através de diferentes técnicas de prova e fornecendo justificativas detalhadas para suas conclusões.

### 1.1 Objetivos

- Implementar um parser robusto para fórmulas lógicas proposicionais e de predicados
- Desenvolver verificador por tabela verdade para lógica proposicional
- Implementar verificador com domínio finito para lógica de predicados
- Adicionar suporte a Forma Normal Prenex (FNP) e Skolemização
- Criar interface gráfica intuitiva com exportação LaTeX

## 2. Arquitetura do Sistema

O sistema foi desenvolvido seguindo uma arquitetura modular, com separação clara de responsabilidades entre os componentes. Esta abordagem facilita a manutenção e extensibilidade do código.

### 2.1 Módulos Principais

| **Módulo**        | **Responsabilidade**                                                                                     |
|-------------------|----------------------------------------------------------------------------------------------------------|
| **MotorLogico**   | Parser e avaliador de fórmulas proposicionais, geração de tabela verdade, identificação de formas de argumento |
| **MotorPredicados** | Expansão de quantificadores, substituição de variáveis, validação em domínio finito                     |
| **Skolemizador**  | Conversão para FNP, eliminação de implicações, movimento de negações, Skolemização                      |
| **ExportadorLatex** | Geração de documentos LaTeX para provas e demonstrações                                                 |
| **AppVerificador** | Interface gráfica Tkinter com três abas principais                                                       |

## 3. Decisões de Design

### 3.1 Parser Recursivo Descendente

Para o parsing de fórmulas lógicas, foi implementado um parser recursivo descendente manual em vez de geradores de parsers externos, com os seguintes objetivos:

- Controle total da precedência de operadores (¬ > ∧ > ∨ > → > ↔)
- Mensagens de erro mais informativas
- Redução de dependências externas do projeto

### 3.2 Validação por Força Bruta

Para domínios finitos pequenos, utiliza-se a enumeração completa de todas as interpretações possíveis (força bruta). Embora não seja a abordagem mais eficiente para domínios grandes, ela garante correção e facilita a geração de contraexemplos.

### 3.3 Skolemização Passo a Passo

O processo de Skolemização foi implementado em 4 passos distintos:

1. **Eliminar Implicação:** \( P \rightarrow Q \equiv \neg P \lor Q \)
2. **Mover Negações:** \( \neg(\forall x)P \equiv (\exists x)\neg P \) e \( \neg(\exists x)P \equiv (\forall x)\neg P \)
3. **Forma Normal Prenex:** Mover quantificadores para o início
4. **Skolemização:** Substituir variáveis existenciais por constantes ou funções de Skolem

## 4. Detalhes de Implementação

### 4.1 Lógica Proposicional

O motor de lógica proposicional implementa as seguintes funcionalidades:

- Normalização: converte símbolos alternativos (¬, ∧, ∨, →, ↔) para formato interno (~, &, V, ->, <->)
- Extração de variáveis: identifica todas as variáveis proposicionais únicas
- Avaliação: avalia fórmulas recursivamente com mapeamento de valores
- Tabela verdade: gera todas as \(2^n\) combinações para \(n\) variáveis

### 4.2 Lógica de Predicados

O motor de predicados expande quantificadores para conjunções/disjunções finitas, por exemplo:

- \((\forall x)P(x)\) com domínio \(\{a,b,c\} \Rightarrow P(a) \land P(b) \land P(c)\)
- \((\exists x)P(x)\) com domínio \(\{a,b,c\} \Rightarrow P(a) \lor P(b) \lor P(c)\)

Após a expansão, o problema é reduzido à lógica proposicional e validado pelo **MotorLogico**.

### 4.3 Formas de Argumento Reconhecidas

| **Forma**                 | **Estrutura**       | **Validade** |
|---------------------------|---------------------|--------------|
| Modus Ponens              | \(P \rightarrow Q, P \vdash Q\)           | VÁLIDO       |
| Modus Tollens             | \(P \rightarrow Q, \neg Q \vdash \neg P\) | VÁLIDO       |
| Silogismo Hipotético      | \(P \rightarrow Q, Q \rightarrow R \vdash P \rightarrow R\) | VÁLIDO |
| Silogismo Disjuntivo      | \(P \lor Q, \neg P \vdash Q\)             | VÁLIDO       |
| Afirmação do Consequente  | \(P \rightarrow Q, Q \vdash P\)           | FALÁCIA      |
| Negação do Antecedente    | \(P \rightarrow Q, \neg P \vdash \neg Q\) | FALÁCIA      |

## 5. Resultados dos Testes

O sistema foi validado com os casos de teste obrigatórios especificados no documento de requisitos.

### 5.1 Testes de Lógica Proposicional

| **Teste**                        | **Esperado** | **Resultado** |
|----------------------------------|--------------|---------------|
| Modus Ponens                     | VÁLIDO       | ✓ PASSOU      |
| Falácia Afirmação Consequente   | INVÁLIDO     | ✓ PASSOU      |
| Silogismo Disjuntivo            | VÁLIDO       | ✓ PASSOU      |
| Dilema Construtivo              | VÁLIDO       | ✓ PASSOU      |

### 5.2 Testes de Lógica de Predicados

| **Teste**                    | **Esperado** | **Resultado** |
|------------------------------|--------------|---------------|
| Particularização Universal   | VÁLIDO       | ✓ PASSOU      |
| Generalização Existencial    | VÁLIDO       | ✓ PASSOU      |
| Silogismo de Aristóteles     | VÁLIDO       | ✓ PASSOU      |
| Equivalência De Morgan       | VÁLIDO       | ✓ PASSOU      |

## 6. Funcionalidades Extras Implementadas

Além dos requisitos obrigatórios, o sistema implementa as seguintes funcionalidades extras.

### 6.1 Forma Normal Prenex e Skolemização

Implementação completa da opção de FNP e Skolemização, incluindo:

- Eliminação de implicações e bicondicionais
- Movimento de negações usando leis de De Morgan para quantificadores
- Extração de quantificadores para forma prenex
- Substituição de variáveis existenciais por constantes ou funções de Skolem

### 6.2 Interface Gráfica

Interface gráfica desenvolvida com Tkinter, contendo três abas:

- **Lógica Proposicional:** entrada de premissas, conclusão e exibição de tabela verdade
- **Lógica de Predicados:** definição de domínio e validação em domínio finito
- **Skolemização:** processamento passo a passo com exibição detalhada

### 6.3 Exportação LaTeX

Sistema de exportação de provas em formato LaTeX, gerando documentos prontos para compilação com:

- Formatação matemática correta usando pacotes `amsmath` e `amssymb`
- Estrutura de documento completa com premissas, conclusão e resultado
- Contraexemplos formatados quando o argumento é inválido

## 7. Conclusão

O sistema desenvolvido atende a todos os requisitos obrigatórios especificados no documento do trabalho, além de implementar funcionalidades extras que agregam valor educacional e prático à ferramenta.

A arquitetura modular adotada permite fácil extensão do sistema para incluir novas técnicas de prova ou suporte a outros sistemas lógicos. A interface gráfica torna o sistema acessível para estudantes que estão aprendendo lógica matemática.

Os casos de teste obrigatórios foram todos validados com sucesso, demonstrando a corretude da implementação para os cenários especificados.

## 8. Referências

1. HUTH, M.; RYAN, M. *Logic for Computer Science*. Cambridge University Press, 2004.  
2. BEN-ARI, M. *Mathematical Logic for Computer Science*. Springer, 2012.  
3. Stanford Encyclopedia of Philosophy – Logic. Disponível em: <https://plato.stanford.edu/entries/logic-classical/>  
4. Documentação Python Tkinter. Disponível em: <https://docs.python.org/3/library/tkinter.html>
