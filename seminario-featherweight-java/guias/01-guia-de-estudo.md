# Guia de estudo: Featherweight Java

Baseado no capítulo 19 de *Types and Programming Languages* (Benjamin C. Pierce, MIT Press, 2002), disponível em [`../livro/`](../livro/). As figuras citadas (19-1 a 19-4) estão nas páginas 255 a 259.

Ordem sugerida de leitura: este guia, depois o capítulo, depois o [passo a passo das reduções](02-reducoes-passo-a-passo.md), e por fim as [perguntas](03-perguntas-e-respostas.md).

---

## 1. O que é e por que existe

**Featherweight Java (FJ)** é um modelo formal mínimo de Java, proposto por Igarashi, Pierce e Wadler em 1999.

- **Objetivo:** provar que o sistema de tipos de Java é seguro, com a prova mais curta possível.
- **Estratégia:** cortar todo recurso que deixa a prova mais longa sem mudar o argumento central.
- **Propriedade-chave:** é um **subconjunto estrito** de Java. Todo programa FJ é um programa Java que compila e roda com o mesmo resultado.
- **Uso principal:** servir de base para estudar extensões de Java. Genéricos (GJ, que virou o Java 5), raw types e classes internas foram formalizados em cima de FJ.

> "Inside every large language is a small language struggling to get out."

### Capítulo 18 contra capítulo 19

| | Cap. 18 | Cap. 19 (FJ) |
|---|---|---|
| Objetos são | **codificados** com registros, referências e subtipagem do lambda-cálculo | **primitivos**: a própria linguagem tem classes |
| Bom para | entender o mecanismo por baixo, como um compilador traduz objetos | projetar e documentar a linguagem, falar de tipos de objetos diretamente |

---

## 2. O que FJ mantém e o que corta

**Mantém:** classes mutuamente recursivas, criação de objetos, acesso a campo, chamada de método, sobrescrita, recursão via `this`, subtipagem e cast.

**Corta:** atribuição, interfaces, sobrecarga, `super.m()`, `null`, tipos primitivos (`int`, `boolean`), métodos abstratos, classes internas, sombreamento de campos, modificadores de acesso, exceções, concorrência e reflexão.

**O corte mais importante é a atribuição.** Campos são definidos no construtor e nunca mudam. Consequências:
- FJ é um fragmento **funcional** de Java.
- Não precisa modelar memória (heap): a avaliação acontece inteira na sintaxe.
- Mesmo assim é **Turing-completo**: dá para codificar o lambda-cálculo dentro de FJ.

---

## 3. Sintaxe (Figura 19-1)

```text
CL ::= class C extends C { C̄ f̄; K M̄ }            declaração de classe
K  ::= C(C̄ f̄) { super(f̄); this.f̄ = f̄; }          construtor
M  ::= C m(C̄ x̄) { return t; }                    método

t  ::= x                                         variável
     | t.f                                       acesso a campo
     | t.m(t̄)                                    chamada de método
     | new C(t̄)                                  criação de objeto
     | (C) t                                     cast

v  ::= new C(v̄)                                  valor
```

- **Barra em cima** (`t̄`) significa sequência: `t1, ..., tn`.
- **Só 5 formas de termo.** Não há `if`, operadores, números. Tudo é objeto.
- **Valores** são objetos com todos os argumentos já avaliados.
- `this` é uma **variável** (não palavra reservada), ligada implicitamente em todo método.
- Um **programa** é o par `(CT, t)`: a tabela de classes e o termo inicial (o `main`).

### Convenções rígidas

1. `extends` sempre escrito, mesmo `extends Object`.
2. Construtor sempre escrito, com **um parâmetro por campo** (incluindo os herdados), na ordem: campos da superclasse primeiro.
3. Corpo do construtor: `super(campos herdados); this.f = f;` para os próprios.
4. Receptor sempre explícito: `this.snd`, nunca `snd`.
5. Corpo de método é um único `return t;`.
6. `super` e `=` só aparecem no construtor.

### Exemplo do livro

