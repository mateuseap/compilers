#!/usr/bin/env python3
"""Featherweight Java em ~250 linhas, seguindo as Figuras 19-1 a 19-4 do TAPL.

Serve para estudar e para conferir os slides: mostra cada passo de avaliação
com a regra usada (de fora para dentro) e o tipo de cada termo.

    python3 fj_trace.py                         # roda as verificações dos slides
    python3 fj_trace.py "new Gato().falar()"    # mostra a redução de um termo

Termos usam a sintaxe de FJ: new C(...), t.f, t.m(...), (C) t, variáveis.
"""
import sys

# ---------------------------------------------------------------- tabelas de classes
# Cada classe: (superclasse, [(tipo, campo)], {metodo: (retorno, [(tipo, param)], corpo)})
# Os corpos são termos em texto; são lidos pelo parser abaixo.

PAIR_CT = {
    "A": ("Object", [], {}),
    "B": ("Object", [], {}),
    "Pair": ("Object", [("Object", "fst"), ("Object", "snd")],
             {"setfst": ("Pair", [("Object", "newfst")], "new Pair(newfst, this.snd)")}),
}

ANIMAIS_CT = {
    "Som": ("Object", [], {}),
    "Latido": ("Som", [], {}),
    "Miado": ("Som", [], {}),
    "Animal": ("Object", [], {"falar": ("Som", [], "new Som()"),
                              "apresentar": ("Som", [], "this.falar()")}),
    "Mamifero": ("Animal", [], {}),
    "Cachorro": ("Mamifero", [("Animal", "amigo")], {"falar": ("Som", [], "new Latido()")}),
    "Gato": ("Mamifero", [], {"falar": ("Som", [], "new Miado()"),
                                "miar": ("Som", [], "new Miado()")}),
}


class Stuck(Exception):
    pass


class TypeError_(Exception):
    pass


