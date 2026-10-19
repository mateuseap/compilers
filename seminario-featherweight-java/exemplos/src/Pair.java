// Exemplo da secao 19.2 do TAPL: tudo aqui e Featherweight Java valido.
class Pair extends Object {
    Object fst;
    Object snd;

    // Construtor: um parametro por campo, super() e depois this.f = f.
    Pair(Object fst, Object snd) {
        super(); this.fst = fst; this.snd = snd;
    }

    // Metodo: o corpo e sempre um unico return.
    Pair setfst(Object newfst) {
        return new Pair(newfst, this.snd);
    }

    // Nao faz parte de FJ: so serve para imprimir o resultado ao rodar.
    public String toString() { return "new Pair(" + fst + ", " + snd + ")"; }
}