```java
class A extends Object { A() { super(); } }
class B extends Object { B() { super(); } }

class Pair extends Object {
  Object fst;
  Object snd;
  Pair(Object fst, Object snd) { super(); this.fst=fst; this.snd=snd; }
  Pair setfst(Object newfst) { return new Pair(newfst, this.snd); }
}
```

Esses arquivos estão em [`../exemplos/src/`](../exemplos/src/) e rodam numa JVM.

---

## 4. Tipos nominais (seção 19.3)

| Estrutural | Nominal |
|---|---|
| Nome do tipo é só abreviação: `NatPair = {fst:Nat, snd:Nat}` | Todo tipo tem nome e é usado pelo nome |
| Subtipagem comparando a **forma** dos tipos | Subtipagem é a que foi **declarada** com `extends` |
| Comum em pesquisa (ML, Haskell) | Comum na prática (Java, C#, C++) |

**Vantagens do nominal:**
- O nome vira **etiqueta em tempo de execução**: permite cast, `instanceof`, serialização, reflexão.
- **Tipos recursivos de graça**: `class List { List next; }` funciona sem mecanismo extra.
- Checar `C <: D` é quase trivial: basta subir a cadeia de `extends`.

**Desvantagem:** fica desconfortável com polimorfismo (`List<T>` não é um nome atômico). Por isso a literatura prefere o estrutural.

---

## 5. Subtipagem e tabela de classes (Figura 19-1)

```text
                    C <: D    D <: E        CT(C) = class C extends D {...}
  ──────           ────────────────         ───────────────────────────────
  C <: C                C <: E                         C <: D
 (reflexiva)         (transitiva)                    (extends)
```

- **Tabela de classes `CT`**: mapeia cada nome de classe para sua declaração.
- **`Object`** não está na tabela, não tem campos nem métodos.
- **Condições de sanidade:** toda classe citada existe; `Object` não está em `CT`; não há ciclos em `<:`.

---

## 6. Funções auxiliares (Figura 19-2)

| Função | Devolve | Regra |
|---|---|---|
| `fields(C)` | todos os campos `C̄ f̄` | `fields(Object) = •` (vazio). Senão, campos da superclasse **seguidos** dos de `C`. |
| `mtype(m, C)` | tipo `B̄ → B` | procura `m` em `C`; se não estiver lá, `mtype(m, D)` na superclasse |
| `mbody(m, C)` | `(x̄, t)`: parâmetros e corpo | mesma busca subindo a hierarquia. **É aqui que mora a sobrescrita.** |
| `override(m, D, C̄ → C0)` | sobrescrita válida? | se `m` existe em `D`, o tipo tem que ser **idêntico** |

Exemplos:
- `fields(Pair) = Object fst, Object snd`
- `mtype(setfst, Pair) = Object → Pair`
- `mbody(setfst, Pair) = (newfst, new Pair(newfst, this.snd))`

---

## 7. Avaliação (Figura 19-3)

Semântica **small-step**, **chamada por valor**.

### As três regras de computação (fazem o trabalho)

```text
       fields(C) = C̄ f̄
  ─────────────────────────────                     (E-ProjNew)
   (new C(v̄)).fi  ⟶  vi

       mbody(m, C) = (x̄, t0)
  ──────────────────────────────────────────────── (E-InvkNew)
   (new C(v̄)).m(ū) ⟶ [x̄ ↦ ū, this ↦ new C(v̄)] t0

            C <: D
  ──────────────────────────────                    (E-CastNew)
   (D)(new C(v̄)) ⟶ new C(v̄)
```

- **E-ProjNew:** como o construtor tem um argumento por campo, na ordem de `fields`, o i-ésimo campo é o i-ésimo argumento.
- **E-InvkNew:** parecida com a regra beta do lambda-cálculo, com duas diferenças:
  1. o corpo é achado pela **classe do receptor** (isso dá a sobrescrita);
  2. `this` é substituído pelo **próprio receptor** (recursão aberta).
- **E-CastNew:** em tempo de execução o cast só **confere** `C <: D` e some. O objeto não muda.

### As cinco regras de congruência (escolhem onde avaliar)

`E-Field`, `E-Invk-Recv`, `E-Invk-Arg`, `E-New-Arg`, `E-Cast`. Elas dizem: avalie primeiro o receptor, depois os argumentos da esquerda para a direita.

Forma equivalente com **contextos de avaliação**:

```text
E ::= [] | E.f | E.m(t̄) | v.m(v̄, E, t̄) | new C(v̄, E, t̄) | (C)E
```

O buraco `[]` marca o próximo subtermo a reduzir.

### Quando a computação trava

1. Acessar campo que a classe não tem.
2. Chamar método que a classe não tem ("message not understood").
3. Cast para algo que não é superclasse: `(A) new B()`.

FJ não tem exceções: **travar é o erro**. Em Java, o caso 3 vira `ClassCastException`.

---

## 8. Tipagem (Figura 19-4)

`Γ ⊢ t : C` lê-se "no ambiente Γ, o termo t tem tipo C". Γ mapeia variáveis para tipos.

```text
   x:C ∈ Γ                Γ ⊢ t0 : C0    fields(C0) = C̄ f̄
  ─────────  (T-Var)     ──────────────────────────────────  (T-Field)
  Γ ⊢ x : C                      Γ ⊢ t0.fi : Ci

   Γ ⊢ t0 : C0   mtype(m, C0) = D̄ → C   Γ ⊢ t̄ : C̄   C̄ <: D̄
  ───────────────────────────────────────────────────────────  (T-Invk)
                     Γ ⊢ t0.m(t̄) : C

   fields(C) = D̄ f̄   Γ ⊢ t̄ : C̄   C̄ <: D̄
  ──────────────────────────────────────  (T-New)
             Γ ⊢ new C(t̄) : C
```

**Não há regra de subsunção solta.** O `<:` aparece só onde é necessário (argumentos). Essa forma é **algorítmica**: cada termo tem um único tipo mínimo, como em Java.

### As três regras de cast

| Regra | Condição | Nome |
|---|---|---|
| T-UCast | `D <: C` | upcast: sempre seguro |
| T-DCast | `C <: D` e `C ≠ D` | downcast: pode falhar em execução |
| T-SCast | `C` e `D` não relacionados, com *stupid warning* | stupid cast |

**Por que FJ aceita o stupid cast, se Java recusa?** Porque um termo bem tipado pode **virar** um stupid cast durante a avaliação:

```text
(A)(Object)new B()      tipa com T-DCast (A <: Object)
⟶ (A)new B()            agora A e B não são relacionados: só T-SCast tipa
```

Sem T-SCast, o teorema de preservação seria falso. Uma tipagem FJ corresponde a uma tipagem Java **só se não usar** T-SCast.

### Métodos e classes

- **Método OK em C:** o corpo é tipado com os parâmetros e `this : C`; o tipo do corpo pode ser subtipo do declarado; e a sobrescrita respeita `override`.
- **Classe OK:** o construtor recebe os campos herdados e os próprios, chama `super` com os herdados, e todo método é OK.
- **Sem circularidade:** o tipo de cada método é declarado, então dá para tipar as classes em qualquer ordem.

---

## 9. Segurança de tipos (seção 19.5)

**Preservação.** Se `Γ ⊢ t : C` e `t ⟶ t'`, então `Γ ⊢ t' : C'` para algum `C' <: C`.
O tipo pode ficar **mais específico**, nunca diferente. Ex.: `(Object)new A()` tem tipo `Object` e avança para `new A()`, tipo `A`.

**Progresso.** Se `t` é fechado, bem tipado e não avança, então `t` é um valor, **ou** `t = E[(C)(new D(v̄))]` com `D ≮: C`.
Ou seja: a única forma de travar é um **downcast que falha**. Campo e método inexistentes nunca acontecem em programa bem tipado.

**Corolário:** programa que só tem upcasts nunca trava.

---

## 10. Resumo para memorizar

- 5 termos: variável, campo, método, `new`, cast.
- Subtipagem nominal, vinda de `extends`.
- 3 regras de computação + 5 de congruência, chamada por valor, sem heap.
- 3 regras de cast, incluindo o stupid cast, que existe para a preservação funcionar.
- Bem tipado só trava em downcast.