# ---------------------------------------------------------------- parser de termos
def tokenize(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c.isalnum() or c == "_":
            j = i
            while j < len(s) and (s[j].isalnum() or s[j] == "_"):
                j += 1
            out.append(s[i:j]); i = j
        else:
            out.append(c); i += 1
    return out


def parse(s):
    toks = tokenize(s)
    pos = [0]

    def peek(k=0):
        return toks[pos[0] + k] if pos[0] + k < len(toks) else None

    def eat(x=None):
        t = toks[pos[0]]
        if x is not None and t != x:
            raise SyntaxError(f"esperava {x!r}, achei {t!r} em {s!r}")
        pos[0] += 1
        return t

    def args():
        eat("(")
        xs = []
        if peek() != ")":
            xs.append(unary())
            while peek() == ",":
                eat(","); xs.append(unary())
        eat(")")
        return xs

    def unary():
        # cast: (C) seguido de termo; o cast se aplica a todo o termo pós-fixo à direita
        if peek() == "(" and peek(1) and peek(1)[0].isupper() and peek(2) == ")":
            eat("("); c = eat(); eat(")")
            return ("cast", c, unary())
        return postfix()

    def postfix():
        t = primary()
        while peek() == ".":
            eat(".")
            name = eat()
            t = ("invk", t, name, args()) if peek() == "(" else ("field", t, name)
        return t

    def primary():
        if peek() == "new":
            eat("new"); c = eat()
            return ("new", c, args())
        if peek() == "(":
            eat("("); t = unary(); eat(")")
            return t
        return ("var", eat())

    t = unary()
    if pos[0] != len(toks):
        raise SyntaxError(f"sobrou {toks[pos[0]:]} em {s!r}")
    return t


def show(t):
    k = t[0]
    if k == "var":
        return t[1]
    if k == "field":
        return f"{show_recv(t[1])}.{t[2]}"
    if k == "invk":
        return f"{show_recv(t[1])}.{t[2]}({', '.join(map(show, t[3]))})"
    if k == "new":
        return f"new {t[1]}({', '.join(map(show, t[2]))})"
    return f"({t[1]}) {show(t[2])}"


def show_recv(t):
    return f"({show(t)})" if t[0] == "cast" else show(t)


# ---------------------------------------------------------------- funções auxiliares (Fig. 19-2)
class FJ:
    def __init__(self, ct):
        self.ct = {c: (d, fs, {m: (r, ps, parse(b)) for m, (r, ps, b) in ms.items()})
                   for c, (d, fs, ms) in ct.items()}

    def fields(self, c):
        if c == "Object":
            return []
        d, fs, _ = self.ct[c]
        return self.fields(d) + fs

    def lookup(self, m, c, path=None):
        """Sobe a hierarquia a partir de c procurando m. Devolve a classe onde achou."""
        if path is not None:
            path.append(c)
        if c == "Object":
            return None
        d, _, ms = self.ct[c]
        return c if m in ms else self.lookup(m, d, path)

    def mtype(self, m, c):
        owner = self.lookup(m, c)
        if owner is None:
            return None
        r, ps, _ = self.ct[owner][2][m]
        return [p[0] for p in ps], r

    def mbody(self, m, c, path=None):
        owner = self.lookup(m, c, path)
        if owner is None:
            return None
        _, ps, body = self.ct[owner][2][m]
        return [p[1] for p in ps], body

    def sub(self, c, d):
        # C <: C ; transitiva ; CT(C) = class C extends D  =>  C <: D
        while True:
            if c == d:
                return True
            if c == "Object":
                return False
            c = self.ct[c][0]

    # ------------------------------------------------------------ avaliação (Fig. 19-3)
    @staticmethod
    def is_value(t):
        return t[0] == "new" and all(FJ.is_value(a) for a in t[2])

    def step(self, t):
        """Um passo chamada-por-valor. Devolve (t', regras de fora para dentro)."""
        k = t[0]
        if k == "field":
            t0 = t[1]
            if not self.is_value(t0):
                t1, rs = self.step(t0)
                return ("field", t1, t[2]), ["E-Field"] + rs
            names = [f for _, f in self.fields(t0[1])]
            if t[2] not in names:
                raise Stuck(f"campo {t[2]} não existe em {t0[1]}")
            return t0[2][names.index(t[2])], ["E-ProjNew"]
        if k == "invk":
            t0, m, xs = t[1], t[2], t[3]
            if not self.is_value(t0):
                t1, rs = self.step(t0)
                return ("invk", t1, m, xs), ["E-Invk-Recv"] + rs
            for i, a in enumerate(xs):
                if not self.is_value(a):
                    a1, rs = self.step(a)
                    return ("invk", t0, m, xs[:i] + [a1] + xs[i + 1:]), ["E-Invk-Arg"] + rs
            mb = self.mbody(m, t0[1])
            if mb is None or len(mb[0]) != len(xs):
                raise Stuck(f"método {m} não existe em {t0[1]}")
            params, body = mb
            return subst(body, dict(zip(params, xs)) | {"this": t0}), ["E-InvkNew"]
        if k == "new":
            for i, a in enumerate(t[2]):
                if not self.is_value(a):
                    a1, rs = self.step(a)
                    return ("new", t[1], t[2][:i] + [a1] + t[2][i + 1:]), ["E-New-Arg"] + rs
            raise Stuck("já é valor")
        if k == "cast":
            if not self.is_value(t[2]):
                t1, rs = self.step(t[2])
                return ("cast", t[1], t1), ["E-Cast"] + rs
            if not self.sub(t[2][1], t[1]):
                raise Stuck(f"{t[2][1]} <: {t[1]} é falso")
            return t[2], ["E-CastNew"]
        raise Stuck("variável livre")

    def run(self, t):
        trace = []
        while not self.is_value(t):
            try:
                t1, rs = self.step(t)
            except Stuck as e:
                return trace, t, str(e)
            trace.append((t1, rs))
            t = t1
        return trace, t, None

    # ------------------------------------------------------------ tipagem (Fig. 19-4)
    def typeof(self, t, env=None):
        """Devolve (tipo, regra). Um stupid cast é reportado como 'T-SCast'."""
        env = env or {}
        k = t[0]
        if k == "var":
            if t[1] not in env:
                raise TypeError_(f"variável {t[1]} fora do ambiente")
            return env[t[1]], "T-Var"
        if k == "field":
            c0, _ = self.typeof(t[1], env)
            for ty, f in self.fields(c0):
                if f == t[2]:
                    return ty, "T-Field"
            raise TypeError_(f"{c0} não tem campo {t[2]}")
        if k == "invk":
            c0, _ = self.typeof(t[1], env)
            mt = self.mtype(t[2], c0)
            if mt is None:
                raise TypeError_(f"{c0} não tem método {t[2]}")
            ds, c = mt
            self._args(t[3], ds, env)
            return c, "T-Invk"
        if k == "new":
            ds = [ty for ty, _ in self.fields(t[1])]
            self._args(t[2], ds, env)
            return t[1], "T-New"
        c = t[1]
        d, _ = self.typeof(t[2], env)
        if self.sub(d, c):
            return c, "T-UCast"
        if self.sub(c, d) and c != d:
            return c, "T-DCast"
        return c, "T-SCast"

    def _args(self, ts, ds, env):
        if len(ts) != len(ds):
            raise TypeError_("número de argumentos errado")
        for a, d in zip(ts, ds):
            ca, _ = self.typeof(a, env)
            if not self.sub(ca, d):
                raise TypeError_(f"{ca} não é subtipo de {d}")

    def check_classes(self):
        """class C extends D {...} OK e M OK in C, incluindo override."""
        for c, (d, fs, ms) in self.ct.items():
            names = [f for _, f in self.fields(c)]
            assert len(names) == len(set(names)), f"campo repetido em {c}"
            for m, (r, ps, body) in ms.items():
                env = {x: ty for ty, x in ps} | {"this": c}
                e0, _ = self.typeof(body, env)
                assert self.sub(e0, r), f"{c}.{m}: corpo {e0} não é subtipo de {r}"
                sup = self.mtype(m, d)
                assert sup is None or sup == ([ty for ty, _ in ps], r), f"override inválido: {c}.{m}"


def subst(t, s):
    k = t[0]
    if k == "var":
        return s.get(t[1], t)
    if k == "field":
        return ("field", subst(t[1], s), t[2])
    if k == "invk":
        return ("invk", subst(t[1], s), t[2], [subst(a, s) for a in t[3]])
    if k == "new":
        return ("new", t[1], [subst(a, s) for a in t[2]])
    return ("cast", t[1], subst(t[2], s))


def norm(s):
    return show(parse(s)).replace(" ", "")


# ---------------------------------------------------------------- verificações dos slides
def expect_trace(fj, term, steps, stuck_at=None):
    """steps: [(termo esperado, [regras de fora para dentro]), ...]"""
    trace, final, err = fj.run(parse(term))
    got = [(show(t).replace(" ", ""), rs) for t, rs in trace]
    want = [(norm(t), rs) for t, rs in steps]
    assert got == want, f"\n{term}\n  obtido:   {got}\n  esperado: {want}"
    if stuck_at is None:
        assert err is None, f"{term} travou: {err}"
    else:
        assert err is not None and show(final).replace(" ", "") == norm(stuck_at), f"{term}: {err}"
    # preservação: cada passo mantém um tipo que é subtipo do anterior
    try:
        ty, _ = fj.typeof(parse(term))
    except TypeError_:
        return
    for t, _ in trace:
        ty1, _ = fj.typeof(t)
        assert fj.sub(ty1, ty), f"preservação falhou em {show(t)}: {ty1} ≮: {ty}"
        ty = ty1
    if err:  # progresso: termo bem tipado só trava em (C)(new D(v)) com D ≮: C
        assert final[0] == "cast" and fj.is_value(final[2]) and not fj.sub(final[2][1], final[1]), \
            f"progresso falhou: {show(final)}"


def expect_type(fj, term, ty, rule, env=None):
    got = fj.typeof(parse(term), env)
    assert got == (ty, rule), f"{term}: obtido {got}, esperado {(ty, rule)}"


def expect_ill_typed(fj, term):
    try:
        fj.typeof(parse(term))
    except TypeError_:
        return
    raise AssertionError(f"{term} deveria ser mal tipado")


def self_check():
    pair, bichos = FJ(PAIR_CT), FJ(ANIMAIS_CT)
    pair.check_classes(); bichos.check_classes()

    # override inválido em FJ: retorno precisa ser idêntico (Java 5+ aceitaria retorno covariante)
    ruim = dict(ANIMAIS_CT, Cachorro=("Mamifero", [("Animal", "amigo")], {"falar": ("Latido", [], "new Latido()")}))
    try:
        FJ(ruim).check_classes()
        raise AssertionError("override covariante deveria ser rejeitado")
    except AssertionError as e:
        assert "override inválido" in str(e)

    # Pessoa 1: subtipagem e consultas
    assert bichos.sub("Cachorro", "Cachorro") and bichos.sub("Cachorro", "Mamifero") and bichos.sub("Cachorro", "Animal")
    assert bichos.sub("Cachorro", "Object") and not bichos.sub("Gato", "Cachorro") and not bichos.sub("Cachorro", "Gato")
    assert not bichos.sub("Animal", "Mamifero")
    assert bichos.fields("Gato") == [] and bichos.fields("Cachorro") == [("Animal", "amigo")]
    assert bichos.mtype("falar", "Mamifero") == ([], "Som")
    assert bichos.mbody("falar", "Mamifero")[1] == parse("new Som()")
    assert bichos.mbody("falar", "Cachorro")[1] == parse("new Latido()")
    path = []
    assert bichos.mbody("apresentar", "Cachorro", path)[1] == parse("this.falar()")
    assert path == ["Cachorro", "Mamifero", "Animal"]
    assert pair.fields("Pair") == [("Object", "fst"), ("Object", "snd")]

    # Pessoa 2: regras de computação com animais
    expect_trace(bichos, "new Cachorro(new Gato()).amigo", [("new Gato()", ["E-ProjNew"])])
    expect_trace(bichos, "new Gato().falar()", [("new Miado()", ["E-InvkNew"])])
    expect_trace(bichos, "(Animal) new Gato()", [("new Gato()", ["E-CastNew"])])
    # chamada por valor: o argumento vira valor antes do E-ProjNew
    expect_trace(bichos, "new Cachorro((Animal) new Gato()).amigo", [
        ("new Cachorro(new Gato()).amigo", ["E-Field", "E-New-Arg", "E-CastNew"]),
        ("new Gato()", ["E-ProjNew"])])
    # exemplo do livro com cast (§19.2)
    expect_trace(pair, "((Pair) new Pair(new Pair(new A(), new B()), new A()).fst).snd", [
        ("((Pair) new Pair(new A(), new B())).snd", ["E-Field", "E-Cast", "E-ProjNew"]),
        ("new Pair(new A(), new B()).snd", ["E-Field", "E-CastNew"]),
        ("new B()", ["E-ProjNew"])])
    expect_ill_typed(pair, "new Pair(new Pair(new A(), new B()), new A()).fst.snd")
    expect_type(pair, "new Pair(new Pair(new A(), new B()), new A()).fst", "Object", "T-Field")
    # setfst por substituição
    expect_trace(pair, "new Pair(new A(), new B()).setfst(new B())", [
        ("new Pair(new B(), new Pair(new A(), new B()).snd)", ["E-InvkNew"]),
        ("new Pair(new B(), new B())", ["E-New-Arg", "E-ProjNew"])])
    # despacho dinâmico e recursão aberta
    expect_trace(bichos, "new Cachorro(new Gato()).apresentar()", [
        ("new Cachorro(new Gato()).falar()", ["E-InvkNew"]),
        ("new Latido()", ["E-InvkNew"])])
    expect_trace(bichos, "new Cachorro(new Gato()).amigo.falar()", [
        ("new Gato().falar()", ["E-Invk-Recv", "E-ProjNew"]),
        ("new Miado()", ["E-InvkNew"])])
    expect_trace(bichos, "new Mamifero().falar()", [("new Som()", ["E-InvkNew"])])
    # casts em execução
    expect_trace(bichos, "(Gato) new Cachorro(new Gato()).amigo", [
        ("(Gato) new Gato()", ["E-Cast", "E-ProjNew"]),
        ("new Gato()", ["E-CastNew"])])
    expect_trace(bichos, "(Cachorro) new Cachorro(new Gato()).amigo", [
        ("(Cachorro) new Gato()", ["E-Cast", "E-ProjNew"])], stuck_at="(Cachorro) new Gato()")
    expect_trace(bichos, "(Cachorro) (Animal) new Gato()", [
        ("(Cachorro) new Gato()", ["E-Cast", "E-CastNew"])], stuck_at="(Cachorro) new Gato()")
    expect_trace(pair, "(A) (Object) new B()", [("(A) new B()", ["E-Cast", "E-CastNew"])], stuck_at="(A) new B()")
    # os três jeitos de travar
    for ct, t in [(bichos, "new Gato().amigo"), (bichos, "new Som().falar()"), (bichos, "(Cachorro) new Gato()"),
                  (pair, "new A().fst"), (pair, "new A().setfst(new B())"), (pair, "(A) new B()")]:
        expect_trace(ct, t, [], stuck_at=t)
    expect_ill_typed(bichos, "new Gato().amigo")
    expect_ill_typed(bichos, "new Som().falar()")

    # Pessoa 3: tipagem
    expect_type(bichos, "new Gato()", "Gato", "T-New")
    expect_type(bichos, "new Cachorro(new Gato())", "Cachorro", "T-New")
    expect_type(bichos, "new Cachorro(new Gato()).amigo", "Animal", "T-Field")
    expect_type(bichos, "new Cachorro(new Gato()).amigo.falar()", "Som", "T-Invk")
    expect_ill_typed(bichos, "new Cachorro(new Gato()).amigo.miar()")
    expect_type(bichos, "((Gato) new Cachorro(new Gato()).amigo).miar()", "Som", "T-Invk")
    expect_trace(bichos, "((Gato) new Cachorro(new Gato()).amigo).miar()", [
        ("((Gato) new Gato()).miar()", ["E-Invk-Recv", "E-Cast", "E-ProjNew"]),
        ("new Gato().miar()", ["E-Invk-Recv", "E-CastNew"]),
        ("new Miado()", ["E-InvkNew"])])
    expect_type(bichos, "this.falar()", "Som", "T-Invk", env={"this": "Animal"})
    expect_type(bichos, "this", "Animal", "T-Var", env={"this": "Animal"})
    expect_type(bichos, "(Animal) new Gato()", "Animal", "T-UCast")
    expect_type(bichos, "(Gato) new Cachorro(new Gato()).amigo", "Gato", "T-DCast")
    expect_type(bichos, "(Cachorro) new Cachorro(new Gato()).amigo", "Cachorro", "T-DCast")
    expect_type(bichos, "(Cachorro) (Animal) new Gato()", "Cachorro", "T-DCast")
    expect_type(bichos, "(Cachorro) new Gato()", "Cachorro", "T-SCast")
    expect_type(bichos, "(Object) new Gato()", "Object", "T-UCast")
    expect_type(pair, "(A) (Object) new B()", "A", "T-DCast")
    expect_type(pair, "(A) new B()", "A", "T-SCast")
    expect_ill_typed(bichos, "new Cachorro(new Som())")

    # exercício do guia 02
    expect_trace(pair, "new Pair(new A(), new B()).setfst(new A()).setfst(new B()).fst", [
        ("new Pair(new A(), new Pair(new A(), new B()).snd).setfst(new B()).fst", ["E-Field", "E-Invk-Recv", "E-InvkNew"]),
        ("new Pair(new A(), new B()).setfst(new B()).fst", ["E-Field", "E-Invk-Recv", "E-New-Arg", "E-ProjNew"]),
        ("new Pair(new B(), new Pair(new A(), new B()).snd).fst", ["E-Field", "E-InvkNew"]),
        ("new Pair(new B(), new B()).fst", ["E-Field", "E-New-Arg", "E-ProjNew"]),
        ("new B()", ["E-ProjNew"])])
    print("todas as verificações passaram")


def main():
    if len(sys.argv) == 1:
        self_check()
        return
    t = parse(sys.argv[1])
    fj = FJ(ANIMAIS_CT if any(c in sys.argv[1] for c in ANIMAIS_CT) else PAIR_CT)
    try:
        ty, rule = fj.typeof(t)
        print(f"   {show(t)}    : {ty}  ({rule})")
    except TypeError_ as e:
        print(f"   {show(t)}    mal tipado: {e}")
    trace, final, err = fj.run(t)
    for t1, rs in trace:
        print(f"⟶ {show(t1)}    [{' > '.join(rs)}]")
    print(f"travado: {err}" if err else "valor final")


if __name__ == "__main__":
    main()
