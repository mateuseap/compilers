// Executa os termos usados nos slides com a JVM real.
// Os termos em si sao FJ; main, toString e println sao Java normal, so para observar.
public class Main {
    public static void main(String[] args) {
        // Secao 19.2: chamada de metodo (E-InvkNew)
        Object t1 = new Pair(new A(), new B()).setfst(new B());
        System.out.println("setfst      -> " + t1);

        // Secao 19.2: acesso a campo com downcast (E-ProjNew, E-CastNew)
        Object t2 = ((Pair) new Pair(new Pair(new A(), new B()), new A()).fst).snd;
        System.out.println("cast + snd  -> " + t2);

        // Upcast: sempre seguro
        Object t3 = (Object) new A();
        System.out.println("upcast      -> " + t3);

        // Cast que falha: em FJ a computacao trava; em Java vira ClassCastException
        try {
            Object t4 = (A) (Object) new B();
            System.out.println("nunca chega aqui " + t4);
        } catch (ClassCastException e) {
            System.out.println("(A)(Object)new B() -> ClassCastException (em FJ: travado)");
        }
    }
}
