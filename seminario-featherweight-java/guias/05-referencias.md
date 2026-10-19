# Referências

## Fonte principal

- Pierce, B. C. *Types and Programming Languages*. MIT Press, 2002. Capítulo 19, "Case Study: Featherweight Java", páginas 247 a 264.

## Artigo original

- Igarashi, A.; Pierce, B. C.; Wadler, P. **Featherweight Java: a minimal core calculus for Java and GJ.** OOPSLA 1999.
- Versão de periódico: *ACM Transactions on Programming Languages and Systems* (TOPLAS), 23(3):396-450, 2001. DOI: [10.1145/503502.503505](https://doi.org/10.1145/503502.503505).
- Cópia gratuita (preprint do autor): [fj-toplas.pdf](https://www.cis.upenn.edu/~bcpierce/papers/fj-toplas.pdf).

A versão do livro usa chamada por valor; o artigo usa uma redução não determinística. O artigo também formaliza FGJ (Featherweight GJ, com genéricos).

## Implementações para explorar

- [yokoyama-lab/featherweight-java](https://github.com/yokoyama-lab/featherweight-java): mecanização em Rocq (Coq), com interpretador, verificador de tipos e as provas de progresso e preservação.
- [inrick/Featherweight-Java](https://github.com/inrick/Featherweight-Java): verificador de tipos em Haskell.

## Capítulos do TAPL que ajudam

| Capítulo | Por quê |
|---|---|
| 8 e 9 | Tipos simples, preservação e progresso pela primeira vez |
| 13 | Referências: base para o exercício de adicionar atribuição |
| 15 e 16 | Subtipagem e a versão algorítmica (por que FJ não tem subsunção solta) |
| 18 | Objetos codificados com registros: o contraponto ao cap. 19 |

## Trabalhos citados no capítulo

- Igarashi, A.; Pierce, B. C.; Wadler, P. *A recipe for raw types.* FOOL 2001. (FJ com raw types)
- Igarashi, A.; Pierce, B. C. *On inner classes.* ECOOP 2000. (FJ com classes internas)
- League, C.; Trifonov, V.; Shao, Z. *Type-preserving compilation of Featherweight Java.* FOOL 2001. (tradução de FJ que preserva tipos)
- Flatt, M.; Krishnamurthi, S.; Felleisen, M. *Classes and mixins.* POPL 1998. (modelo maior, com atribuição e cast)
- Abadi, M.; Cardelli, L. *A Theory of Objects.* Springer, 1996. (cálculo de objetos)

> O capítulo do TAPL não é redistribuído neste repositório por direitos autorais. Consulte o exemplar fornecido na disciplina ou a biblioteca. O artigo original tem uma cópia gratuita do autor linkada acima.
