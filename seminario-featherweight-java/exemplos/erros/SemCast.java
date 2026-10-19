// Slide 14: sem o cast, o termo nao tipa. fst tem tipo estatico Object, que nao tem campo snd.
// Compile junto com src/ e veja o erro: (a partir de exemplos/) javac -d /tmp/out src/A.java src/B.java src/Pair.java erros/SemCast.java
class SemCast {
    Object t = new Pair(new Pair(new A(), new B()), new A()).fst.snd;
}
