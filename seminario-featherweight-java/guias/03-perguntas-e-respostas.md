# Perguntas e respostas

Perguntas prováveis na apresentação, com respostas curtas. As do livro estão marcadas com o número do exercício. **As respostas dos exercícios são do grupo, não do livro** (o TAPL não traz solução para eles).

---

## Conceitos

**O que é Featherweight Java, em uma frase?**
Um modelo formal mínimo de Java, com 5 formas de termo, feito para provar segurança de tipos com a menor prova possível.

**Por que não modelar Java inteiro?**
Porque a prova ficaria enorme. FJ corta tudo que deixa a prova mais longa sem mudar o argumento. Modelos maiores existem (Drossopoulou e Eisenbach, Nipkow e Oheimb, Flatt et al.), mas são várias vezes maiores.

**FJ é Java mesmo?**
Sim. É um subconjunto estrito: todo programa FJ compila e roda numa JVM com o mesmo resultado. A pasta [`../exemplos/`](../exemplos/) mostra isso.

**Se não tem atribuição, como FJ consegue ser útil?**
Fica um fragmento funcional de Java, que ainda é Turing-completo (dá para codificar o lambda-cálculo). E o principal uso de FJ é estudar extensões de Java, não escrever programas.

**Por que tirar a atribuição simplifica tanto?**
Sem atribuição não há estado. A avaliação acontece só reescrevendo o termo, sem modelar memória (heap). Objetos são o próprio termo `new C(v̄)`.

**O que é nominal e o que é estrutural?**
Nominal: subtipagem é a declarada com `extends`. Estrutural: subtipagem é decidida comparando a forma dos tipos. Java e FJ são nominais.

**Qual a vantagem do nominal?**
O nome vira etiqueta em tempo de execução (permite cast e `instanceof`), tipos recursivos saem de graça e checar `C <: D` é trivial.

**Por que `this` é variável e não palavra reservada?**
Para a regra E-InvkNew poder substituir `this` pelo receptor do mesmo jeito que substitui os parâmetros.

---

## Avaliação

**Quais são as regras que realmente calculam?**
Três: E-ProjNew (campo), E-InvkNew (método) e E-CastNew (cast). As outras cinco só dizem onde avaliar.

**Por que E-ProjNew funciona só olhando a posição?**
Porque o construtor é obrigado a ter um parâmetro por campo, na ordem de `fields(C)`. O i-ésimo campo é sempre o i-ésimo argumento.

**Qual a diferença entre E-InvkNew e a regra beta do lambda-cálculo?**
Duas: o corpo é achado pela classe do receptor (isso implementa a sobrescrita), e `this` é substituído pelo próprio objeto (recursão aberta).

**O que é recursão aberta?**
Um método pode chamar outro método via `this`, e se uma subclasse sobrescrever esse outro método, a versão da subclasse é usada. Isso funciona porque `this` vira o objeto real, e a busca do método começa na classe dele.

**O cast muda o objeto?**
Não. Em execução ele só confere `C <: D` e some. Igual a Java.

**O que acontece quando um cast falha?**
Em FJ, nenhuma regra se aplica e a computação trava. Em Java, vira `ClassCastException`.

**Por que chamada por valor?**
Para ser consistente com o resto do livro. O artigo original usava uma redução não determinística, como a beta pura.

---

## Tipagem

**Por que FJ não tem regra de subsunção?**
Porque é apresentado de forma algorítmica, como Java: o `<:` aparece só onde é preciso (argumentos de método e construtor). Assim cada termo tem um único tipo mínimo.

**Por que há três regras de cast?**
Upcast (sempre seguro), downcast (pode falhar) e stupid cast (classes não relacionadas). Separar deixa claro qual cast pode falhar.

**O que é um stupid cast e por que FJ aceita, se Java recusa?**
Cast entre classes sem relação de subtipo, como `(A) new B()`. FJ precisa aceitar porque um termo bem tipado pode virar um assim durante a avaliação: `(A)(Object)new B() ⟶ (A)new B()`. Sem essa regra, a preservação seria falsa. A tipagem só corresponde a Java se não usar essa regra.

**O que garante a preservação?**
Que um passo de avaliação não muda o tipo para algo incompatível: o novo tipo é igual ou subtipo do anterior.

**Por que o tipo pode ficar mais específico?**
Porque um upcast some na avaliação. `(Object)new A()` tem tipo `Object`, mas avança para `new A()`, que tem tipo `A`.

**O que garante o progresso?**
Que um termo fechado e bem tipado ou é valor, ou avança, ou está travado num downcast que falha. Campo inexistente e método inexistente nunca acontecem.

**Um programa FJ bem tipado pode travar?**
Só em downcast. Se o programa só tiver upcasts, nunca trava.

**Existe circularidade em tipar métodos que chamam uns aos outros?**
Não, porque o tipo de cada método é declarado. Dá para tipar as classes em qualquer ordem.

---

## Exercícios do livro

**19.4.1. Por que não precisa de uma regra dizendo que `Object` é supertipo de tudo (como S-Top)?**
Porque toda classe declara uma superclasse e não há ciclos. Então toda cadeia de `extends` termina em `Object`, e a transitividade já dá `C <: Object`. Além disso, em FJ os únicos tipos são nomes de classe; não há tipos de outra forma que precisariam de um topo.

**19.4.2. Se FJ não precisasse ser subconjunto de Java, o que daria para simplificar?**
Por exemplo: tirar a chamada `super(...)` do construtor e deixar cada construtor inicializar todos os campos direto (o próprio livro sugere isso); dispensar o construtor escrito, já que ele é totalmente determinado pelos campos; e deixar o receptor `this` implícito.

**19.4.3. Como adicionar atribuição a campos?**
Seguindo o capítulo 13: introduzir locações e uma memória (heap). `new C(v̄)` passa a alocar e devolver uma referência, e as regras de avaliação passam a carregar o estado da memória. A tipagem precisa de um ambiente para as locações.

**19.4.7. Como adicionar `super.m()`?**
A busca do corpo tem que começar na superclasse da classe **onde o método foi escrito**, não na classe do receptor. Então o corpo do método precisa lembrar em que classe foi definido. `this` continua sendo o receptor.

---

## Perguntas de "pegadinha"

**`new A()` é um valor?**
Sim. É `new C(v̄)` com zero argumentos.

**`x` é um valor?**
Não. Variáveis não são valores, e um termo fechado não tem variáveis livres.

**`fields(Object)` dá erro?**
Não. É a sequência vazia `•`. Por isso `new A().fst` trava (não há regra) e também não tipa (`fst` não está em `fields(A)`).

**Um método pode mudar o tipo de retorno ao sobrescrever?**
Não em FJ: `override` exige o mesmo tipo. (Java 5 em diante permite retorno covariante, mas FJ segue a versão mais antiga.)
