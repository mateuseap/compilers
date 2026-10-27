// Avalia na JVM os termos Animal/Cachorro usados na apresentacao.
// main e println sao Java comum, apenas para observar resultados.
public class MainAnimais {
    public static void main(String[] args) {
        Object t1 = new Cachorro().falar();
        System.out.println("cachorro.falar -> " + t1);

        Object t2 = new Cachorro().apresentar();
        System.out.println("apresentar     -> " + t2);

        Object t3 = new Mamifero().falar();
        System.out.println("mamifero.falar -> " + t3);

        Object t4 = (Animal) new Cachorro();
        System.out.println("upcast         -> " + t4);

        try {
            Object t5 = (Gato) (Animal) new Cachorro();
            System.out.println("nunca chega aqui " + t5);
        } catch (ClassCastException e) {
            System.out.println("downcast ruim  -> ClassCastException (em FJ: stuck)");
        }
    }
}
