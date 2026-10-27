# Seminário: Featherweight Java

Seminário sobre o capítulo 19 de *Types and Programming Languages* (Pierce, 2002): **Featherweight Java (FJ)**, um núcleo mínimo de Java com sintaxe, tipos e semântica que cabem numa página.

## Por onde começar

1. Leia o [guia de estudo](guias/01-guia-de-estudo.md): resumo de todo o capítulo.
2. Leia o [capítulo 19 do livro](livro/tapl-cap19-featherweight-java.pdf) (18 páginas).
3. Treine com as [reduções passo a passo](guias/02-reducoes-passo-a-passo.md).
4. Rode os [exemplos](exemplos/) e veja que FJ é Java de verdade.
5. Revise com as [perguntas e respostas](guias/03-perguntas-e-respostas.md).
6. Siga o [plano de leitura do capítulo](guias/07-plano-de-leitura-do-capitulo.md).
7. Veja sua parte na [divisão e roteiro](guias/04-divisao-e-roteiro.md) e ensaie com a [apresentação](apresentacao/index.html).
8. Para a parte do meio, use o [roteiro detalhado de avaliação](guias/06-roteiro-pessoa-2-avaliacao.md).
9. Para assumir qualquer parte: [Pessoa 1](guias/08-guia-pessoa-1-fundamentos.md), [Pessoa 3](guias/09-guia-pessoa-3-tipagem-e-seguranca.md) e [cola geral](guias/10-cola-geral.md).
10. Consulte o [relatório da revisão didática](guias/11-relatorio-de-revisao-didatica.md).

## Conteúdo

| Pasta | O que tem |
|---|---|
| [`apresentacao/`](apresentacao/) | 25 slides em HTML, com um recorte citado da Figura 19-3 e exemplos progressivos. Setas navegam, F liga tela cheia. |
| [`guias/`](guias/) | Guia geral, reduções, perguntas, divisão, roteiros das 3 pessoas, cola geral, plano de leitura, revisão e referências |
| [`livro/`](livro/) | Capítulo 19 do TAPL em PDF, fornecido para uso na disciplina |
| [`exemplos/`](exemplos/) | Os termos dos slides em Java, prontos para compilar e rodar |

## Resumo em cinco linhas

- 5 formas de termo: variável, campo, método, `new` e cast.
- Subtipagem nominal, vinda de `extends`.
- 3 regras de computação e avaliação por valor, sem memória.
- 3 regras de cast, incluindo o "stupid cast", necessário para a preservação.
- Programa bem tipado só trava em downcast.
