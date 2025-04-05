from deck import kagit_dagit
from rules import Rules
from score import ScoreManager

class GameController:
    def __init__(self, koz="maça"):
        self.koz = koz
        self.eller = kagit_dagit()
        self.yer = []
        self.sira = 0
        self.ilk_tur = ""
        self.score_manager = ScoreManager()
        self.oyuncu_adlari = {
            0: "Yüksel",
            1: "Bot 1",
            2: "Bot 2",
            3: "Bot 3"
        }

        for i, el in enumerate(self.eller):
            print(f"Oyuncu-{i+1}'in eli: {el}")

    def kart_at(self, oyuncu, kart):
        if len(self.yer) >= 4:
            raise RuntimeError("Bu turda zaten 4 kart oynandı.")
        print(f"Kart atılıyor: Oyuncu-{oyuncu}, Kart-{kart}")
        if kart in self.eller[oyuncu]:
            self.eller[oyuncu].remove(kart)
            kart_puan = Rules.kagit_puan(kart)
            self.yer.append((kart, oyuncu, kart_puan))
        else:
            raise ValueError(f"Kart bulunamadı: {kart}, Oyuncunun eli: {self.eller[oyuncu]}")

    def eli_tamamla(self):
        oyuncu = Rules.yer_kime_kaldi(self.yer, self.koz, self.ilk_tur)
        print(f"El kazananı: {self.oyuncu_adlari[oyuncu]}")
        self.score_manager.el_kazanan(oyuncu)
        return oyuncu  # MASA artık burada temizlenmiyor

    def masa_temizle(self):
        self.yer.clear()
        self.ilk_tur = ""
