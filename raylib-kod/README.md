# Raylib Kod Örnekleri

Bu klasördeki C dosyaları, "Bilgisayar Grafikleri - Sıfırdan" eğitim serisinin **Işın İzleme** bölümüne eşlik eden pratik örneklerdir.

## Gereksinimler

- **C derleyici** (gcc, clang)
- **raylib** kütüphanesi

### raylib Kurulumu

```bash
# macOS
brew install raylib

# Ubuntu/Debian
sudo apt install libraylib-dev

# Kaynak koddan derleme
git clone https://github.com/raysan5/raylib.git
cd raylib/src && make PLATFORM=PLATFORM_DESKTOP && sudo make install
```

## Derleme ve Çalıştırma

```bash
# Tüm örnekleri derle
make all

# Tek bir örneği derle ve çalıştır
make ornek01
./ornek01

make ornek04
./ornek04
```

## Örnekler

| Dosya | Açıklama | İlgili Bölüm |
|-------|----------|---------------|
| `ornek01_temel_pencere.c` | Temel raylib penceresi, piksel çizimi | 2.1 - Giriş |
| `ornek02_kure_cizimi.c` | 3D küreler sahnesi, kamera kontrolü | 2.2 - Varsayımlar |
| `ornek03_viewport_ve_isinlar.c` | Viewport ve ışın görselleştirme | 2.3 - Işınlar |
| `ornek04_basit_raytracer.c` | Tam yazılımsal ışın izleyici | 2.5 - İlk Küreler |
