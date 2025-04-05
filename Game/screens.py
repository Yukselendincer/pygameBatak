import pygame
import os

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.kart_gorselleri = self.kartlari_yukle()
        self.last_logged = None  # 🔁 Masadaki kartlar tekrar yazdırılmasın

    def kart_adi_donustur(self, kart):
        tur_cevir = {
            "maça": "clubs",
            "kupa": "hearts",
            "sinek": "spades",
            "karo": "diamonds"
        }
        deger_cevir = {
            "AS": "A",
            "VALE": "J",
            "KIZ": "Q",
            "PAPAZ": "K"
        }

        try:
            kart = kart.strip()
            parcalar = kart.split()
            if len(parcalar) != 2:
                print(f"❌ Hatalı kart formatı: '{kart}'")
                return "back"
            tur, deger = parcalar
        except Exception as e:
            print(f"❌ Kart ayrıştırılamadı: '{kart}' | Hata: {e}")
            return "back"

        tur_ing = tur_cevir.get(tur.lower(), "spades")
        deger_ing = deger_cevir.get(deger.upper(), deger.lower())

        return f"{deger_ing}_of_{tur_ing}"


    def kartlari_yukle(self):
        klasor = "assets/image"
        kartlar = {}
        for dosya in os.listdir(klasor):
            if dosya.endswith(".png"):
                isim = dosya.replace(".png", "")
                yol = os.path.join(klasor, dosya)
                kartlar[isim] = pygame.image.load(yol)
        return kartlar

    def render_enemy_hand(self, oyuncu_no, kart_sayisi, kart_boyutu=(60, 90)):
        img = self.kart_gorselleri.get("back")
        if not img:
            print("⚠️ 'back.png' kart arkası görüntüsü eksik!")
            return

        img = pygame.transform.scale(img, kart_boyutu)
        ekran_w, ekran_h = self.screen.get_size()

        if oyuncu_no == 1:  # ÜST
            x_start = ekran_w // 2 - (kart_sayisi * 15) // 2
            y = 80
            for i in range(kart_sayisi):
                rect = img.get_rect(topleft=(x_start + i * 15, y))
                self.screen.blit(img, rect)

        elif oyuncu_no == 2:  # SAĞ
            x = ekran_w - kart_boyutu[0] - 30
            y_start = ekran_h // 2 - (kart_sayisi * 15) // 2
            for i in range(kart_sayisi):
                rect = img.get_rect(topleft=(x, y_start + i * 15))
                self.screen.blit(img, rect)

        elif oyuncu_no == 3:  # SOL
            x = 30
            y_start = ekran_h // 2 - (kart_sayisi * 15) // 2
            for i in range(kart_sayisi):
                rect = img.get_rect(topleft=(x, y_start + i * 15))
                self.screen.blit(img, rect)

    def render_hand_images(self, hand, kart_boyutu=(80, 120), secili_index=None):
        tur_sirasi = ["maça", "kupa", "karo", "sinek"]
        deger_sirasi = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "VALE", "KIZ", "PAPAZ", "AS"]

        grouped_cards = {tur: [] for tur in tur_sirasi}
        for kart in hand:
            tur, deger = kart.split()
            grouped_cards[tur].append((deger_sirasi.index(deger), kart))

        for tur in grouped_cards:
            grouped_cards[tur].sort()

        x_start = 50
        y = 600
        card_rects = []

        font = pygame.font.SysFont(None, 24)
        kart_index = 0

        for tur in tur_sirasi:
            x = x_start
            for _, kart in grouped_cards[tur]:
                img_key = self.kart_adi_donustur(kart)
                img = self.kart_gorselleri.get(img_key)
                if img:
                    img = pygame.transform.scale(img, kart_boyutu)
                    rect = img.get_rect(topleft=(x, y))
                    self.screen.blit(img, rect)

                    if secili_index is not None and kart_index == secili_index:
                        pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)

                    text_surface = font.render(f"{kart_index+1}. Kart", True, (255, 255, 0))
                    text_rect = text_surface.get_rect(center=(rect.centerx, rect.bottom + 12))
                    self.screen.blit(text_surface, text_rect)

                    card_rects.append((rect, kart))
                    x += kart_boyutu[0] + 10
                    kart_index += 1

            x_start += (kart_boyutu[0] + 10) * 4

        return card_rects

    def render_played_cards(self, played_cards, kart_boyutu=(60, 90)):
        """
        Masadaki 4 kartı oyunculara göre sabit pozisyonlarda gösterir:
        - Oyuncu 0: Alt (sen)
        - Oyuncu 1: Üst
        - Oyuncu 2: Sağ
        - Oyuncu 3: Sol
        """
        ekran_w, ekran_h = self.screen.get_size()

        # Sabit masa pozisyonları
        positions = {
            0: (ekran_w // 2 - kart_boyutu[0] // 2, ekran_h // 2 + 100),  # ALT
            1: (ekran_w // 2 - kart_boyutu[0] // 2, ekran_h // 2 - kart_boyutu[1] - 100),  # ÜST
            2: (ekran_w // 2 + 150, ekran_h // 2 - kart_boyutu[1] // 2),  # SAĞ
            3: (ekran_w // 2 - 150 - kart_boyutu[0], ekran_h // 2 - kart_boyutu[1] // 2),  # SOL
        }

        if played_cards != self.last_logged:
            print(f"🎴 Masadaki kartlar: {played_cards}")
            self.last_logged = played_cards

        for kart, oyuncu, puan in played_cards:
            img_key = self.kart_adi_donustur(kart)
            img = self.kart_gorselleri.get(img_key)
            if not img:
                print(f"⚠️ Görsel bulunamadı: {img_key}")
                continue
            img = pygame.transform.scale(img, kart_boyutu)
            pos = positions.get(oyuncu, (750, 300))
            rect = img.get_rect(topleft=pos)
            self.screen.blit(img, rect)

    def goster_el_kazanan(self, oyuncu_adi):
        font = pygame.font.SysFont(None, 48)
        text = font.render(f"🃏 El Kazananı: {oyuncu_adi}", True, (255, 255, 0))
        rect = text.get_rect(center=(750, 400))
        self.screen.blit(text, rect)

    def render_restart_button(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render("Yeniden Başlat", True, (255, 255, 255))
        rect = text.get_rect(center=(1350, 750))
        pygame.draw.rect(self.screen, (0, 0, 0), rect.inflate(20, 10))
        self.screen.blit(text, rect)
        return rect

    def render_continue_button(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render("Devam Et", True, (255, 255, 255))
        rect = text.get_rect(topleft=(30, 750))
        pygame.draw.rect(self.screen, (0, 0, 0), rect.inflate(20, 10))
        self.screen.blit(text, rect)
        return rect
    
    def kurallari_goster(self):
        kurallar = [
            "Batak (Koz Maça) Kuralları:",
            "- Her oyuncuya 13 kart dağıtılır.",
            "- Oyunda her zaman 'maça' kozdur.",
            "- Koz, yerdeki kartları geçer.",
            "- Oyuncular ellerindeki kartları sırayla oynar.",
            "- Aynı türden kart varsa atmak zorunlu.",
            "- Tur sonunda en yüksek kartı atan eli alır.",
            "- Koz yoksa farklı türden kart atılabilir.",
            "- Her elin sonunda puan toplanır.",
            "- Oyun, tüm kartlar bitince sona erer.",
        ]
        font = pygame.font.SysFont(None, 28)
        ekran_w, ekran_h = self.screen.get_size()
        popup_rect = pygame.Rect(300, 150, 900, 500)

        # Arkaplan ve çerçeve
        pygame.draw.rect(self.screen, (30, 30, 30), popup_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 3)

        # Başlık
        title_font = pygame.font.SysFont(None, 36)
        title_text = title_font.render("🃏 Batak Kuralları", True, (255, 255, 0))
        self.screen.blit(title_text, (popup_rect.x + 20, popup_rect.y + 20))

        # Kurallar metni
        for i, kural in enumerate(kurallar):
            line = font.render(kural, True, (255, 255, 255))
            self.screen.blit(line, (popup_rect.x + 20, popup_rect.y + 60 + i * 30))

        # Kapat butonu
        button_font = pygame.font.SysFont(None, 28)
        button_text = button_font.render("Kapat", True, (0, 0, 0))
        button_rect = button_text.get_rect(center=(popup_rect.centerx, popup_rect.bottom - 40))
        pygame.draw.rect(self.screen, (255, 255, 0), button_rect.inflate(20, 10))
        self.screen.blit(button_text, button_rect)

        return button_rect


    def render_kurallar_button(self):
        font = pygame.font.SysFont(None, 30)
        text = font.render("Kurallar", True, (255, 255, 255))
        rect = text.get_rect(center=(90, 30))
        pygame.draw.rect(self.screen, (0, 0, 128), rect.inflate(20, 10))
        self.screen.blit(text, rect)
        return rect

    


