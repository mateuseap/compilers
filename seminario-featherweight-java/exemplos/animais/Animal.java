// Classe da hierarquia usada nos exemplos intuitivos do seminario.
// Segue o subconjunto Featherweight Java do capitulo 19. toString NAO faz parte de FJ.

class Animal extends Object {
    Animal() { super(); }
    Som falar() { return new Som(); }
    Som apresentar() { return this.falar(); }
    public String toString() { return "new Animal()"; }
}
