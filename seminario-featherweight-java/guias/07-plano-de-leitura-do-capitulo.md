# Plano de leitura do capítulo 19

Você vai apresentar a parte do meio, mas precisa dominar a história inteira. O capítulo tem 18 páginas (247 a 264). Leia em duas passadas: primeiro para entender o argumento; depois para dominar as regras.

Tempo total: cerca de 2h30, dividido como quiser.

---

## Passada 1: a história do capítulo (50 a 60 min)

Leia sem tentar decorar fórmulas. Responda uma pergunta por seção.

### 19.1 Introduction (pp. 247-249)

**Pergunta:** por que FJ precisa existir?

Marque no texto:
- tensão entre completude e compacidade;
- 5 formas de termo;
- FJ é subconjunto estrito de Java;
- aplicação principal: estudar extensões;
- o que FJ mantém e o que corta;
- por que tirar atribuição elimina o heap.

Ao terminar, explique em 30 segundos: "FJ é para Java o que o lambda-cálculo é para linguagens funcionais."

### 19.2 Overview (pp. 249-251)

**Pergunta:** como cada construção avalia intuitivamente?

Reproduza num papel:

```text
new Pair(new A(), new B()).snd
new Pair(new A(), new B()).setfst(new B())
((Pair)new Pair(new Pair(new A(),new B()), new A()).fst).snd
```

Sem olhar as regras formais, explique:
- por que `.snd` escolhe o segundo argumento;
- quais substituições a chamada faz;
- por que o cast é necessário;
- os 3 jeitos de travar;
- ordem call-by-value do último exemplo.

Esta é a seção mais importante para sua fala: ela explica as regras antes de formalizar.

### 19.3 Nominal and Structural Type Systems (pp. 251-254)

**Pergunta:** por que o nome de uma classe é mais que abreviação?

Faça uma tabela:

| Nominal | Estrutural |
|---|---|
| subtipo declarado | subtipo pela forma |
| nome usado em runtime | nome cosmético |
| tipos recursivos simples | tipo fechado e autocontido |
| comum na prática | comum na pesquisa |

Não precisa decorar todas as citações. Entenda os argumentos de vantagem e desvantagem.

### 19.4 Definitions (pp. 254-260)

**Pergunta:** quais peças mínimas definem uma linguagem de classes?

Na primeira passada, identifique:
- Figura 19-1: sintaxe e subtipagem;
- Figura 19-2: consultas à tabela de classes;
- Figura 19-3: avaliação (sua parte);
- Figura 19-4: tipagem;
- por que não há circularidade na checagem de métodos;
- por que existe stupid cast.

Não pare nos exercícios ainda.

### 19.5 Properties (pp. 261-262)

**Pergunta:** o que segurança de tipos significa em FJ?

Escreva com suas palavras:
- preservação: um passo não produz tipo incompatível;
- progresso: termo bem tipado avança, é valor ou falha num downcast;
- campo/método inexistente nunca causa stuck em programa bem tipado.

### 19.6 Encodings vs. Primitive Objects (pp. 262-263)

**Pergunta:** por que as duas abordagens são úteis?

- codificação explica o mecanismo e a compilação;
- primitivo explica diretamente o design e a tipagem;
- ideal: ter a linguagem e uma tradução comprovadamente correta.

### 19.7 Notes (pp. 263-264)

**Pergunta:** em que FJ se diferencia dos trabalhos próximos?

Leia por contexto, não decore. Guarde:
- artigo original usa redução não determinística; livro usa call-by-value;
- há modelos maiores de Java, mas FJ quer ser o menor núcleo útil;
- FJ aparece como base para extensões e compilação que preserva tipos.

---

## Passada 2: dominar as regras (60 a 75 min)

### 1. Copie a Figura 19-3 à mão

Não copie mecanicamente. Ao lado de cada regra escreva:

| Regra | Pergunta que responde |
|---|---|
| E-ProjNew | como obter o valor de um campo? |
| E-InvkNew | como executar o corpo de um método? |
| E-CastNew | quando o cast desaparece? |
| E-Field | o que avaliar antes de projetar? |
| E-Invk-Recv | o que avaliar antes de chamar? |
| E-Invk-Arg | em qual argumento entrar? |
| E-New-Arg | em qual argumento do construtor entrar? |
| E-Cast | o que avaliar antes de testar o cast? |

### 2. Faça os 3 exemplos sem olhar

Use [02-reducoes-passo-a-passo.md](02-reducoes-passo-a-passo.md) apenas para conferir no fim.

### 3. Entenda as dependências

Faça estas ligações:

```text
fields(C)  -> E-ProjNew -> T-Field e T-New
mbody(m,C) -> E-InvkNew
mtype(m,C) -> T-Invk -> garante que mbody existe (lema do progresso)
override   -> tipagem de método
subtyping  -> casts, argumentos, resultado de método, preservação
```

### 4. Leia a Figura 19-4

Você não apresenta essa parte, mas precisa entender a resposta para: "como sabemos que campo e método existem?"

- T-Field consulta `fields`.
- T-Invk consulta `mtype` e checa argumentos.
- O lema 19.5.2 liga tipagem a `fields` e `mbody` existentes.

### 5. Refaça o stupid cast

```text
(A)(Object)new B()  ->  (A)new B()
```

Explique por que:
- o primeiro termo tipa com downcast;
- o segundo tem classes não relacionadas;
- sem T-SCast, a preservação seria quebrada.

---

## Passada 3: ensaio e perguntas (30 min)

1. Apresente slides 11 a 17 em 8-10 minutos.
2. Responda sem consultar:
   - Qual a diferença entre computação e congruência?
   - Por que não há heap?
   - Onde a sobrescrita aparece na avaliação?
   - O que `this` vira?
   - Por que o cast do exemplo é necessário?
   - Por que um programa bem tipado ainda pode travar?
3. Leia [03-perguntas-e-respostas.md](03-perguntas-e-respostas.md) e marque as respostas em que hesitou.
4. Ensaie de novo só esses pontos.

---

## Mapa de dependências conceituais

```text
sintaxe
  -> tabela de classes CT
      -> fields, mtype, mbody, override
          -> regras de avaliação
          -> regras de tipagem
              -> preservação + progresso
                  -> segurança de tipos (com exceção do downcast)
```

Se esse fluxo fizer sentido, você entendeu o capítulo inteiro.
