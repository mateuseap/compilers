# Exemplos executáveis

Featherweight Java é um subconjunto estrito de Java: todo programa FJ compila e roda numa JVM normal. Aqui estão os termos usados nos slides, prontos para rodar.

## Estrutura

| Arquivo | O que tem |
|---|---|
| `src/A.java`, `src/B.java`, `src/Pair.java` | As classes da seção 19.2 do livro |
| `src/Main.java` | Avalia os termos dos slides e imprime o resultado |
| `erros/SemCast.java` | Slide 14: `...fst.snd` sem cast não tipa |
| `erros/StupidCast.java` | Slide 18: `(A) new B()` é rejeitado pelo `javac` |

`main`, `toString` e `println` são Java comum, adicionados só para observar o resultado. As classes e os termos são FJ puro.

## Como rodar

Precisa de um JDK (17 ou mais novo). Na pasta `exemplos/`:

```bash
javac -d /tmp/fj src/*.java
java -cp /tmp/fj Main
```

Saída esperada:

```text
setfst      -> new Pair(new B(), new B())
cast + snd  -> new B()
upcast      -> new A()
(A)(Object)new B() -> ClassCastException (em FJ: travado)
```

Compare com os slides 13 e 15: os resultados são os mesmos que as regras de avaliação produzem no papel.

## Ver os erros de tipo

```bash
javac -d /tmp/fj src/A.java src/B.java src/Pair.java erros/SemCast.java
# erros/SemCast.java:4: error: cannot find symbol

javac -d /tmp/fj src/A.java src/B.java src/Pair.java erros/StupidCast.java
# erros/StupidCast.java:3: error: incompatible types: B cannot be converted to A
```

O segundo erro é exatamente o "stupid cast": Java recusa, FJ só aceita com o aviso da regra T-SCast.
