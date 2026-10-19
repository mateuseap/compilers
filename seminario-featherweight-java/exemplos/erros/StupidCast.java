// Slide 18: cast entre classes nao relacionadas. Java rejeita; FJ so aceita com "stupid warning" (T-SCast).
class StupidCast {
    Object t = (A) new B();
}
