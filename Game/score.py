# score.py

class ScoreManager:
    def __init__(self, oyuncu_sayisi=4):
        self.skorlar = {i: 0 for i in range(oyuncu_sayisi)}
        self.el_gecmisleri = []  # Her elin kime gittiğini tutar

    def el_kazanan(self, oyuncu_id):
        """Bir oyuncunun el kazandığını kaydeder"""
        self.el_gecmisleri.append(oyuncu_id)
        self.skorlar[oyuncu_id] += 1

    def skor_getir(self, oyuncu_id):
        """Belirli oyuncunun skorunu döndürür"""
        return self.skorlar.get(oyuncu_id, 0)

    def skor_tablosu(self):
        """Tüm oyuncuların skorlarını döndürür"""
        return self.skorlar.copy()

    def resetle(self):
        """Skorları sıfırlar"""
        for k in self.skorlar:
            self.skorlar[k] = 0
        self.el_gecmisleri.clear()
