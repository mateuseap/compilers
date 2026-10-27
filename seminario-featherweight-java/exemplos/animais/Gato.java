// Classe da hierarquia usada nos exemplos intuitivos do seminario.
// Segue o subconjunto Featherweight Java do capitulo 19. toString NAO faz parte de FJ.

class Gato extends Mamifero {
    Gato() { super(); }
    Som falar() { return new Miado(); }
    Som miar() { return new Miado(); }
    public String toString() { return "new Gato()"; }
}
