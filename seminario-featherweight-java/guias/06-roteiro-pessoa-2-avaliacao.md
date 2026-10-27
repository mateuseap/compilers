# Roteiro oral: Pessoa 2, avaliação (slides 11 a 18)

Tempo-alvo: **8–10 minutos**. Regra didática: um conceito por exemplo; só o exemplo formal de Pair combina vários conceitos no final da progressão.

## Transição de entrada

> "Já sabemos quais termos existem e como consultar classes, campos e métodos. Agora veremos como um termo executa em pequenos passos."

---

## Slide 11: computação versus congruência (50 s)

> "Esta é a Figura 19-3 original, página 258. `t → t'` significa que t reduz para t' em um passo."
>
> "Há três regras de computação: campo, método e cast. Elas produzem o passo real. Há cinco regras de congruência: elas não calculam o resultado; apenas conduzem a avaliação para dentro de uma expressão maior."

Frase para memorizar: **congruência encontra o redex; computação reduz o redex.**

---

## Slide 12: E-ProjNew, um campo (1 min)

Expressão:

```text
new Pair(new A(), new B()).snd
```

Avance:

1. `fields(Pair) = Object fst, Object snd`.
2. `snd` está na segunda posição.
3. O construtor padronizado guarda `new B()` na segunda posição.
4. Resultado: `new B()`.

> "E-ProjNew seleciona por posição. Isso só é possível porque FJ obriga o construtor a ter um argumento por campo, na mesma ordem."

Nenhum método, cast ou sobrescrita ainda.

---

## Slide 13: E-CastNew, um cast (55 s)

Expressão:

```text
(Animal)new Cachorro()
```

1. Classe real: Cachorro.
2. Alvo: Animal.
3. `Cachorro <: Animal` pela cadeia de `extends`.
4. E-CastNew remove o cast.
5. Resultado continua `new Cachorro()`.

> "Cast válido não modifica o objeto. Ele apenas verifica a relação de subtipagem e desaparece."

---

## Slide 14: call-by-value e E-New-Arg (1 min)

Expressão:

```text
new Pair(new Pair(new A(), new B()).fst, new B())
```

Pergunta: o `new Pair` externo já é um valor? **Não**, porque o primeiro argumento ainda é um acesso a campo.

1. E-New-Arg permite reduzir dentro do primeiro argumento.
2. Nesse argumento, E-ProjNew transforma `new Pair(new A(),new B()).fst` em `new A()`.
3. O contexto externo é preservado.
4. Resultado: `new Pair(new A(),new B())`, agora valor.

> "E-ProjNew faz a redução interna; E-New-Arg permite que esse passo aconteça dentro do construtor externo."

Frase para memorizar: **call-by-value avalia os argumentos antes de considerar `new C(...)` um valor.**

---

## Slide 15: tipo estático versus classe real (1 min)

Termo:

```text
new Pair(new Pair(new A(),new B()), new A()).fst
```

- O campo `fst` foi declarado `Object`; T-Field devolve tipo estático Object.
- O valor guardado é `new Pair(new A(),new B())`; classe real Pair.
- Sem cast, tentar `.snd` falha na tipagem: `fields(Object)` é vazio.
- Com `((Pair)...fst).snd`, o cast recupera precisão estática.
- Runtime confere se a classe real é Pair.

> "O type checker usa o tipo declarado. O avaliador encontra a classe no termo `new`. O cast conecta essas duas visões."

---

## Slide 16: E-InvkNew e `setfst` (1 min 30 s)

Expressão:

```text
new Pair(new A(),new B()).setfst(new B())
```

1. Receptor e argumento já são valores.
2. `mbody(setfst,Pair)` retorna:
   - parâmetro `newfst`;
   - corpo `new Pair(newfst,this.snd)`.
3. Substituição simultânea:
   - `newfst ↦ new B()`;
   - `this ↦ new Pair(new A(),new B())`.
4. Intermediário:

```text
new Pair(new B(), new Pair(new A(),new B()).snd)
```

5. E-New-Arg entra no segundo argumento e E-ProjNew reduz `.snd`.
6. Resultado: `new Pair(new B(),new B())`.

> "E-InvkNew é parecida com beta-redução, mas também substitui `this` e usa `mbody` para achar o corpo."

---

## Slide 17: despacho dinâmico isolado (1 min)

Declarações mostradas no slide:

```java
class Animal extends Object {
  Som falar() { return new Som(); }
}
class Cachorro extends Animal {
  Som falar() { return new Latido(); }
}
```

Expressão:

```text
new Cachorro().falar()
```

1. Receptor real é `new Cachorro()`.
2. `mbody(falar,Cachorro)` começa a busca em Cachorro.
3. Encontra a versão sobrescrita antes de subir para Animal.
4. Corpo retorna `new Latido()`.

> "Despacho dinâmico significa que a classe real do receptor decide onde começa a busca. O tipo de retorno declarado permanece Som nas duas versões, porque FJ exige assinatura idêntica no override."

Não há campos, argumentos ou casts neste exemplo.

---

## Slide 18: três formas de stuck (55 s)

1. `new A().fst`: `fields(A)` é vazio; E-ProjNew não se aplica; T-Field rejeita.
2. `new A().setfst(new B())`: `mbody(setfst,A)` é indefinido; E-InvkNew não se aplica; T-Invk rejeita.
3. `(Gato)new Cachorro()`: `Cachorro <: Gato` é falso; E-CastNew não se aplica. T-SCast pode formar uma derivação FJ com warning, mas runtime trava.

> "Stuck significa que o termo não é valor e nenhuma regra de avaliação se aplica. A tipagem elimina os dois primeiros. O cast preso permanece como exceção do progresso."

## Transição para Pessoa 3

> "Vimos exatamente onde a avaliação pode ficar sem regra. Agora veremos como as regras de tipo garantem campo e método existentes e isolam o risco dos casts."

---

## Cronometragem

| Slide | Tempo |
|---|---:|
| 11 | 0:50 |
| 12 | 1:00 |
| 13 | 0:55 |
| 14 | 1:00 |
| 15 | 1:00 |
| 16 | 1:30 |
| 17 | 1:00 |
| 18 | 0:55 |
| Transições/margem | 0:50 |
| **Total** | **9:00** |

## Checklist

- [ ] Sei distinguir computação de congruência.
- [ ] Sei explicar E-ProjNew sem misturar outros conceitos.
- [ ] Sei explicar que cast válido não muda objeto.
- [ ] Sei dizer o papel separado de E-New-Arg e E-ProjNew.
- [ ] Sei separar tipo estático de classe real.
- [ ] Sei fazer as duas substituições de setfst.
- [ ] Sei explicar despacho apenas com Animal/Cachorro.
- [ ] Sei os três stuck e qual regra de tipo previne cada um.

## Comandos para treinar

```bash
cd seminario-featherweight-java/exemplos
python3 fj_trace.py
python3 fj_trace.py "new Pair(new Pair(new A(), new B()).fst, new B())"
python3 fj_trace.py "(Animal) new Cachorro()"
python3 fj_trace.py "new Cachorro().falar()"
```
