// Classe da hierarquia usada nos exemplos intuitivos do seminario.
// Segue o subconjunto Featherweight Java do capitulo 19. toString NAO faz parte de FJ.

class Cachorro extends Mamifero {
    Animal amigo;
    Cachorro(Animal amigo) { super(); this.amigo = amigo; }
    Som falar() { return new Latido(); }
    public String toString() { return "new Cachorro(" + amigo + ")"; }
}
