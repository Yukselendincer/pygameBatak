kagit_puanlari = {
    "AS":30, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,
    "9":9, "10":10, "VALE":15, "KIZ":20, "PAPAZ":25
}

class Rules:
    @staticmethod
    def kagit_puan(kagit):
        return kagit_puanlari[kagit.split()[1]]

    @staticmethod
    def elde_tur_varmi(el, tur):
        return any(k.startswith(tur) for k in el)

    @staticmethod
    def elde_buyuk_kagit_varmi(el, tur, puan):
        for k in el:
            t, isim = k.split()
            if t == tur and kagit_puanlari[isim] > puan:
                return True
        return False

    @staticmethod
    def elin_en_buyugu(el, tur):
        uygunlar = [k for k in el if k.startswith(tur)]
        return max(uygunlar, key=lambda k: kagit_puanlari[k.split()[1]]) if uygunlar else None

    @staticmethod
    def yer_kime_kaldi(yer, koz, ilk_tur):
        kozlar = [k for k in yer if k[0].startswith(koz)]
        hedef_kagitlar = kozlar if kozlar else [k for k in yer if k[0].startswith(ilk_tur)]
        en_buyuk = max(hedef_kagitlar, key=lambda k: k[2])  # <-- burada düzeltme yapıldı
        return en_buyuk[1]  # oyuncu index'i (en_buyuk[1]'de oyuncu var)

