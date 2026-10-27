# Relatório de revisão didática e técnica

Documento para os três apresentadores revisarem as mudanças. Fonte de verdade: capítulo 19 do TAPL, especialmente Figuras 19-1 a 19-4.

## Escopo preservado

- Ordem e conteúdo-base das partes das Pessoas 1 e 3 mantidos.
- Nenhuma fórmula, exemplo ou animação anterior dessas partes foi removido.
- Melhorias nelas são adições curtas e identificáveis.
- A parte da Pessoa 2 foi reorganizada e ampliada, conforme autorizado.

## Pessoa 1: acréscimos realizados

| Slide | Acréscimo | Motivo |
|---|---|---|
| 9 | Faixa `Cachorro <: Mamifero <: Animal <: Object` + nota sobre Gato/Cachorro irmãos | Tornar reflexividade/transitividade e nominalidade concretas |
| 10 | Caixa com `fields`, `mtype`, `mbody` no exemplo Cachorro | Preparar as funções que a Pessoa 2 usa na avaliação |

Nenhuma outra mudança foi aplicada diretamente à parte 1.

## Pessoa 2: reformulação principal

| Slide | Mudança final |
|---|---|
| 11 | Figura 19-3 original + distinção computação/congruência |
| 12 | E-ProjNew isolada: `new Pair(...).snd` |
| 13 | E-CastNew isolada: `(Animal)new Cachorro()` |
| 14 | Call-by-value isolado: E-New-Arg + E-ProjNew dentro do construtor |
| 15 | Tipo estático Object versus classe real Pair; por que o cast é necessário |
| 16 | `setfst` com busca em `mbody` e duas substituições |
| 17 | Despacho dinâmico isolado: `new Cachorro().falar()` |
| 18 | Três casos pequenos de stuck |

Os exemplos complexos com campo, cast e chamada no mesmo termo foram removidos. Cada slide ensina primeiro um conceito. Duração projetada: 9 minutos.

## Pessoa 3: acréscimos realizados

| Slide | Acréscimo | Motivo |
|---|---|---|
| 19 | Exemplo `Γ ⊢ new Gato() : Gato` e texto mais curto | Dar leitura concreta ao julgamento |
| 20 | Faixa upcast/downcast/stupid cast com Animal/Gato/Cachorro | Fixar a distinção antes do exemplo A/B |
| 22 | Mnemônicos: “um passo não estraga o tipo” e “bem tipado não fica sem passo, salvo cast preso” | Separar preservação de progresso |

Nenhuma fórmula foi alterada.

## Revisão técnica: correções incorporadas

1. **Chamada por valor:** receptor primeiro, depois argumentos da esquerda para a direita. Regras de congruência apenas transportam a redução.
2. **E-InvkNew:** `mbody` usa a classe real do receptor `new C(v̄)`, não seu tipo estático.
3. **Despacho dinâmico:** `this` é substituído pelo receptor real; uma chamada posterior começa `mbody` nessa classe.
4. **Tipo estático ≠ classe real:** T-Field devolve o tipo declarado, enquanto E-ProjNew revela o valor concreto.
5. **Casts:** upcast sempre passa; downcast pode travar; stupid cast é formalmente tipado apenas para preservação.
6. **Override:** FJ exige assinatura idêntica. Retorno covariante de Java moderno não foi misturado com FJ.
7. **Construtor:** preservada a forma padronizada `C(D̄ ḡ,C̄ f̄){super(ḡ);this.f̄=f̄;}`.
8. **Sem heap:** atribuição após construção não existe; a semântica reescreve termos.
9. **Preservação:** tipo pode ficar mais específico `C' <: C`.
10. **Progresso:** não afirma terminação; admite exatamente um cast preso `D ≮: C`; isso inclui downcast que falha e stupid cast.

## Exemplos validados

- [`../exemplos/animais/`](../exemplos/animais/): hierarquia compilada e executada na JVM.
- [`../exemplos/fj_trace.py`](../exemplos/fj_trace.py): interpretador/type checker mínimo com verificações das Figuras 19-1 a 19-4.
- `python3 exemplos/fj_trace.py`: valida automaticamente exemplos dos slides, preservação passo a passo, caso de progresso, casts, dispatch e exercício do guia 02.

## Sugestões não aplicadas (potencialmente invasivas)

1. Substituir Pair por Animal nas fórmulas das partes 1 e 3. Não aplicado: Pair permanece referência formal do capítulo.
2. Adicionar slides exclusivos de Animal nas partes 1 e 3. Não aplicado: aumentaria a responsabilidade e o tempo dos colegas.
3. Trocar todos os exemplos A/B por Gato/Cachorro. Não aplicado: A/B é essencial para explicar stupid cast e preservação como no livro.
4. Inserir as Figuras 19-1, 19-2 e 19-4 inteiras nos slides dos colegas. Não aplicado: ocuparia espaço e mudaria a estrutura; o PDF permanece disponível para consulta.

## Validação visual exigida

O deck deve passar `scripts/check_deck.mjs` em todos os slides e etapas, sem overflow ou clipping. Também são geradas capturas de todos os estados da Pessoa 2 para revisão visual.
