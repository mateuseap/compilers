// Classe da hierarquia usada nos exemplos intuitivos do seminario.
// Segue Featherweight Java; toString serve apenas para observar o resultado na JVM.
class Cachorro extends Mamifero {
    Cachorro() { super(); }
    Som falar() { return new Latido(); }
    public String toString() { return "new Cachorro()"; }
}
