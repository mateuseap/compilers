# Roteiro oral: Pessoa 2, avaliação (slides 11 a 18)

Tempo-alvo: **8–10 minutos**. Sua história tem 4 atos:

1. separar computação de congruência;
2. mostrar call-by-value e Pair passo a passo;
3. separar tipo estático de classe real;
4. executar método/substituição/despacho e fechar com stuck.

A Pessoa 1 já explicou os termos, `<:`, `fields`, `mtype` e `mbody`. Faça só uma lembrança curta.

## Transição de entrada (10 s)

> "Já sabemos escrever os termos e consultar classes, campos e métodos. Agora vamos ver como esses termos executam. A semântica é small-step: cada regra descreve um único passo."

---

## Slide 11: mapa da Figura 19-3 (50 s)

> "Esta é a Figura 19-3 original, página 258. O julgamento `t → t'` diz que t reduz para t' em um passo. A figura tem duas famílias."
>
> "As três regras de computação fazem a transformação real: uma para campo, uma para método e uma para cast. As cinco regras de congruência só conduzem a avaliação até o próximo subtermo."
>
> "A pergunta é: esta regra calcula o resultado ou apenas escolhe onde calcular? Essa diferença organiza toda a avaliação."

Não leia todas as fórmulas no recorte; os próximos slides ampliam cada parte.

---

## Slide 12: três regras de computação (1 min 20 s)

Avance um cartão por vez.

### E-ProjNew

> "Se `fields(C)` lista os campos, acessar o campo i em `new C(v)` devolve o valor i. `new Cachorro(new Gato()).amigo` vira `new Gato()`. Isso funciona porque o construtor padronizado tem um argumento por campo, na mesma ordem."

### E-InvkNew

> "Se `mbody(m,C)` encontra parâmetros e corpo, a chamada substitui parâmetros pelos argumentos e `this` pelo receptor. `new Gato().falar()` encontra o corpo sobrescrito e vira `new Miado()`."

### E-CastNew

> "Se a classe real C é subtipo do alvo D, o cast desaparece. `(Animal)new Gato()` vira o mesmo `new Gato()`: cast não muda objeto."

Fecho:

> "São as únicas três regras que calculam. Para conseguir aplicá-las, os componentes envolvidos precisam estar em forma de valor."

---

## Slide 13: call-by-value e congruência (1 min 15 s)

Termo:

```text
new Cachorro((Animal)new Gato()).amigo.falar()
```

### Estado inicial

> "Queremos chamar `falar`, mas o receptor ainda contém um objeto cujo argumento é um cast. Call-by-value exige avaliar primeiro."

### Passo 1

> "E-Invk-Recv entra no receptor da chamada; E-Field entra no receptor do campo; E-New-Arg entra no argumento do construtor; só então E-CastNew remove o cast. As regras externas preservam o contexto."

### Passo 2

> "Agora E-ProjNew seleciona o campo `amigo`, sob o contexto E-Invk-Recv. Sai `new Gato().falar()`."

### Passo 3

> "Receptor já é valor: E-InvkNew encontra o corpo em Gato e produz `new Miado()`."

Frase-chave:

> "Congruência leva até o redex; computação faz o passo."

O contexto inicial é `new Cachorro([]).amigo.falar()`: `[]` marca o próximo redex.

---

## Slide 14: Pair com cast (1 min 10 s)

Este é o exemplo formal do livro. Avance com a seta.

1. Contexto `((Pair)[]).snd`. E-ProjNew em `.fst` seleciona o primeiro argumento, outro Pair.
2. E-CastNew remove `(Pair)` porque `Pair <: Pair` pela reflexividade.
3. E-ProjNew em `.snd` seleciona o segundo argumento: `new B()`, um valor.

> "Em cada passo, as regras de congruência apontam o lugar e uma das três regras de computação transforma o redex."

---

## Slide 15: tipo estático versus classe real (1 min)

> "O verificador e o avaliador têm informações diferentes. O campo `amigo` foi declarado Animal, então T-Field conclui tipo estático Animal. Mas o argumento concreto guardado é `new Gato()`: a classe real é Gato."
>
> "O cast `(Gato)` recupera precisão estática para acessar algo específico de Gato. Em runtime ele precisa conferir a classe real. Se a classe real for subtipo do alvo, passa; se não, fica stuck."

