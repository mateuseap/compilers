# Cola geral do seminário

Revisão rápida para levar no celular. Se você entende as conexões abaixo, consegue assumir qualquer parte.

---

## Página 1: linguagem e execução

### Ideia central

FJ é um subconjunto mínimo e funcional de Java para formalizar classes, herança e casts e provar segurança de tipos. Sem atribuição, não há heap explícito: objetos são termos `new C(v̄)`.

### Sintaxe em uma linha

```text
classe: class C extends D { C̄ f̄; K M̄ }
termo:  x | t.f | t.m(t̄) | new C(t̄) | (C)t
valor:  new C(v̄)
```

Construtor: parâmetros = campos herdados + próprios; `super` recebe herdados; `this.f=f` inicializa próprios. Método: um único `return t`.

### Nominal

```text
Object > Animal > Mamifero > Cachorro
                            > Gato
```

- `Cachorro <: Animal` por declaração + transitividade.
- Cachorro e Gato são irmãos: nenhum é subtipo do outro.
- Nominal = nome e `extends` importam; estrutural = forma dos membros importa.

### Auxiliares

| Função | Resposta |
|---|---|
| `fields(C)` | campos herdados + próprios |
| `mtype(m,C)` | tipos dos parâmetros → retorno |
| `mbody(m,C)` | parâmetros + corpo; sobe hierarquia |
| `override(m,D,...)` | assinatura idêntica à herdada? |

### Avaliação: computação versus congruência

- **Computação:** muda o redex.
  - E-ProjNew: campo escolhe argumento por posição.
  - E-InvkNew: busca `mbody`; substitui parâmetros e `this`.
  - E-CastNew: se classe real é subtipo do alvo, cast some.
- **Congruência:** escolhe onde reduzir para implementar call-by-value.
  - receptor primeiro;
  - argumentos da esquerda para a direita;
  - só então computação.

### `setfst`

```text
new Pair(new A(),new B()).setfst(new B())
mbody = (newfst, new Pair(newfst,this.snd))
[newfst ↦ new B(), this ↦ receptor]
→ new Pair(new B(), receptor.snd)
→ new Pair(new B(),new B())
```

### Despacho dinâmico

```text
new Cachorro(...).apresentar()
→ new Cachorro(...).falar()     // apresentar herdado substitui this pelo receptor real
→ new Latido()                  // mbody começa em Cachorro, acha override
```

### 3 formas de stuck

1. campo inexistente; T-Field previne;
2. método inexistente; T-Invk previne;
3. cast inválido; bem tipado ainda pode chegar aqui.

---

## Página 2: tipagem e segurança

### Julgamento

`Γ ⊢ t:C`: no ambiente Γ, t tem tipo C. Γ mapeia variáveis a tipos.

### Regras-chave

- T-Var: procura em Γ.
- T-Field: tipa receptor e procura campo em `fields`.
- T-Invk: usa `mtype`; cada argumento pode ser subtipo do parâmetro.
- T-New: argumentos correspondem a todos os campos, aceitando subtipos.

Sem subsunção separada: testes `<:` ficam nas regras; cada termo tem tipo mínimo único.

### Tipo estático versus classe real

```text
new Cachorro(new Gato()).amigo
```

- tipo estático: Animal (declaração do campo);
- classe real: Gato (valor armazenado);
- `(Gato)...amigo` recupera precisão, mas checa em runtime.

### Casts

| Cast | Relação | Exemplo | Runtime |
|---|---|---|---|
| upcast | origem <: alvo | `(Animal)new Gato()` | sempre passa |
| downcast | alvo <: tipo estático | `(Gato)(Animal)new Gato()` | pode falhar |
| stupid | não relacionados | `(Cachorro)new Gato()` | Java rejeita; FJ tipa com warning e trava |

T-SCast existe para preservação:

```text
(A)(Object)new B()  -- T-DCast
→ (A)new B()        -- só T-SCast tipa
```

### Método e classe OK

- Corpo do método tipado com parâmetros + `this:C`.
- Tipo do corpo pode ser subtipo do retorno.
- Sobrescrita: assinatura idêntica em FJ.
- Construtor segue forma padronizada; métodos OK.

### Teoremas

**Preservação:** se `t:C` e `t→t'`, então `t':C'` com `C' <: C`.  
Frase: **um passo não estraga o tipo**.

**Progresso:** fechado + bem tipado + não avança ⇒ valor ou cast preso `(C)(new D(v̄))` com `D ≮: C`.  
Frase: **bem tipado não fica sem próximo passo, salvo cast**.

Progresso não significa terminar; pode reduzir para sempre.

### Transições

- Pessoa 1 → 2: "Definimos termos e consultas; agora vamos executar."
- Pessoa 2 → 3: "Vimos onde pode travar; agora veremos como tipos evitam isso."
- Fecho: pequeno núcleo, semântica precisa, prova manejável, base para extensões.

### Perguntas-relâmpago

- Por que não heap? Sem mutação.
- Por que cast necessário no Pair? `fst:Object`, mas classe real Pair.
- Por que `this`? vira receptor real; permite recursão aberta/despacho.
- Sobrescrita covariante? Não em FJ; assinatura idêntica.
- Bem tipado trava? Só num cast preso; isso inclui downcast que falha e termo com T-SCast.
- FJ é Java? Subconjunto estrito; o cálculo omite muitos recursos.
