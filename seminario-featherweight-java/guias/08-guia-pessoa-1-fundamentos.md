# Guia para substituir a Pessoa 1: fundamentos (slides 1 a 10)

Tempo-alvo: **8 minutos**. Objetivo: chegar ao slide 10 com a turma sabendo quais termos existem, como a subtipagem nominal nasce e como consultar a tabela de classes.

A hierarquia complementar usada neste guia é FJ válido:

```text
Object
└── Animal
    └── Mamifero
        ├── Cachorro   (sobrescreve falar)
        └── Gato       (sobrescreve falar)

Som
├── Latido
└── Miado
```

Código validado em [`../exemplos/animais/`](../exemplos/animais/).

---

## Slide 1: capa (15 s)

> "Featherweight Java é um núcleo mínimo de Java. Ele mantém classes, herança, métodos, campos, criação de objetos e cast, mas é pequeno o bastante para sua sintaxe, avaliação e tipagem caberem em poucas figuras."

## Slide 2: duas formas de estudar objetos (40 s)

- Cap. 18: **codifica** objetos com registros, referências e funções.
- Cap. 19: objetos e classes são **primitivos** da linguagem.
- FJ é subconjunto estrito: termo FJ é Java válido.

**Não precisa decorar:** nomes de todos os trabalhos citados. Saiba a oposição codificação versus primitivo.

**Pergunta provável:** "Qual abordagem é melhor?"  
**Resposta:** para entender implementação e tradução, codificação; para especificar tipos e semântica diretamente, primitivo. O capítulo 19.6 diz que elas se complementam.

## Slide 3: completude contra compacidade (40 s)

> "Quanto mais Java modelamos, mais pesada fica a prova. FJ corta recursos que aumentam a prova sem mudar o argumento de segurança. O objetivo não é programar aplicações: é estudar linguagem e extensões."

Aplicações: GJ/genéricos, raw types, classes internas, compilação que preserva tipos.

## Slide 4: o que mantém e corta (45 s)

Destaque o corte decisivo: **atribuição**.

> "Campos são inicializados no construtor e não mudam. Sem estado mutável, a semântica não precisa representar heap; um objeto é o próprio termo `new C(v̄)`."

Ainda assim, FJ é Turing-completo: lambda-cálculo pode ser codificado nele.

**Pegadinha:** `this.f=f` existe no construtor, mas é inicialização padronizada, não uma expressão de atribuição disponível na linguagem.

## Slide 5: Pair (1 min)

Explique a forma padronizada:

1. `extends` sempre explícito.
2. Um parâmetro por campo; herdados primeiro.
3. `super(ḡ)` inicializa campos herdados; `this.f̄=f̄` inicializa os novos.
4. Corpo de método é só `return t;`.
5. Receptor sempre explícito.

> "A rigidez não é limitação acidental: ela permite que as regras formais sejam pequenas."

## Slide 6: cinco termos (50 s)

Associe cada sintaxe a uma pergunta:

| Termo | Pergunta |
|---|---|
| `x` | qual variável? |
| `t.f` | qual campo do objeto? |
| `t.m(t̄)` | qual corpo de método aplicar? |
| `new C(t̄)` | como construir o objeto? |
| `(C)t` | o objeto pertence à hierarquia de C? |

`this` é variável, não uma sexta forma. Valor é só `new C(v̄)` com argumentos já valores.

## Slide 7: gramática (50 s)

Não leia símbolo por símbolo. Mostre três níveis:

- `CL`: classe, superclasse, campos, construtor, métodos.
- `K`: construtor completamente determinado pelos campos.
- `M`: retorno, nome, parâmetros e um corpo `return t`.
- `t`: 5 termos; `v`: objeto totalmente avaliado.

A barra em cima significa sequência: `t̄ = t1,...,tn`.

Programa = `(CT,t)`: tabela de classes mais termo principal.

## Slide 8: nominal versus estrutural (1 min)

Use Animal:

```text
class Cachorro extends Mamifero { ... }
class Gato extends Mamifero { ... }
```

Mesmo que Cachorro e Gato tenham os mesmos métodos, um não é subtipo do outro. O nome e a declaração `extends` importam.

- Nominal: `Cachorro <: Mamifero` porque foi declarado.
- Estrutural: dois tipos seriam compatíveis pela forma dos membros.

Vantagens nominal: etiquetas em runtime/cast, recursão simples, checagem de subtipagem barata.

## Slide 9: subtipagem (1 min)

Leia as três regras:

1. Reflexiva: `C <: C`.
2. Transitiva: `C <: D` e `D <: E` dão `C <: E`.
3. Declaração: `class C extends D` dá `C <: D`.

No diagrama adicionado:

```text
Cachorro <: Mamifero <: Animal <: Object
```

Logo `Cachorro <: Animal`. Mas `Gato ≮: Cachorro` e `Cachorro ≮: Gato`.

`CT` mapeia nome para declaração. Condições: nomes existem, Object é especial, não há ciclo.

## Slide 10: funções auxiliares (1 min)

Estas funções ligam as definições às regras seguintes:

- `fields(C)`: campos herdados + campos de C.
- `mtype(m,C)`: tipo do método; sobe se necessário.
- `mbody(m,C)`: parâmetros e corpo; sobe se necessário.
- `override`: se já existia método, o tipo deve ser **idêntico** em FJ.

Exemplo Animal:

```text
fields(Cachorro)       = •
mtype(falar,Cachorro)  = [] → Som
mbody(falar,Cachorro)  = ([], new Latido())
```

### Transição para Pessoa 2

> "Já sabemos escrever termos, decidir subtipagem e consultar campos e métodos. Agora podemos usar essas funções para executar um programa, um passo por vez."

---

## O que saber sem decorar

- Por que retirar atribuição elimina heap explícito.
- 5 termos e única forma de valor.
- Diferença nominal/estrutural.
- As 3 regras de subtipagem.
- O que retorna cada auxiliar e por que `mbody` implementa busca/sobrescrita.
- Construtor padronizado.

## Perguntas rápidas

**Por que não há regra S-Top?** Toda classe, exceto Object, tem superclasse; sem ciclos, toda cadeia termina em Object. Reflexividade + declaração + transitividade já dão `C <: Object`.

**Sobrescrita pode mudar retorno covariantemente?** Java moderno pode; FJ não. `override` exige tipo idêntico.

**Classes mutuamente recursivas não criam problema?** A tabela de classes é global; nomes são conhecidos antes de checar corpos. Tipos dos métodos são declarados.
