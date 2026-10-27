// Stupid cast: Gato e Cachorro nao sao relacionados por <:.
// Java rejeita; FJ so aceita com "stupid warning" (T-SCast).
class CastEntreIrmaos {
    Object t = (Cachorro) new Gato();
}
