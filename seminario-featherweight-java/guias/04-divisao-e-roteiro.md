# Divisão e roteiro da apresentação

A apresentação está em [`../apresentacao/index.html`](../apresentacao/index.html). Abra no navegador; setas, Espaço ou PageUp/PageDown navegam, e F liga a tela cheia. Os slides 14, 16 e 19 avançam passo a passo. Os slides 25 a 27 são apêndices com as figuras originais do livro.

Duração estimada: 25 minutos.

## Divisão em 3 pessoas

| Pessoa | Slides | Tema | Tempo |
|---|---|---|---|
| 1 | 1 a 10 | O que é FJ: motivação, recorte, sintaxe e tipos nominais | ~8 min |
| 2 | 11 a 17 | Como FJ executa: regras de avaliação, passo a passo e quando trava | ~8 min |
| 3 | 18 a 24 | Como FJ garante segurança: tipagem, casts, teoremas, exercícios e fechamento | ~9 min |

## Pessoa 1: o que é FJ (slides 1 a 10)

| Slide | Ideia central |
|---|---|
| 1 | Capa |
| 2 | Cap. 18 codifica objetos com lambda-cálculo; cap. 19 trata objetos como parte da linguagem. FJ é subconjunto estrito de Java. |
| 3 | Modelo formal serve para provar propriedades. FJ escolhe ser pequeno para a prova ser curta. |
| 4 | O que fica e o que sai. O corte principal é a atribuição. |
| 5 | Exemplo `Pair` e as convenções rígidas. |
| 6 | As 5 formas de termo. |
| 7 | A gramática completa. Valores são `new C(v̄)`. |
| 8 | Nominal contra estrutural. |
| 9 | Subtipagem vem de `extends`. Tabela de classes. |
| 10 | `fields`, `mtype`, `mbody`, `override`. |

**Ponte:** "Com a sintaxe e as funções auxiliares definidas, vamos ver como um programa FJ roda."

## Pessoa 2: como FJ executa (slides 11 a 17)

| Slide | Ideia central |
|---|---|
| 11 | Figura 19-3 original do livro: visão geral de toda a avaliação. |
| 12 | As três regras de computação: campo, método, cast. |
| 13 | As cinco regras de congruência e os contextos de avaliação. |
| 14 | Passo a passo do termo com cast. Avance com a seta e diga a regra de cada passo. |
| 15 | Por que o cast é necessário: sem ele, `.snd` não tipa. |
| 16 | Passo a passo da chamada de método: substituição de parâmetros e de `this`. |
| 17 | Três jeitos de travar. |

**Ponte:** "Travar é o erro de FJ. A próxima parte mostra como o sistema de tipos evita isso."

## Pessoa 3: como FJ garante segurança (slides 18 a 24)

| Slide | Ideia central |
|---|---|
| 18 | Uma regra de tipo para cada forma de termo. Sem subsunção solta. |
| 19 | Três regras de cast. Avance para mostrar o stupid cast e por que ele é necessário. |
| 20 | Tipagem de métodos e classes. |
| 21 | Preservação e progresso. Só trava em downcast. |
| 22 | Exercícios do livro. |
| 23 | As duas visões se complementam. |
| 24 | Resumo e referências. |

## Dicas

- Ensaiem as transições juntos: a pessoa 2 usa `fields` e `mbody` do slide 10, e a pessoa 3 retoma o "travar" do slide 17.
- A parte da pessoa 3 é a mais densa. Fica com quem estiver mais confortável com tipos.
- Se o tempo apertar, os slides 13 e 23 podem ser pulados sem quebrar a história.
- Para uma demo rápida, rodem [`../exemplos/`](../exemplos/) e mostrem que os resultados batem com os slides 14 e 16.
- Cada um deve conseguir responder as perguntas da sua parte em [03-perguntas-e-respostas.md](03-perguntas-e-respostas.md).
