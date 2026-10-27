// Classe da hierarquia usada nos exemplos intuitivos do seminario.
// Segue o subconjunto Featherweight Java do capitulo 19. toString NAO faz parte de FJ.

class Mamifero extends Animal {
    Mamifero() { super(); }
    public String toString() { return "new Mamifero()"; }
}
