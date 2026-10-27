# Guia para substituir a Pessoa 3: tipagem e segurança (slides 19 a 25)

Tempo-alvo: **9 minutos**. Objetivo: mostrar como as regras de tipo impedem dois dos três travamentos e por que cast preso continua como exceção.

---

## Antes de começar: três leituras

- `Γ ⊢ t : C`: no ambiente Γ, o termo t tem tipo C.
- Premissas em cima da barra; conclusão embaixo.
- `C̄ <: D̄`: comparação elemento a elemento das sequências.

### Transição da Pessoa 2

> "A avaliação pode ficar sem regra em campo inexistente, método inexistente ou cast inválido. Agora veremos como a tipagem elimina os dois primeiros e isola o terceiro."

---

## Slide 19: tipagem dos termos (2 min)

### T-Var

Se `x:C` está em Γ, então `x` tem tipo C.

Animal: com `Γ = {this:Cachorro}`, temos `Γ ⊢ this : Cachorro`.

### T-Field

1. Descobre o tipo `C0` do receptor.
2. Consulta `fields(C0) = C̄ f̄`.
3. O tipo de `fi` é `Ci`.

```text
new Cachorro(new Gato()).amigo : Animal
```

Mesmo guardando um Gato, o tipo estático do campo é Animal.

### T-Invk

1. Tipa o receptor como C0.
2. Consulta `mtype(m,C0)=D̄→C`.
3. Tipa os argumentos como C̄.
4. Exige `C̄ <: D̄`.
5. Resultado tem tipo C.

```text
new Gato().falar() : Som
```

### T-New

Os argumentos precisam corresponder a todos os campos de `fields(C)`, aceitando subtipos.

```text
new Cachorro(new Gato()) : Cachorro
```

É válido porque o campo espera Animal e `Gato <: Animal`.

**Sem subsunção solta:** FJ põe os testes `<:` dentro das regras necessárias. Isso dá tipo mínimo único.

---

## Slide 20: três regras de cast (2 min)

### T-UCast

Tipo real estático do termo é subtipo do alvo:

```text
(Animal)new Gato() : Animal       Gato <: Animal
```

Seguro; em execução E-CastNew sempre passa.

### T-DCast

Alvo é subtipo do tipo estático do termo:

```text
(Gato)(Animal)new Gato() : Gato   Gato <: Animal
```

Pode passar ou falhar em runtime, porque o termo de tipo Animal poderia ter classe real Cachorro.

### T-SCast

Classes sem relação:

```text
(Cachorro)new Gato() : Cachorro   Gato ≮: Cachorro, Cachorro ≮: Gato
```

Java rejeita; FJ aceita com `stupid warning` para a prova de preservação funcionar.

### Por que é necessário

```text
(A)(Object)new B()     -- tipa com T-DCast
⟶ (A)new B()           -- só T-SCast consegue tipar
```

Sem T-SCast, o passo transformaria termo tipado em termo sem tipo, quebrando preservação. Uma derivação FJ corresponde a Java apenas se não usar T-SCast.

---

## Slide 21: tipagem de método e classe (1 min)

### Método OK em C

- Γ contém parâmetros e `this:C`.
- Corpo tem tipo E0 e `E0 <: retorno declarado`.
- `override` precisa ser válido.

No exemplo:

```text
Som falar() { return new Latido(); }
```

`Latido <: Som`, então o corpo é compatível. Mas a **assinatura** sobrescrita continua `[]→Som`: FJ não permite declarar retorno Latido na subclasse.

### Classe OK

- construtor recebe campos herdados + próprios;
- `super` recebe os herdados;
- `this.f=f` inicializa os próprios;
- todos os métodos são OK.

Não há circularidade: assinaturas são declaradas, então um método pode chamar outro sem precisar verificar o corpo dele antes.

---

## Slide 22: preservação e progresso (2 min)

### Preservação

```text
Se Γ ⊢ t:C e t⟶t', então Γ ⊢ t':C' para algum C' <: C.
```

Memória: **um passo não estraga o tipo**. Ele pode ficar mais específico.

Exemplo:

```text
(Object)new Gato() : Object
⟶ new Gato() : Gato
```

`Gato <: Object`, então preservação vale.

### Progresso

Termo fechado, bem tipado e em forma normal:

- é valor; ou
- é um cast inválido num contexto: `E[(C)(new D(v̄))]` com `D ≮: C`.

Memória: **bem tipado não fica sem próximo passo, salvo cast preso**.

Por que campo e método não travam:
- T-Field prova que o campo está em `fields`.
- T-Invk + bem-formação da tabela garantem `mbody` e aridade correta.

Se só há upcasts, nunca trava.

---

## Slide 23: exercícios (45 s)

- 19.4.1: Object já é topo pela cadeia de `extends` + transitividade.
- 19.4.3: para atribuição, introduzir locações e heap (cap. 13); objetos deixam de ser só termos `new`.
- 19.4.7: `super.m()` deve começar busca na superclasse da classe **onde o método foi escrito**, não na classe dinâmica do receptor.

Avise: as ideias de resposta são do grupo, não soluções oficiais do livro.

## Slide 24: codificação versus primitivo (35 s)

- Cap. 18 codifica objetos: bom para entender implementação/tradução.
- Cap. 19 trata objetos como primitivos: bom para projetar e documentar tipos e semântica.
- O ideal é ligar ambos com uma tradução que preserve tipo e avaliação.

## Slide 25: fechamento (30 s)

Retome os cinco pontos e encerre na segurança:

> "Featherweight Java mostra que o núcleo de classes, herança, métodos e casts pode ser descrito com poucas regras e ainda sustentar um argumento preciso de segurança de tipos."

---

## O que saber sem decorar

- Ler `Γ ⊢ t:C`.
- T-New, T-Field, T-Invk em linguagem simples.
- Diferença upcast/downcast/stupid cast.
- Por que T-SCast é necessário para preservação.
- Preservação ≠ progresso.
- Exceção de progresso: cast preso `E[(C)(new D(v̄))]` com `D ≮: C`; pode vir de downcast ou T-SCast.
- Sobrescrita em FJ exige assinatura idêntica.

## Perguntas prováveis

**Preservação diz que o tipo nunca muda?** Não: pode ficar mais específico (`C' <: C`).

**Progresso diz que sempre termina?** Não. Diz que ou é valor, ou há um passo (salvo cast inválido). Pode haver avaliação infinita.

**Stupid cast executa?** Não se classes não relacionadas: E-CastNew não se aplica. T-SCast só mantém a preservação formal.

**Por que o sistema aceita downcast se pode falhar?** Para modelar Java. A segurança declarada admite exatamente essa falha de runtime.
