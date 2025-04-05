import os
import pygame

pygame.init()

def kart_gorsellerini_kontrol_et(klasor="assets/image"):
    eksikler = []
    yuklenenler = []

    if not os.path.exists(klasor):
        print(f"❌ Klasör bulunamadı: {klasor}")
        return

    for dosya in os.listdir(klasor):
        if dosya.endswith(".png"):
            yol = os.path.join(klasor, dosya)
            try:
                img = pygame.image.load(yol)
                yuklenenler.append(dosya)
            except pygame.error as e:
                print(f"❌ Hatalı dosya: {dosya} -> {e}")
                eksikler.append(dosya)

    print(f"\n✅ Yüklenen görseller ({len(yuklenenler)}):")
    for dosya in sorted(yuklenenler):
        print(f"  - {dosya}")

    if eksikler:
        print(f"\n🚫 Hatalı veya bozuk görseller ({len(eksikler)}):")
        for dosya in eksikler:
            print(f"  - {dosya}")
    else:
        print("\n🎉 Tüm kart görselleri başarıyla yüklendi!")

kart_gorsellerini_kontrol_et()
