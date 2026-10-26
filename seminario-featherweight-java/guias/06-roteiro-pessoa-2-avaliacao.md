# Roteiro detalhado: Pessoa 2, avaliação (slides 11 a 17)

Sua parte começa quando a pessoa 1 já explicou:

- as 5 formas de termo;
- `fields(C)`, `mtype(m,C)` e `mbody(m,C)`;
- subtipagem `C <: D`.

Você não precisa redefinir tudo. Faça uma lembrança de 15 segundos e entre na avaliação.

Tempo-alvo: **8 a 10 minutos**.

---

## Transição de entrada

> "A gente já definiu como um programa FJ é escrito, como a hierarquia de classes funciona e como consultar campos e métodos na tabela de classes. Agora eu vou mostrar como esses termos executam. A semântica é small-step: em vez de executar tudo de uma vez, cada regra descreve um único passo de redução."

---

## Slide 11: Figura 19-3 original (cerca de 50 s)

**Objetivo:** mostrar que o material vem diretamente do livro e dar o mapa da parte.

> "Esta é a Figura 19-3 original do capítulo, na página 258. Ela contém a semântica operacional inteira de FJ. O julgamento no topo, `t → t'`, significa que o termo `t` reduz para `t'` em um passo."
>
> "A figura tem dois grupos. À esquerda estão as três regras de computação: acesso a campo, chamada de método e cast. Essas regras fazem a transformação real. O resto são regras de congruência: elas só dizem em qual pedaço de uma expressão maior devemos aplicar uma redução primeiro."
>
> "Nos próximos slides a gente amplia essas regras e aplica elas em exemplos concretos."

**Se perguntarem por que o artigo usa `R-Field` mas o livro usa `E-ProjNew`:**

> "O artigo original e o capítulo usam nomes diferentes, mas a regra é a mesma. Aqui estamos seguindo os nomes do capítulo: E-ProjNew, E-InvkNew e E-CastNew."

---

## Slide 12: três regras de computação (cerca de 2 min)

### Como ler uma regra de inferência

Antes das três:

> "Cada regra tem premissas em cima da barra e uma conclusão embaixo. Se as condições de cima forem verdadeiras, o passo de baixo pode acontecer."

### E-ProjNew: acesso a campo

Leia em voz alta:

> "Se `fields(C)` devolve a sequência de tipos e nomes dos campos de C, então acessar o campo de posição `i` em `new C(v)` devolve o valor da posição `i`."

Explique o motivo:

> "Isso funciona porque FJ obriga o construtor a receber exatamente um argumento por campo, na mesma ordem dos campos herdados e depois dos próprios. O objeto não tem uma memória separada: os valores estão dentro do próprio termo `new`."

Exemplo rápido:

```text
fields(Pair) = Object fst, Object snd
new Pair(new A(), new B()).snd → new B()
```

### E-InvkNew: chamada de método

Leia:

> "Se `mbody(m,C)` devolve os parâmetros `x` e o corpo `t0`, então chamar `m` sobre um objeto novo substitui os parâmetros pelos argumentos e substitui `this` pelo próprio receptor."

Pontos importantes:

- `mbody` começa a busca na **classe do receptor**; por isso a sobrescrita funciona.
- `this` vira o objeto real; por isso uma chamada `this.m()` pode escolher uma versão sobrescrita na subclasse.
- É parecida com beta-redução: aplica um corpo substituindo valores nos parâmetros.

### E-CastNew: cast

> "Se o tipo real C do objeto é subtipo do alvo D, o cast passa e desaparece. Ele não altera o objeto. Se `C <: D` for falso, nenhuma regra se aplica e FJ trava. Em Java, isso seria uma `ClassCastException`."

### Fechamento do slide

> "Essas são as únicas três regras que realmente transformam um redex. Sem atribuição não há heap: toda a avaliação é reescrita do próprio termo."

---

## Slide 13: cinco regras de congruência (cerca de 1 min)

> "As três regras anteriores só se aplicam quando o receptor e os argumentos já são valores. Para chegar nesse formato, precisamos das regras de congruência. Elas propagam um passo de redução para dentro de uma expressão maior."

Leia os grupos, não cada símbolo:

- **E-Field:** primeiro avalia o objeto antes de acessar o campo.
- **E-Invk-Recv:** primeiro avalia o receptor da chamada.
- **E-Invk-Arg:** depois avalia os argumentos, da esquerda para a direita.
- **E-New-Arg:** avalia os argumentos do construtor, também em ordem.
- **E-Cast:** avalia o termo dentro do cast antes de testar o tipo.

> "Juntas, essas regras definem uma estratégia chamada por valor: só fazemos projeção, invocação ou cast quando o objeto envolvido já está avaliado."

### Contextos de avaliação

> "A expressão `E` com um buraco `[]` é uma forma compacta de dizer a mesma coisa: ela marca o próximo subtermo a reduzir. Por exemplo, `((Pair)[]).snd` diz que primeiro reduzimos o que está dentro do cast, depois o cast, e por último o campo `snd`."

