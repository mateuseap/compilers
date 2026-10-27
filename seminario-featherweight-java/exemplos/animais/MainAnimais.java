// Avalia na JVM os termos com animais usados na apresentacao.
// main e println sao Java comum, so para observar o resultado.
public class MainAnimais {
    public static void main(String[] args) {
        // E-ProjNew: o campo amigo devolve o argumento do construtor
        Object t1 = new Cachorro(new Gato()).amigo;
        System.out.println("campo           -> " + t1);

        // Chamada por valor: o argumento (cast) vira valor antes do .amigo
        Object t2 = new Cachorro((Animal) new Gato()).amigo;
        System.out.println("cbv             -> " + t2);

        // Tipo estatico Animal, classe real Gato: E-InvkNew usa mbody(falar, Gato)
        Object t3 = new Cachorro(new Gato()).amigo.falar();
        System.out.println("amigo.falar()   -> " + t3);

        // Despacho dinamico + recursao aberta: corpo escrito em Animal, this e um Cachorro
        Object t4 = new Cachorro(new Gato()).apresentar();
        System.out.println("apresentar()    -> " + t4);

        // Metodo herdado sem sobrescrita: mbody(falar, Mamifero) sobe para Animal
        Object t5 = new Mamifero().falar();
        System.out.println("mamifero.falar  -> " + t5);

        // Upcast: sempre passa
        Object t6 = (Animal) new Gato();
        System.out.println("upcast          -> " + t6);

        // Downcast que passa: a classe real e Gato
        Object t7 = (Gato) new Cachorro(new Gato()).amigo;
        System.out.println("downcast ok     -> " + t7);

        // Downcast que falha: em FJ trava; em Java vira ClassCastException
        try {
            Object t8 = (Cachorro) new Cachorro(new Gato()).amigo;
            System.out.println("nunca chega aqui " + t8);
        } catch (ClassCastException e) {
            System.out.println("downcast ruim   -> ClassCastException (em FJ: travado em (Cachorro) new Gato())");
        }
    }
}
