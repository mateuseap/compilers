// Travamento 1: Gato nao tem campo amigo (fields(Gato) = vazio). T-Field rejeita.
class CampoInexistente {
    Object t = new Gato().amigo;
}
