# Reduções passo a passo

Os três exemplos de avaliação do capítulo, com a regra usada em cada passo. Em cada linha, o trecho entre `«` e `»` é o **redex**: o subtermo que vai ser reduzido.

Classes usadas: `A`, `B` e `Pair` da seção 19.2 (veja [`../exemplos/src/`](../exemplos/src/)).

```text
fields(Pair)          = Object fst, Object snd
mbody(setfst, Pair)   = (newfst, new Pair(newfst, this.snd))
```

---

## Exemplo 1: acesso a campo

```text
  «new Pair(new A(), new B()).snd»
⟶ new B()                                   E-ProjNew
```

`snd` é o **segundo** campo em `fields(Pair)`, então sai o **segundo** argumento do construtor.

---

## Exemplo 2: chamada de método

```text
  «new Pair(new A(), new B()).setfst(new B())»
⟶ new Pair(new B(), «new Pair(new A(), new B()).snd»)       E-InvkNew
⟶ new Pair(new B(), new B())                                 E-ProjNew dentro de E-New-Arg
```

Passo 1 em detalhe (E-InvkNew):

1. O receptor `new Pair(new A(), new B())` e o argumento `new B()` já são valores.
2. `mbody(setfst, Pair) = (newfst, new Pair(newfst, this.snd))`.
3. Substitui no corpo:
   - `newfst ↦ new B()` (o argumento)
   - `this ↦ new Pair(new A(), new B())` (o receptor)
4. Resultado: `new Pair(new B(), new Pair(new A(), new B()).snd)`.

Passo 2: o primeiro argumento do `new Pair` já é valor, então E-New-Arg escolhe o segundo, `...snd`, que reduz por E-ProjNew.

---

## Exemplo 3: cast e campos aninhados

```text
  ((Pair) «new Pair(new Pair(new A(),new B()), new A()).fst»).snd
⟶ («(Pair)new Pair(new A(),new B())»).snd                  E-ProjNew dentro de E-Cast e E-Field
⟶ «new Pair(new A(),new B()).snd»                          E-CastNew dentro de E-Field
⟶ new B()                                                  E-ProjNew
```

| Passo | Contexto de avaliação `E` | Redex | Regra |
|---|---|---|---|
| 1 | `((Pair)[]).snd` | `new Pair(...).fst` | E-ProjNew |
| 2 | `[].snd` | `(Pair)new Pair(...)` | E-CastNew, porque `Pair <: Pair` |
| 3 | `[]` | `new Pair(new A(),new B()).snd` | E-ProjNew |

---

## Exemplo 4: cast que trava

```text
  (A) «(Object) new B()»
⟶ «(A) new B()»                  E-CastNew (B <: Object)
  travado: B <: A é falso, nenhuma regra se aplica
```

- O termo inicial **é bem tipado** (`(Object)new B()` tem tipo `Object`, e `(A)` sobre `Object` é downcast, T-DCast).
- Depois de um passo, `(A) new B()` só tipa com T-SCast (stupid cast).
- É exatamente o caso que o teorema de progresso permite: `t = E[(C)(new D(v̄))]` com `D ≮: C`.
- Em Java, isso lança `ClassCastException`. Rode [`../exemplos/src/Main.java`](../exemplos/src/Main.java) para ver.

---

## Exercício para treinar

Reduza até virar valor, indicando a regra de cada passo:

```text
new Pair(new A(), new B()).setfst(new A()).setfst(new B()).fst
```

<details>
<summary>Resposta</summary>

```text
  «new Pair(new A(), new B()).setfst(new A())».setfst(new B()).fst
⟶ new Pair(new A(), «new Pair(new A(), new B()).snd»).setfst(new B()).fst     E-InvkNew (via E-Invk-Recv, E-Field)
⟶ «new Pair(new A(), new B()).setfst(new B())».fst                             E-ProjNew (via E-New-Arg, E-Invk-Recv, E-Field)
⟶ new Pair(new B(), «new Pair(new A(), new B()).snd»).fst                      E-InvkNew (via E-Field)
⟶ «new Pair(new B(), new B()).fst»                                             E-ProjNew (via E-New-Arg, E-Field)
⟶ new B()                                                                      E-ProjNew
```

</details>
