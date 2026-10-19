# Seminário: Featherweight Java

Seminário sobre o capítulo 19 de *Types and Programming Languages* (Pierce, 2002): **Featherweight Java (FJ)**, um núcleo mínimo de Java com sintaxe, tipos e semântica que cabem numa página.

## Por onde começar

1. Leia o [guia de estudo](guias/01-guia-de-estudo.md): resumo de todo o capítulo.
2. Leia o capítulo 19 do livro (18 páginas; obtenha pela biblioteca ou pelo exemplar fornecido na disciplina).
3. Treine com as [reduções passo a passo](guias/02-reducoes-passo-a-passo.md).
4. Rode os [exemplos](exemplos/) e veja que FJ é Java de verdade.
5. Revise com as [perguntas e respostas](guias/03-perguntas-e-respostas.md).
6. Veja sua parte na [divisão e roteiro](guias/04-divisao-e-roteiro.md) e ensaie com a [apresentação](apresentacao/index.html).

## Conteúdo

| Pasta | O que tem |
|---|---|
| [`apresentacao/`](apresentacao/) | Slides em HTML. Abra `index.html` no navegador: setas navegam, F liga tela cheia. |
| [`guias/`](guias/) | Guia de estudo, reduções passo a passo, perguntas e respostas, divisão do grupo e referências |
| [`exemplos/`](exemplos/) | Os termos dos slides em Java, prontos para compilar e rodar |

## Resumo em cinco linhas

- 5 formas de termo: variável, campo, método, `new` e cast.
- Subtipagem nominal, vinda de `extends`.
- 3 regras de computação e avaliação por valor, sem memória.
- 3 regras de cast, incluindo o "stupid cast", necessário para a preservação.
- Programa bem tipado só trava em downcast.
