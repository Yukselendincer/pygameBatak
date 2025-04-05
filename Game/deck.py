import random

turler = ["maça", "kupa", "sinek", "karo"]
kagitlar = ["AS", "2", "3", "4", "5", "6", "7", "8", "9", "10", "VALE", "KIZ", "PAPAZ"]

def deste_olustur():
    """ Tam bir iskambil destesini oluşturur. """
    return [f"{tur} {kagit}" for kagit in kagitlar for tur in turler]

def kagit_dagit(oyuncu_sayisi=4):
    """ Kart destesini karıştırıp belirtilen oyuncu sayısına eşit dağıtır. """
    deste = deste_olustur()
    random.shuffle(deste)
    oyuncu_basina_kart = len(deste) // oyuncu_sayisi
    oyuncu_elleri = [deste[i * oyuncu_basina_kart : (i + 1) * oyuncu_basina_kart] for i in range(oyuncu_sayisi)]
    return oyuncu_elleri

# Test amaçlı:
if __name__ == "__main__":
    eller = kagit_dagit()
    for i, el in enumerate(eller):
        print(f"Oyuncu {i+1}: {el}")