Conecte a Pair:

> "No exemplo do livro, `fst` tem tipo estático Object, embora guarde um Pair. Sem cast, `.snd` não tipa."

Distinção para decorar:

- tipo estático: vem da derivação de tipos;
- classe real: nome em `new C(v)`;
- dispatch usa classe real;
- type checker usa tipo estático.

---

## Slide 16: `setfst` por substituição (1 min 15 s)

Cores: azul receptor, marrom argumento, vermelho parâmetro, roxo `this`, verde resultado.

1. Receptor e argumento já são valores.
2. `mbody(setfst,Pair)` dá parâmetro `newfst` e corpo `new Pair(newfst,this.snd)`.
3. Substituição simultânea:
   - `newfst ↦ new B()`;
   - `this ↦ new Pair(new A(),new B())`.
4. Sobra o campo `.snd`; E-New-Arg + E-ProjNew o reduzem.
5. Resultado: `new Pair(new B(),new B())`.

> "E-InvkNew é parecida com beta-redução, mas também substitui `this` e encontra o corpo pela classe do receptor."

---

## Slide 17: `mbody`, despacho dinâmico e recursão aberta (1 min 10 s)

Termo:

```text
new Cachorro(new Gato()).apresentar()
```

1. `apresentar` não está em Cachorro nem Mamifero; `mbody` sobe até Animal.
2. Corpo herdado: `this.falar()`.
3. E-InvkNew substitui `this` pelo receptor **real**, Cachorro.
4. Nova chamada: `new Cachorro(...).falar()`.
5. `mbody(falar,Cachorro)` acha a sobrescrita antes de subir: `new Latido()`.

> "O corpo herdado em Animal chama comportamento sobrescrito em Cachorro. Isso é recursão aberta via `this` e é a essência do despacho dinâmico."

Restrição FJ: todas as versões de `falar` têm tipo `[] → Som`; `override` exige assinatura idêntica.

---

## Slide 18: três formas de stuck (55 s)

1. `new Gato().amigo`: campo não existe; E-ProjNew não casa; T-Field rejeita.
2. `new Som().falar()`: corpo não existe; E-InvkNew não casa; T-Invk rejeita.
3. `(Cachorro)(Animal)new Gato()`:
   - upcast interno desaparece;
   - sobra `(Cachorro)new Gato()`;
   - `Gato <: Cachorro` é falso; E-CastNew não casa;
   - termo pode ser aceito como downcast antes da execução e travar.

### Transição para Pessoa 3

> "A tipagem elimina os dois primeiros travamentos. A exceção prevista pelo progresso é um cast preso `(C)(new D(...))` com `D ≮: C`; ele pode surgir de um downcast ou já ser tipado por T-SCast. Agora veremos as regras que sustentam essa garantia."

---

## Cronometragem

| Slide | Tempo |
|---|---:|
| 11 | 0:50 |
| 12 | 1:20 |
| 13 | 1:15 |
| 14 | 1:10 |
| 15 | 1:00 |
| 16 | 1:15 |
| 17 | 1:10 |
| 18 | 0:55 |
| Transições/margem | 0:45 |
| **Total** | **9:40** |

## Checklist

- [ ] Consigo dizer computação versus congruência sem olhar.
- [ ] Sei a ordem call-by-value e consigo ler a pilha de regras.
- [ ] Consigo reduzir Pair com cast de memória.
- [ ] Sei separar tipo estático de classe real.
- [ ] Sei as duas substituições de E-InvkNew.
- [ ] Sei explicar por que `mbody` produz dispatch dinâmico.
- [ ] Sei os três stuck e qual regra de tipo previne cada um.
- [ ] Consigo fazer a ponte para tipagem.

## Comandos de treino

```bash
cd seminario-featherweight-java/exemplos
python3 fj_trace.py
python3 fj_trace.py "new Cachorro(new Gato()).apresentar()"
python3 fj_trace.py "(Cachorro) (Animal) new Gato()"
```
