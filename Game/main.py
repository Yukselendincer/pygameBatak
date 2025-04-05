import pygame
from game_controller import GameController
from screens import GameScreen
from botmanage import BotManager
import time

def skor_goster(screen, skorlar: dict, oyuncu_adlari: dict, el_sayisi: int):
    font = pygame.font.SysFont(None, 28)
    x, y = 1150, 50
    title = font.render("Skorlar", True, (255, 255, 0))
    screen.blit(title, (x, y))
    y += 30

    for oyuncu_id, skor in skorlar.items():
        isim = oyuncu_adlari.get(oyuncu_id, f"Oyuncu {oyuncu_id}")
        text = font.render(f"{isim}: {skor}", True, (255, 255, 255))
        screen.blit(text, (x, y))
        y += 25

    el_text = font.render(f"El: {el_sayisi}", True, (255, 255, 255))
    screen.blit(el_text, (x, y + 10))

pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Batak Oyunu")

controller = GameController()
game_screen = GameScreen(screen)

running = True
aktif_oyuncu = 0
player_card_rects = []
el_sayisi = 0
el_bekle = False
bekleyen_kazanan = None
el_bekleme_baslangic = None
sure_beklendi = False
kurallar_goster = False
kurallar_kapat_rect = None
btn_rect = None
clock = pygame.time.Clock()

while running:
    screen.fill((0, 100, 0))
    kurallar_btn = game_screen.render_kurallar_button()
    if el_bekle and sure_beklendi:
        btn_rect = game_screen.render_continue_button()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if kurallar_goster and kurallar_kapat_rect and kurallar_kapat_rect.collidepoint(mouse_pos):
                kurallar_goster = False
                continue

            if kurallar_btn.collidepoint(mouse_pos):
                kurallar_goster = True
                continue

            if el_bekle and sure_beklendi and btn_rect and btn_rect.collidepoint(mouse_pos):
                controller.masa_temizle()
                aktif_oyuncu = bekleyen_kazanan
                el_bekle = False
                bekleyen_kazanan = None
                el_bekleme_baslangic = None
                sure_beklendi = False
                continue

            if not el_bekle and aktif_oyuncu == 0:
                for rect, kart in player_card_rects:
                    if rect.collidepoint(mouse_pos):
                        print(f"🖱️ Tıklanan kart: {kart}")
                        print(f"🎴 Oyuncunun elindeki kartlar: {controller.eller[0]}")
                        try:
                            controller.kart_at(0, kart)
                            controller.ilk_tur = kart.split()[0] if not controller.yer else controller.ilk_tur
                            aktif_oyuncu = 1
                        except ValueError as e:
                            print(f"❌ Hata: {e}")
                        break

    if all(len(el) == 0 for el in controller.eller):
        print("🏁 Oyun bitti, kartlar tükendi.")
        running = False
        continue

    game_screen.render_enemy_hand(1, len(controller.eller[1]))
    game_screen.render_enemy_hand(2, len(controller.eller[2]))
    game_screen.render_enemy_hand(3, len(controller.eller[3]))

    if aktif_oyuncu == 0:
        player_card_rects = game_screen.render_hand_images(controller.eller[0], kart_boyutu=(60, 90))

    game_screen.render_played_cards(controller.yer, kart_boyutu=(60, 90))

    if not el_bekle and aktif_oyuncu != 0 and controller.eller[aktif_oyuncu]:
        pygame.time.wait(400)
        kart = BotManager.bot_oyna(controller.eller[aktif_oyuncu], controller.yer, controller.koz, controller.ilk_tur)
        print(f"🤖 Bot-{aktif_oyuncu} oynuyor: {kart}")
        try:
            controller.kart_at(aktif_oyuncu, kart)
            aktif_oyuncu = (aktif_oyuncu + 1) % 4
        except RuntimeError as e:
            print(f"⚠️ Bot hatası: {e}")
            continue

    if len(controller.yer) == 4 and not el_bekle:
        bekleyen_kazanan = controller.eli_tamamla()
        el_sayisi += 1
        el_bekle = True
        el_bekleme_baslangic = time.time()
        sure_beklendi = False

    if el_bekle and not sure_beklendi:
        game_screen.goster_el_kazanan(controller.oyuncu_adlari[bekleyen_kazanan])
        if time.time() - el_bekleme_baslangic >= 3:
            sure_beklendi = True

    if kurallar_goster:
        kurallar_kapat_rect = game_screen.kurallari_goster()

    skor_goster(screen, controller.score_manager.skor_tablosu(), controller.oyuncu_adlari, el_sayisi)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
