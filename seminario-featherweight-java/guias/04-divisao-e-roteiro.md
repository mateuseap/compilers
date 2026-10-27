# Divisão e roteiro da apresentação

A apresentação está em [`../apresentacao/index.html`](../apresentacao/index.html). Setas, Espaço ou PageUp/PageDown navegam; F liga a tela cheia. Slides 11 a 18 pertencem à Pessoa 2 e usam animação progressiva onde ela ajuda a seguir a execução.

Duração estimada: 27–30 minutos.

## Divisão em 3 pessoas

| Pessoa | Slides | Tema | Tempo |
|---|---|---|---|
| 1 | 1 a 10 | O que é FJ: motivação, recorte, sintaxe e tipos nominais | ~8 min |
| 2 | 11 a 18 | Como FJ executa: regras, call-by-value, casts, substituição e despacho | ~9 min |
| 3 | 19 a 25 | Como FJ garante segurança: tipagem, casts, teoremas, exercícios e fechamento | ~9 min |

## Pessoa 1: o que é FJ (slides 1 a 10)

| Slide | Ideia central |
|---|---|
| 1 | Capa |
| 2 | Cap. 18 codifica objetos; cap. 19 os trata como primitivos. FJ é subconjunto de Java. |
| 3 | FJ escolhe compacidade para tornar as provas manejáveis. |
| 4 | O que mantém e corta; ausência de atribuição elimina heap explícito. |
| 5 | Exemplo Pair e construtor padronizado. |
| 6 | Cinco formas de termo e única forma de valor. |
| 7 | Gramática completa e programa `(CT,t)`. |
| 8 | Subtipagem nominal contra estrutural. |
| 9 | Três regras de subtipagem + exemplo Animal/Mamifero/Cachorro. |
| 10 | `fields`, `mtype`, `mbody`, `override` + exemplo Cachorro. |

**Ponte:** "Com a sintaxe e as consultas à tabela de classes definidas, podemos executar os termos um passo por vez."

Guia completo: [08-guia-pessoa-1-fundamentos.md](08-guia-pessoa-1-fundamentos.md).

## Pessoa 2: como FJ executa (slides 11 a 18)

| Slide | Ideia central |
|---|---|
| 11 | Figura 19-3 original: computação versus congruência. |
| 12 | E-ProjNew, E-InvkNew e E-CastNew, com animais. |
| 13 | Call-by-value: congruência leva até o próximo redex. |
| 14 | Exemplo formal Pair com cast, passo a passo. |
| 15 | Tipo estático Animal versus classe real Gato; por que cast é necessário. |
| 16 | `setfst`: `mbody` e substituição de parâmetro e `this`. |
| 17 | Despacho dinâmico e recursão aberta com `Cachorro.apresentar`. |
| 18 | Três formas de stuck e o papel posterior da tipagem. |

**Ponte:** "A avaliação mostrou onde pode faltar regra. Agora veremos como o sistema de tipos elimina campo e método inexistentes e isola a falha de cast."

Roteiro oral: [06-roteiro-pessoa-2-avaliacao.md](06-roteiro-pessoa-2-avaliacao.md).

## Pessoa 3: como FJ garante segurança (slides 19 a 25)

| Slide | Ideia central |
|---|---|
| 19 | T-Var, T-Field, T-Invk, T-New e leitura de `Γ ⊢ t:C`. |
| 20 | Upcast, downcast e stupid cast, com exemplos Animal/Gato/Cachorro. |
| 21 | Tipagem de métodos e classes; restrição de override. |
| 22 | Preservação e progresso. |
| 23 | Exercícios do livro. |
| 24 | Codificação contra objetos primitivos. |
| 25 | Resumo e referências. |

Guia completo: [09-guia-pessoa-3-tipagem-e-seguranca.md](09-guia-pessoa-3-tipagem-e-seguranca.md).

## Materiais para qualquer substituição

- [10-cola-geral.md](10-cola-geral.md): revisão em duas páginas.
- [03-perguntas-e-respostas.md](03-perguntas-e-respostas.md): perguntas prováveis.
- [07-plano-de-leitura-do-capitulo.md](07-plano-de-leitura-do-capitulo.md): plano de estudo integral.
- [11-relatorio-de-revisao-didatica.md](11-relatorio-de-revisao-didatica.md): mudanças e decisões técnicas.

## Dicas

- Ensaiem as duas transições em conjunto.
- Não leiam a Figura 19-3 linha por linha; usem-na como mapa e expliquem as ampliações.
- Pair continua sendo o exemplo formal. Animal/Mamifero/Cachorro é a ponte intuitiva.
- Para demo, rodem `python3 exemplos/fj_trace.py` e os exemplos Java.
- Se o tempo apertar, omitam o slide 24, não uma regra formal.