**Detalhe importante:** o artigo original usa redução não determinística. O capítulo usa call-by-value para manter consistência com o resto do TAPL. Se perguntarem, diga isso.

---

## Slide 14: cast passo a passo (cerca de 1 min e 30 s)

Avance uma etapa por vez com a seta. Sempre aponte o sublinhado vermelho.

### Estado inicial

> "O termo quer pegar `fst`, dizer que o resultado é um `Pair`, e então pegar `snd`. O sublinhado mostra o redex do passo atual."

### Passo 1: E-ProjNew dentro de contexto

> "Primeiro o contexto é `((Pair)[]).snd`. Dentro dele temos `new Pair(...).fst`. Como `fst` é o primeiro campo, E-ProjNew devolve o primeiro argumento, que é outro `Pair`."

### Passo 2: E-CastNew

> "Agora o redex é `(Pair)new Pair(...)`. Como `Pair <: Pair` pela reflexividade, E-CastNew elimina o cast."

### Passo 3: E-ProjNew

> "Sobra `new Pair(new A(),new B()).snd`. `snd` é o segundo campo, então sai o segundo argumento: `new B()`. Esse é um valor e a avaliação termina."

**Resumo:**

> "A regra de congruência escolhe o lugar; a regra de computação faz o passo."

---

## Slide 15: por que o cast é necessário (cerca de 1 min)

> "O cast não está ali por causa da avaliação. Em tempo de execução, a gente sabe que `fst` contém um Pair. O problema é o tipo estático."
>
> "O campo `fst` foi declarado como `Object`. Então, depois de acessar `fst`, o verificador de tipos só sabe que o resultado é um `Object`. E `fields(Object)` é vazio, logo `.snd` não tipa."
>
> "O downcast `(Pair)` afirma que aquele `Object` deve ser tratado como `Pair`. Depois disso `.snd` tipa, mas surge uma checagem em tempo de execução. Se o valor não fosse realmente um Pair, a computação travaria."

Conexão útil:

> "Isso é exatamente o custo de baixar um tipo estático: ganhamos acesso aos membros mais específicos, mas aceitamos risco em execução."

---

## Slide 16: chamada de método passo a passo (cerca de 1 min e 30 s)

### Estado inicial

> "Aqui tanto o receptor quanto o argumento já são valores, então podemos aplicar E-InvkNew direto."

### Busca do corpo

> "A classe do receptor é Pair. `mbody(setfst,Pair)` devolve o parâmetro `newfst` e o corpo `new Pair(newfst,this.snd)`."

### Substituições

> "Substituímos `newfst` pelo argumento `new B()`. Também substituímos `this` pelo próprio receptor `new Pair(new A(),new B())`. Esse segundo ponto é o que o livro chama de recursão aberta via `this`."

Resultado intermediário:

```text
new Pair(new B(), new Pair(new A(),new B()).snd)
```

### Último passo

> "O segundo argumento ainda contém um acesso a campo. E-New-Arg leva a avaliação para dentro desse argumento, E-ProjNew reduz `.snd` para `new B()`, e o resultado final é `new Pair(new B(),new B())`."

**Ligação com sobrescrita:**

> "Como `mbody` começa na classe dinâmica do receptor, se uma subclasse sobrescrevesse o método chamado via `this`, seria a versão da subclasse que apareceria."

---

## Slide 17: três formas de travar (cerca de 50 s)

> "Como FJ não tem exceções, erro de execução significa ficar sem regra aplicável. Há três possibilidades: campo inexistente, método inexistente e cast inválido."
>
> "O sistema de tipos, que a próxima pessoa vai explicar, elimina os dois primeiros. Se o programa é bem tipado, todo campo acessado existe e todo método chamado tem corpo com a quantidade certa de parâmetros."
>
> "O cast inválido continua possível porque o downcast é aceito estaticamente. Por isso o teorema de progresso de FJ tem uma exceção: um programa bem tipado pode travar num downcast."

### Ponte para pessoa 3

> "Então a pergunta natural é: quais regras de tipo garantem que campo e método inexistentes nunca chegam à execução? É isso que a próxima parte responde."

---

## Checklist antes de apresentar

Você deve conseguir explicar sem ler:

- [ ] diferença entre regra de computação e congruência;
- [ ] por que E-ProjNew usa a posição do campo;
- [ ] as duas substituições em E-InvkNew;
- [ ] por que `mbody` começa na classe do receptor;
- [ ] por que o cast do exemplo é necessário mesmo sabendo o valor real;
- [ ] os três jeitos de travar;
- [ ] por que não há heap;
- [ ] a frase de transição para tipagem.

## Treino rápido

1. Abra a apresentação no slide 11: `index.html#11`.
2. Grave só sua parte (slides 11 a 17), sem parar.
3. Meta: 8 a 10 minutos.
4. Ouça e confira se você explicou **o porquê** de cada regra, não só leu a fórmula.
5. Faça as perguntas da seção "Avaliação" em [03-perguntas-e-respostas.md](03-perguntas-e-respostas.md) sem consultar a resposta.
