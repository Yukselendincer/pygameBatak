
from rules import Rules

class BotManager:
    @staticmethod
    def bot_oyna(bot_el, yer, koz, ilk_tur):
        def kart_turu(kart): return kart.split()[0]
        def kart_degeri(kart): return kart.split()[1]
        def kart_puan(kart): return Rules.kagit_puan(kart)

        # Strateji 1: Aynı türden varsa oyna
        uygun_kartlar = []
        if yer:
            uygun_kartlar = [k for k in bot_el if kart_turu(k) == ilk_tur]

            if not uygun_kartlar:
                # Strateji 2: Koz at, ama en düşük koz
                kozlar = [k for k in bot_el if kart_turu(k) == koz]
                if kozlar:
                    kozlar.sort(key=kart_puan)  # En düşük puanlı koz önce
                    return kozlar[0]

                # Strateji 3: Elinde ne varsa en düşük puanlıyı at
                bot_el.sort(key=kart_puan)
                return bot_el[0]
            else:
                # Strateji 4: Aynı türde varsa, kazanma ihtimali düşük kartı at
                uygun_kartlar.sort(key=kart_puan)
                return uygun_kartlar[0]
        else:
            # Strateji 5: İlk atan botsa - küçük kartla başla
            bot_el.sort(key=kart_puan)
            return bot_el[0]
