"""
Bölüm prompt tanımları.
Her bölüm için OpenAI'a gönderilecek promptları içerir.
"""

SYSTEM_PROMPT = """Sen bilgisayar grafikleri alaninda uzman bir Turkce egitmensin. Gorevin, isin izleme (ray tracing) kavramlarini Turkce olarak aciklamaktir.

HEDEF KITLE: Raylib ve C dilini ilk kez goren, matematik bilgisi sinirli yazilimcilar. Her kavram SIFIRDAN aciklanmali. Okuyucu "bu kod ne yapiyor?" diye sormamali - sen zaten her satiri acikla.

KURALLAR:
1. Tum icerik Turkce olmalidir. Teknik terimlerin Ingilizce karsiligini parantez icinde ver.
2. HTML formati kullan:
   - Basliklar: h2, h3, h4 (h1 kullanma, sablon ekliyor)
   - Paragraflar: p etiketi
   - Listeler: ul/ol + li
   - Kalin: strong, italik: em
3. Matematik formulleri icin LaTeX (MathJax):
   - Satir ici: \\( ... \\)
   - Blok formul: \\[ ... \\]
4. Kod bloklari: <pre><code class="language-c">...</code></pre>
   - Kodda < ve > isaretlerini &lt; ve &gt; olarak yaz
   - Kodda & isaretini &amp; olarak yaz
5. Ozel bilgi kutulari:
   - Matematik: <div class="math-box"><div class="box-title">📐 Matematik Notu: BASLIK</div>ICERIK</div>
   - Bilgi: <div class="info-box"><div class="box-title">ℹ️ Bilgi: BASLIK</div>ICERIK</div>
   - Raylib: <div class="raylib-box"><div class="box-title">🎮 Raylib: BASLIK</div>ICERIK</div>
   - Deneyin: <div class="try-box"><div class="box-title">🧪 Deneyin: BASLIK</div>ICERIK</div>
6. Gorseller: <div class="figure"><img src="../../images/raytracing/DOSYA" alt="ACK"><div class="caption">Sekil X: ACK</div></div>
7. Samimi ama profesyonel. Tutarli "siz" kullan.
8. Uzun, kapsamli, detayli icerik uret. Kisaltma yapma.
9. SADECE HTML icerik uret. DOCTYPE/head/body etiketi EKLEME. Direkt h2 ile basla.
10. Tum aciklamalari KENDI ORIJINAL KELIMELERIN ile yaz. Baska kaynaktan kopyalama.

KOD ACIKLAMA KURALLARI (COK ONEMLI):
11. Raylib/C kodu gosterdiginde, kodu ONCE butun olarak goster, SONRA onemli satirlari tek tek acikla.
12. Her onemli fonksiyon/satir icin "Bu satir ne yapiyor?" seklinde kisa baslikli aciklama yap.
13. C dilini bilmeyen biri icin yaz: typedef, struct, float, return, for dongusu, pointer gibi temel kavramlari ilk geciste kisa acikla.
14. Her kod orneginden sonra EN AZ BIR "Deneyin" kutusu ekle. Ornekler:
    - "Kodda kure yaricapini 1.0f yerine 2.0f yapin ve ne oldugunu goruntuleyin."
    - "camera.fovy degerini 30 ve 90 arasinda degistirip bakis acisinin nasil degistigini gozlemleyin."
    - "Kirmizi kurenin merkezini (0, -1, 3) yerine (0, 0, 3) yapin - kure nereye kaydi?"
    - "Isik yogunlugunu 0.6 yerine 1.5 yapin - neler oluyor? Neden?"
    Bu "Deneyin" kutulari okuyucunun teoriyi ELLEYEREK ogrenmesini saglar. Her kutu, degistirilecek SPESIFIK degeri, dosya adini ve beklenen sonucu icersin.
15. Kodlarda her yapinin AMACINI anlat. "Vec3 yapisi nedir? Neden struct kullniyoruz? float nedir?" gibi temel sorulari cevapla."""


def get_chapters(raylib_code_html):
    """
    Bölüm tanımlarını döndürür.
    raylib_code_html: dict, dosya adı -> HTML-safe kod bloğu
    """
    return [
        # ── BÖLÜM 1: GİRİŞ ──
        {
            "filename": "01-giris.html",
            "title": "Işın İzlemeye Giriş",
            "prev": None,
            "next": ("02-temel-varsayimlar.html", "Temel Varsayımlar ve Viewport"),
            "prompt": f"""Isin izleme (ray tracing) kavramina giris yapan kapsamli bir Turkce egitim sayfasi olustur.

KAPSAMLI OLARAK SU KONULARI ISLE:

1. ISIN IZLEME NEDIR?
Bilgisayar grafiklerinde bir goruntu olusturma (rendering) yontemini anlat. Sunu hayal edelim: guzel bir manzaranin resmini yapmak istiyoruz ama resim yetenegimiz yok. Bunun yerine sistematik bir yontem kullanalim: sabit bir bakis noktasi secelim, onumuze izgarali (kareli) bir cerceve koyalim, her karedeki bakin rengi belirleyip tuvale boyayalim. Iste bilgisayarda isin izleme tam olarak budur. Bu analojiyi DETAYLI anlat.

Asagidaki gorselleri uygun yerlerde kullan:
<div class="figure"><img src="../../images/raytracing/figure-2-1.jpg" alt="Manzara"><div class="caption">Sekil 2-1: Resmetmek istedigimiz guzel bir manzara</div></div>
<div class="figure"><img src="../../images/raytracing/figure-2-2.png" alt="Cerceveden resim"><div class="caption">Sekil 2-2: Izgarali cerceveden bakarak sistematik sekilde resim yapma</div></div>

2. ALGORITMA OLARAK IFADE
Bu sureci 4 adimlik bir algoritma olarak yaz (pseudocode seklinde):
- Goz noktasini ve cercveyi (viewport) yerlestir
- Her piksel icin viewport'taki kareyi bul
- O kareden gorunen rengi belirle
- Pikseli boya
Bu 4 adimin aslinda tum isin izleme algoritmasinin ozeti oldugunu vurgula.

3. TERS YONDE ISIN IZLEME
Gercekte isik kaynaktan cikar, nesnelerden seker, gozumuze ulasir. Ama bunu simule etmek cok pahalidir (milyarlarca foton, cok azi gozumuze ulasir). Bu yuzden "tersten" dusunuyoruz: kameradan (gozden) isinlar gonderiyoruz, carptigi nesnenin rengini aliyoruz. Bu kavramI iyice acikla.

4. EKSTRA BILGILER (info-box kullanarak):
- Piksel (picture element) nedir?
- Rendering (goruntu olusturma) ne demek?
- Isin izlemenin kisa tarihcesi (1968 Appel, 1980 Whitted recursive ray tracing)

5. RAYLIB ILE ILK ADIM (raylib-box kullanarak):
Raylib nedir kisa tanitim yap (basit C tabanli grafik kutuphanesi). Asagidaki kodu goster ve her fonksiyonu tek tek acikla:
- InitWindow: pencere olusturma
- SetTargetFPS: kare hizi
- WindowShouldClose: pencere kapatma kontrolu
- BeginDrawing/EndDrawing: cizim dongusunun baslangic/bitis
- ClearBackground: arka plan temizleme
- DrawPixel: TEK PIKSEL cizme (isin izleme ile baglanti kur!)
- CloseWindow: pencere kapatma

{raylib_code_html.get('ornek01_temel_pencere.c', '')}

DrawPixel fonksiyonunun isin izleme ile bagini vurgula: "Isin izleyici de tam olarak bunu yapar - her piksel icin bir renk hesaplar ve o pikseli boyar."

EN AZ 1500 kelime icerik uret. Cok detayli ol."""
        },

        # ── BÖLÜM 2: TEMEL VARSAYIMLAR ──
        {
            "filename": "02-temel-varsayimlar.html",
            "title": "Temel Varsayımlar ve Viewport",
            "prev": ("01-giris.html", "Işın İzlemeye Giriş"),
            "next": ("03-isinlari-izleme.html", "Işınları İzlemek"),
            "prompt": f"""Isin izlemede kamera, viewport ve canvas kavramlarini anlatan kapsamli Turkce egitim sayfasi olustur.

KAPSAMLI OLARAK SU KONULARI ISLE:

1. KAMERA KONUMU VE YONELIMI
Basitlik icin sabit varsayimlar yapiyoruz (ileride kaldiririz):
- Kamera orijinde: O = (0, 0, 0)
- +Z ileri, +Y yukari, +X saga bakiyor
Bu varsayimlari acikla ve neden basitlik icin yaptigimizi belirt.

2. KOORDINAT SISTEMI (math-box icinde DETAYLI):
- 2B ve 3B koordinat sistemi nedir?
- x, y, z eksenleri neyi temsil eder?
- Orijin nedir? Neden (0,0,0)?
- Bir noktayi (x,y,z) olarak ifade etme ornekleri ver
- Sag el kurali nedir?

3. VIEWPORT (GORUNTULEME ALANI)
- Viewport = kameranin onundeki dikdortgen cerceve
- Boyutlari Vw (genislik) ve Vh (yukseklik)
- Kameradan d mesafede, Z eksenine dik
- Basitlik icin Vw = Vh = d = 1 aliyoruz
- Bu yaklasik 53 derecelik FOV (gorus acisi) verir

4. GORUS ACISI (FOV) ACIKLAMASI (info-box):
- FOV nedir? Neden onemli?
- Insan gozu ~180 derece yatay FOV
- Viewport ve kamera mesafesi FOV'u nasil etkiler?

5. CANVAS - VIEWPORT DONUSUMU
Canvas piksel cinsinden (800x600), viewport dunya birimi cinsinden (1x1).
Donusum formulleri:
\\[ V_x = C_x \\cdot \\frac{{V_w}}{{C_w}} \\]
\\[ V_y = C_y \\cdot \\frac{{V_h}}{{C_h}} \\]
\\[ V_z = d \\]
Bu formulleri somut orneklerle acikla (mesela piksel (200, 150) viewport'ta nereye denk gelir?).

6. GORSELLER:
<div class="figure"><img src="../../images/raytracing/figure-2-3.png" alt="Kamera yonelimi"><div class="caption">Sekil 2-3: Kamera yonelimi ve koordinat eksenleri</div></div>
<div class="figure"><img src="../../images/raytracing/figure-2-4.png" alt="Viewport"><div class="caption">Sekil 2-4: Viewport - kameranin onundeki goruntuleme alani</div></div>

7. EKSTRA MATEMATIK (math-box):
- Olcekleme (scaling) nedir? Ornekle acikla.
- Piksel koordinatlari vs dunya koordinatlari farki
- Neden viewport'un merkezi ile canvas'in merkezi hizali?

8. RAYLIB UYGULAMASI (raylib-box):
Asagidaki kodu goster ve acikla:
- Camera3D yapisi: position, target, up, fovy, projection
- BeginMode3D/EndMode3D: 3B cizim modu
- DrawSphere: 3B kure cizimi
- DrawLine3D: 3B cizgi (koordinat eksenleri gosterimi)
- UpdateCamera: kamera hareketi (fare ile dondurme)
- CAMERA_ORBITAL modu

{raylib_code_html.get('ornek02_kure_cizimi.c', '')}

EN AZ 1500 kelime. Cok detayli ol."""
        },

        # ── BÖLÜM 3: IŞINLARI İZLEMEK ──
        {
            "filename": "03-isinlari-izleme.html",
            "title": "Işınları İzlemek: Işın ve Küre Denklemleri",
            "prev": ("02-temel-varsayimlar.html", "Temel Varsayımlar ve Viewport"),
            "next": ("04-isin-kure-kesisimi.html", "Işın-Küre Kesişimi"),
            "prompt": f"""Isin denklemi ve kure denklemini anlatan kapsamli Turkce egitim sayfasi olustur.

KAPSAMLI OLARAK SU KONULARI ISLE:

1. ISINLARI IZLEMEK - TEMEL FIKIR
Onceki bolumde her piksel icin viewport'taki noktayi bulduk. Simdi o noktadan gorunen rengi bulmamiz gerekiyor. Kameradan viewport noktasina dogru bir "isin" (ray) gonderiyoruz. Bu isin sahnedeki nesnelere carpinca o nesnenin rengini aliyoruz. Bu kavrami DETAYLI anlat.

Gorsel:
<div class="figure"><img src="../../images/raytracing/figure-2-5.png" alt="Isin izleme"><div class="caption">Sekil 2-5: Kameradan viewport uzerinden sahnedeki nesnelere isinlar gonderme</div></div>

2. VEKTOR KAVRAMI (math-box icinde COK DETAYLI):
- Vektor nedir? (buyuklugu VE yonu olan nicelik)
- Skaler vs vektor farki
- 3B vektor gosterimi: \\(\\vec{{v}} = (v_x, v_y, v_z)\\)
- Vektor toplama: \\(\\vec{{a}} + \\vec{{b}} = (a_x+b_x, a_y+b_y, a_z+b_z)\\)
- Vektor cikarma: \\(\\vec{{a}} - \\vec{{b}}\\)
- Skaler ile carpma: \\(t \\cdot \\vec{{v}} = (t \\cdot v_x, t \\cdot v_y, t \\cdot v_z)\\)
- Somut ornekler ver (sayisal)

3. ISIN DENKLEMI (THE RAY EQUATION)
Bir isin, baslangic noktasi O ve yonu D ile tanimlanir:
\\[ P = O + t\\vec{{D}} \\]
Burada t herhangi bir reel sayidir. t'nin farkli degerleri isin uzerindeki farkli noktalari verir.
- t = 0 ise P = O (baslangic noktasi)
- t = 1 ise P = O + D (viewport noktasi)
- t < 0 ise kameranin arkasi
- t > 0 ise kameranin onu
Bu denklemi COK DETAYLI, adim adim, orneklerle acikla.

Gorsel:
<div class="figure"><img src="../../images/raytracing/figure-2-6.png" alt="Parametrik isin"><div class="caption">Sekil 2-6: Isin denklemi - farkli t degerleri farkli noktalar verir</div></div>

4. NOKTA CARPIM (DOT PRODUCT) - math-box icinde COK DETAYLI:
- Iki vektorun nokta carpimi: \\(\\langle \\vec{{a}}, \\vec{{b}} \\rangle = a_x b_x + a_y b_y + a_z b_z\\)
- Sonuc bir SKALER (sayi), vektor degil!
- Geometrik anlami: iki vektorun ne kadar "ayni yonde" oldugunu olcer
- Bir vektorun uzunlugu: \\(|\\vec{{v}}| = \\sqrt{{\\langle \\vec{{v}}, \\vec{{v}} \\rangle}}\\)
- Sayisal ornekler ver: (1,2,3) . (4,5,6) = 4+10+18 = 32
- Dagitma ozelligi: \\(\\langle \\vec{{a}} + \\vec{{b}}, \\vec{{c}} \\rangle = \\langle \\vec{{a}}, \\vec{{c}} \\rangle + \\langle \\vec{{b}}, \\vec{{c}} \\rangle\\)

5. KURE DENKLEMI (THE SPHERE EQUATION)
Kure = sabit bir noktadan (merkez C) sabit uzaklikta (yaricap r) olan noktalarin kumesi.
\\[ |P - C| = r \\]
Uzaklik = vektorun uzunlugu:
\\[ \\sqrt{{\\langle P - C, P - C \\rangle}} = r \\]
Iki tarafin karesini alalim:
\\[ \\langle P - C, P - C \\rangle = r^2 \\]
Her adimi acikla.

Gorsel:
<div class="figure"><img src="../../images/raytracing/figure-2-7.png" alt="Kure"><div class="caption">Sekil 2-7: Kure - merkez C ve yaricap r ile tanimlanir</div></div>

6. RAYLIB UYGULAMASI (raylib-box):
Viewport ve isin kavramlarini 3D olarak gorsellestiren kodu goster ve acikla:
- Gercek 3D küreler (DrawSphere, DrawSphereWires) kullanilarak sahne olusturulur
- 3D uzayda viewport düzlemi (z=1) cizilir ve grid ile bölünür
- RaySphereIntersect: isin-küre kesisim fonksiyonu (kitaptaki formülün C implementasyonu)
- GetScreenToWorldRay: fare konumundan 3D isin hesaplama
- Space tusu ile viewport üzerinden NxN isin gridi gönderilir
- DrawLine3D: 3D cizgilerle isinlar gosterilir
- Isinlar en yakin küreye carptığında o kürenin rengiyle boyanir
- Camera3D ve CAMERA_ORBITAL ile sahne etrafinda dönme

{raylib_code_html.get('ornek03_viewport_ve_isinlar.c', '')}

EN AZ 2000 kelime. Ozellikle vektor ve nokta carpim aciklamalari COK DETAYLI olmali."""
        },

        # ── BÖLÜM 4: IŞIN-KÜRE KESİŞİMİ ──
        {
            "filename": "04-isin-kure-kesisimi.html",
            "title": "Işın-Küre Kesişimi",
            "prev": ("03-isinlari-izleme.html", "Işınları İzlemek"),
            "next": ("05-ilk-kurelerimiz.html", "İlk Kürelerimizi Çizdirmek"),
            "prompt": """Isin ve kurenin kesisimini matematiksel olarak turetmeyi anlatan kapsamli Turkce egitim sayfasi olustur.

KAPSAMLI OLARAK SU KONULARI ISLE:

1. PROBLEM TANIMI
Elimizde iki denklem var:
- Isin: \\( P = O + t\\vec{D} \\)
- Kure: \\( \\langle P - C, P - C \\rangle = r^2 \\)
Bu iki denklemin ayni anda saglandigi P noktalarini bulmak istiyoruz. Yani isin kureyle nerede kesisiyor?

2. DENKLEMI TURETME (ADIM ADIM, COK DETAYLI)
P yerine isin denklemini koy:
\\[ \\langle O + t\\vec{D} - C, O + t\\vec{D} - C \\rangle = r^2 \\]

\\(\\vec{CO} = O - C\\) tanimla, denklemi ac:
\\[ \\langle \\vec{CO} + t\\vec{D}, \\vec{CO} + t\\vec{D} \\rangle = r^2 \\]

Nokta carpimin dagitma ozelligini kullanarak ac:
\\[ \\langle \\vec{CO}, \\vec{CO} \\rangle + 2\\langle \\vec{CO}, t\\vec{D} \\rangle + \\langle t\\vec{D}, t\\vec{D} \\rangle = r^2 \\]

t'yi disari cikar:
\\[ t^2 \\langle \\vec{D}, \\vec{D} \\rangle + 2t \\langle \\vec{CO}, \\vec{D} \\rangle + \\langle \\vec{CO}, \\vec{CO} \\rangle - r^2 = 0 \\]

Bu bir IKINCI DERECE DENKLEM:
\\[ a = \\langle \\vec{D}, \\vec{D} \\rangle \\]
\\[ b = 2\\langle \\vec{CO}, \\vec{D} \\rangle \\]
\\[ c = \\langle \\vec{CO}, \\vec{CO} \\rangle - r^2 \\]
\\[ at^2 + bt + c = 0 \\]

HER ADIMI TEK TEK, YAVAŞÇA, ORNEKLERLE ACIKLA.

3. IKINCI DERECE DENKLEM (QUADRATIC) - math-box icinde COK DETAYLI:
- \\( ax^2 + bx + c = 0 \\) formundaki denklem
- Cozum formulü: \\( x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a} \\)
- Diskriminant = \\( b^2 - 4ac \\):
  * Diskriminant > 0: iki farkli cozum (isin kureyi iki noktada keser)
  * Diskriminant = 0: tek cozum (isin kureye teget)
  * Diskriminant < 0: cozum yok (isin kureyi kesmez)
- SAYISAL ORNEK: a=1, b=-5, c=6 coz ve acikla
- Geometrik anlamini DETAYLI acikla

4. GEOMETRIK YORUM
Gorsel:
<div class="figure"><img src="../../images/raytracing/figure-2-8.png" alt="Kesisim durumlari"><div class="caption">Sekil 2-8: Uc durum - kesisim yok, temas (teget), iki noktada kesisim</div></div>

Uc durumu acikla:
- Isin kureyi kesmez: diskriminant negatif
- Isin kureye teget: diskriminant sifir (tam yuzeyden gecer)
- Isin kureyi iki noktada keser: diskriminant pozitif (girer ve cikar)

5. SAYISAL ORNEK
Kamera O=(0,0,0), isin yonu D=(0,0,1), kure merkez C=(0,0,5), yaricap r=1.
Adim adim hesapla:
- CO = O - C = (0,0,-5)
- a = D.D = 1
- b = 2*CO.D = 2*(0*0+0*0+(-5)*1) = -10
- c = CO.CO - r^2 = 25 - 1 = 24
- disk = 100 - 96 = 4
- t1 = (10+2)/2 = 6, t2 = (10-2)/2 = 4
Yorum: isin kureye t=4'te girer, t=6'da cikar.

6. EKSTRA: NEDEN NOKTA CARPIM KULLANIYORUZ? (info-box)
Uzunluk hesabi, aci hesabi, projeksiyon... Nokta carpimin faydalarini ozet olarak anlat.

EN AZ 2000 kelime. Matematik turetmelerini ADIM ADIM, COK DETAYLI yap."""
        },

        # ── BÖLÜM 5: İLK KÜRELERİMİZ ──
        {
            "filename": "05-ilk-kurelerimiz.html",
            "title": "İlk Kürelerimizi Çizdirmek",
            "prev": ("04-isin-kure-kesisimi.html", "Işın-Küre Kesişimi"),
            "next": ("../light/01-isik-giris.html", "Işık ve Aydınlatma"),
            "prompt": f"""Tum bilgileri birlestirip ilk isin izleme goruntusunu olusturmayi anlatan kapsamli Turkce egitim sayfasi olustur.

KAPSAMLI OLARAK SU KONULARI ISLE:

1. PARAMETRE t'NIN ANLAMI
Isin denklemi P = O + tD'de t parametresinin anlamini tekrar vurgula:
- t = 0: kamera noktasi (O)
- t = 1: viewport noktasi (V)
- t < 0: kameranin arkasi (istemiyoruz!)
- t > 1: viewport'un otesi (gercek sahne nesneleri burada)
- 0 < t < 1: kamera ile viewport arasi

Gorsel:
<div class="figure"><img src="../../images/raytracing/figure-2-9.png" alt="Parametre uzayi"><div class="caption">Sekil 2-9: t parametresinin farkli aralik degerleri ve anlamlari</div></div>

Dolayisiyla t_min = 1 ve t_max = sonsuz aliyoruz. Sadece viewport'un otesindeki nesneleri goruyoruz.

2. TAM ALGORITMA (PSEUDOCODE)
Ana dongu:
- Her piksel (x, y) icin:
  1. CanvasToViewport(x, y) ile viewport noktasini bul
  2. TraceRay(O, D, 1, inf) ile rengi bul
  3. PutPixel(x, y, renk) ile pikseli boya

TraceRay fonksiyonu:
- Her kure icin IntersectRaySphere cagir
- En yakin kesisimi (en kucuk t) bul
- O kurenin rengini dondur
- Kesisim yoksa arka plan rengi dondur

IntersectRaySphere fonksiyonu:
- Ikinci derece denklemi coz
- t1 ve t2 degerlerini dondur

Her fonksiyonu pseudocode olarak yaz ve DETAYLI acikla.

3. SAHNE TANIMLAMASI
Basit sahnemizi tanimla:
- Viewport: 1x1, mesafe d=1
- Kirmizi kure: merkez (0, -1, 3), yaricap 1
- Mavi kure: merkez (2, 0, 4), yaricap 1
- Yesil kure: merkez (-2, 0, 4), yaricap 1

Gorsel:
<div class="figure"><img src="../../images/raytracing/figure-2-10.png" alt="Sahne"><div class="caption">Sekil 2-10: 3 kureli basit sahnemiz</div></div>

4. SONUC
Bu algoritmayı calistirinca ne elde ediyoruz:
<div class="figure"><img src="../../images/raytracing/figure-2-11.png" alt="Sonuc"><div class="caption">Sekil 2-11: Ilk isin izleme goruntumuz - 3 renkli kure!</div></div>

Kureler daire gibi gorunuyor (kure gibi degil). Neden? Cunku isik modeli yok - nesneler duz renkli. Isik, golge, yansima ekleyince gercekci gorunecek (sonraki bolumler).

5. RAYLIB ILE TAM RAYTRACER (raylib-box - EN ONEMLI KISIM):
Asagidaki kodu goster ve HER FONKSIYONU, HER SATIRI DETAYLI acikla:
- Vec3 yapisi ve vektor islemleri (vec3_sub, vec3_dot, vb.)
- Sphere yapisi
- Sahne tanimlamasi (4 kure)
- IntersectRaySphere: ikinci derece denklem cozumu
- TraceRay: en yakin kesisimi bulma
- CanvasToViewport: piksel -> viewport donusumu
- Ana dongu: her piksel icin TraceRay cagirma
- Image/Texture kullanimi: pikselleri bir goruntüye yazma

{raylib_code_html.get('ornek04_basit_raytracer.c', '')}

Bu kodun kitaptaki pseudocode ile birebir uyumunu goster.

6. OZET VE SIRADAKI ADIMLAR
- Bu bolumde ne ogrendik: kamera, viewport, isin denklemi, kure denklemi, kesisim, algoritma
- Neden kureler duz renkli gorunuyor (isik modeli eksik)
- Sonraki bolum: ISIK (diffuse, specular, ambient)

EN AZ 2000 kelime. Ozellikle raylib kodu aciklamasi COK DETAYLI olmali."""
        },
    ]


def get_light_chapters(raylib_code_html):
    """Işık bölümü tanımlarını döndürür."""
    return [
        # ── IŞIK BÖLÜM 1: GİRİŞ VE IŞIK KAYNAKLARI ──
        {
            "filename": "01-isik-giris.html",
            "title": "Işık ve Aydınlatma",
            "prev": ("../raytracing/05-ilk-kurelerimiz.html", "İlk Kürelerimizi Çizdirmek"),
            "next": ("02-diffuse-yansima.html", "Diffuse Yansıma"),
            "prompt": """Isik (light) kavramina giris yapan ve isik kaynaklarini anlatan kapsamli Turkce egitim sayfasi olustur.

KAPSAMLI OLARAK SU KONULARI ISLE:

1. ISIK NEDIR VE NEDEN ONEMLI?
Onceki bolumde kureleri cizdik ama duz renkli daireler gibi gorunuyorlardi. Neden? Cunku isik modeli yok! Gercek dunyada nesnelerin 3 boyutlu gorunmesini saglayan sey ISIKTIR. Isik, golge ve yansima olmadan nesneler düz gorunur. Bu baglami DETAYLI anlat.

2. BASITLESTIRICI VARSAYIMLAR
- Tum isiklar BEYAZ olsun (sadece bir yoğunluk degeri i kullaniyoruz). Renkli isik icin her kanal icin ayri hesap yapilir ama simdilik basit tutalim.
- Atmosferi yok sayiyoruz: gercekte uzaktaki isiklar soluk gorunur (havadaki parcaciklar yuzunden). Biz bunu gormezden geliyoruz.
Bu varsayimlarin neden yapildigini ve sonuclarina etkisini acikla.

3. NOKTASAL ISIK KAYNAKLARI (Point Lights)
- Sabit bir noktadan her yone esit isik yayar (omnidirectional)
- Konum (position) ve yogunluk (intensity) ile tanimlanir
- Gercek hayat ornegi: ampul
- Isik vektoru: \\( \\vec{L} = Q - P \\) (isik konumu Q, yuzey noktasi P)
- Her nokta icin FARKLI isik vektoru hesaplanir

Gorsel:
<div class="figure"><img src="../../images/light/05-point-light.png" alt="Noktasal isik"><div class="caption">Sekil 3-1: Noktasal isik kaynagi - her noktaya farkli yon</div></div>

4. YONLU ISIK KAYNAKLARI (Directional Lights)
- Sonsuz uzaktan gelen, SABİT yonlu isik (Gunes ornegi)
- Gunes noktasal gibi dusunulebilir ama Dunya olceginde cok uzak, isinlar neredeyse paralel
- Yon (direction) ve yogunluk ile tanimlanir, konumu yok
- Tum noktalar icin AYNI isik vektoru \\( \\vec{L} \\)

Gorsel:
<div class="figure"><img src="../../images/light/05-directional-light.png" alt="Yonlu isik"><div class="caption">Sekil 3-2: Yonlu isik kaynagi - tum noktalara ayni yon</div></div>

5. ORTAM ISIGI (Ambient Light)
- Gercekte isik nesnelerden sekmez mi? Evet! Isik bir nesneye carpar, bir kismi yutulur, geri kalani sahneye saçılır (scattered). Bu saçılan isik baska nesnelere carpar, tekrar saçılır... (global illumination)
- Bunu tamamen simule etmek COK karmasik (global illumination arastirin!)
- Basit cozum: ORTAM ISIGI - sahnenin her noktasina sabit bir miktar isik ekle
- Sadece yogunluk degeri var, konumu veya yonu yok
- Genellikle sahnede tek bir ambient isik yeterli
- Ornek sahne: ambient 0.2, point 0.6, directional 0.2 (toplam 1.0)

6. ISIK TURLERI OZET TABLOSU
Bir tablo veya liste ile 3 isik turunu karsilastir:
| Tur | Konum | Yon | Kullanim Alani |

7. EKSTRA BILGILER (info-box):
- Isik yogunlugu (intensity) nedir? 0-1 arasi deger
- Neden yogunluklar toplami 1.0? (asiri parlaklik/overexposure onleme)
- Global illumination nedir? (kisa tanitim)

EN AZ 1500 kelime. Detayli ol."""
        },

        # ── IŞIK BÖLÜM 2: DİFFUSE YANSIMA ──
        {
            "filename": "02-diffuse-yansima.html",
            "title": "Diffuse (Yayınık) Yansıma",
            "prev": ("01-isik-giris.html", "Işık ve Aydınlatma"),
            "next": ("03-specular-yansima.html", "Specular Yansıma"),
            "prompt": f"""Diffuse (yayinik) yansimayi anlatan kapsamli Turkce egitim sayfasi olustur.

KAPSAMLI OLARAK SU KONULARI ISLE:

1. MAT (MATTE) NESNELER VE DIFFUSE YANSIMA
- Mat nesneler isigi her yone esit sacar (diffuse reflection)
- Nereden bakarsan bak ayni rengi gorursun (duvara bak, hareket et - renk degismez)
- FAKAT isik acisina gore PARLAKLIK degisir
- Isik dik geldiginde yuzey daha parlak, yana geldiginde daha loş
- Neden? Ayni enerji daha genis alana yayilir

Gorsel:
<div class="figure"><img src="../../images/light/06-light-spread.png" alt="Isik yayilimi"><div class="caption">Sekil 3-3: Ayni genislikli iki isik demeti - dik ve acili yuzey vurusu</div></div>

2. YUZEY NORMALI (SURFACE NORMAL)
- Normal = yuzeye DİK birim vektor
- Uzunlugu 1 (birim vektor / unit vector)
- \\( \\vec{{N}} \\) ile gosterilir
- Her noktanin kendi normali vardir

3. DIFFUSE FORMÜLÜNÜ TÜRETME (math-box icinde COK DETAYLI)
Isik yonu \\(\\vec{{L}}\\), normal \\(\\vec{{N}}\\), aralarindaki aci \\(\\alpha\\).

Gorsel:
<div class="figure"><img src="../../images/light/06-diffuse-diagram.png" alt="Diffuse diyagram"><div class="caption">Sekil 3-4: Isik, normal ve yuzey geometrisi</div></div>
<div class="figure"><img src="../../images/light/06-qrp.png" alt="QRP ucgeni"><div class="caption">Sekil 3-5: PQR dik ucgeni - cos(alpha) = I/A tureten geometri</div></div>

- PQR dik ucgeninden: \\( \\cos(\\alpha) = I / A \\)
- Nokta carpim ile: \\( \\cos(\\alpha) = \\frac{{\\langle \\vec{{N}}, \\vec{{L}} \\rangle}}{{|\\vec{{N}}| \\cdot |\\vec{{L}}|}} \\)
- Son formul: \\( I / A = \\frac{{\\langle \\vec{{N}}, \\vec{{L}} \\rangle}}{{|\\vec{{N}}| \\cdot |\\vec{{L}}|}} \\)
- DIKKAT: \\( \\cos(\\alpha) < 0 \\) olabilir (aci > 90 derece). Bu durumda isik yuzeyin ARKASINI aydinlatiyor, 0 olarak al.
Her adimi COKK detayli, sayisal orneklerle acikla. Trigonometri bilmeyenler icin cos fonksiyonunu anlat.

4. TAM DIFFUSE AYDINLATMA DENKLEMI
\\[ I_P = I_A + \\sum_{{i=1}}^{{n}} I_i \\cdot \\frac{{\\langle \\vec{{N}}, \\vec{{L_i}} \\rangle}}{{|\\vec{{N}}| \\cdot |\\vec{{L_i}}|}} \\]
Her terimi acikla. Negatif terimleri ekleme!

5. KÜRE NORMALLERİ
Kure icin normal hesaplamak cok kolay:
\\( \\vec{{N}} = \\frac{{P - C}}{{|P - C|}} \\)
Merkez C, yuzey noktasi P. Normalin neden bu oldugunu acikla.

Gorsel:
<div class="figure"><img src="../../images/light/06-sphere-normal.png" alt="Kure normali"><div class="caption">Sekil 3-6: Kurenin yuzey normali - merkezden yuzey noktasina yon</div></div>

6. PSEUDOCODE: ComputeLighting ve TraceRay GUNCELLEME
ComputeLighting(P, N) fonksiyonunu pseudocode olarak yaz. TraceRay'in guncellenmis halini goster:
- Kesisim noktasi P = O + closest_t * D
- Normal N = (P - sphere.center) / |P - sphere.center|
- Renk = sphere.color * ComputeLighting(P, N)

7. DIFFUSE SONUC GORSELI
<div class="figure"><img src="../../images/light/raytracer-02.png" alt="Diffuse sonuc"><div class="caption">Sekil 3-7: Diffuse aydinlatma ile render - kureler artik 3D gorunuyor!</div></div>
Buyuk sari kurenin neden duz zemin gibi gorundugunü acikla (cok buyuk yuzey).

8. RAYLIB KODU (raylib-box - COK DETAYLI ACIKLA):
{raylib_code_html.get('ornek05_diffuse_aydinlatma.c', '')}

Her fonksiyonu ve satirini acikla:
- Light yapisi ve 3 isik kaynagi tanimlamasi
- ComputeLighting: ambient + diffuse hesabi
- Normal hesaplama: vec3_norm(vec3_sub(P, center))
- Renk carpimi: sphere.color * light_intensity

EN AZ 2000 kelime. Matematik turetmeleri COK DETAYLI."""
        },

        # ── IŞIK BÖLÜM 3: SPECULAR YANSIMA ──
        {
            "filename": "03-specular-yansima.html",
            "title": "Specular (Aynamsı) Yansıma",
            "prev": ("02-diffuse-yansima.html", "Diffuse Yansıma"),
            "next": None,
            "prompt": f"""Specular (aynamsi/parlak) yansimayi anlatan kapsamli Turkce egitim sayfasi olustur.

KAPSAMLI OLARAK SU KONULARI ISLE:

1. PARLAK NESNELER
- Mat nesneler isigi her yone sacar. Peki parlak nesneler? (bilardo topu, cilalanmis araba)
- Parlak nesnelerde parlak noktalar (highlights) gorursun, hareket ettikce yer degistirir
- Bu SPECULAR yansima (speculum = Latince ayna)
- Specular, diffuse'un YERINE gecmez, ONU TAMAMLAR

2. YÜZEY PÜRÜZLÜLÜĞü
Gorsel:
<div class="figure"><img src="../../images/light/06-rough-surface.png" alt="Puruzlu yuzey"><div class="caption">Sekil 3-8: Mat yuzey - mikroskobik duzeyde rastgele yonlenmis parcaciklar</div></div>
<div class="figure"><img src="../../images/light/06-mirror.png" alt="Ayna yuzey"><div class="caption">Sekil 3-9: Parlak yuzey (ayna) - isik tek yonde yansir</div></div>

- Mat: mikroskobik parcaciklar rastgele yonlenmis, isik her yone sacilinir
- Parlak: yuzey duzenli, isik belirli bir yonde (R) yansir
- "Cilalanmislik" derecesine gore R etrafinda ne kadar isik dagilir degisir

Gorsel:
<div class="figure"><img src="../../images/light/07-specular-decay.png" alt="Specular dagilim"><div class="caption">Sekil 3-10: Parlaklik derecesine gore isik dagilimi - R etrafinda yogunlasma</div></div>

3. YANSIMA VEKTORU R HESAPLAMA (math-box COK DETAYLI)
\\( \\vec{{L}} \\): isik yonu (isiga dogru)
\\( \\vec{{N}} \\): yuzey normali
\\( \\vec{{R}} \\): yansima vektoru
\\( \\vec{{V}} \\): goruntuye dogru (kameraya) vektor = \\( -\\vec{{D}} \\)
\\( \\alpha \\): \\( \\vec{{R}} \\) ile \\( \\vec{{V}} \\) arasindaki aci

Gorsel:
<div class="figure"><img src="../../images/light/07-specular-diagram.png" alt="Specular diyagram"><div class="caption">Sekil 3-11: V, R ve alpha acisi</div></div>

L'yi N'e paralel ve dik bilesenlerine ayir:
\\( \\vec{{L_N}} = \\vec{{N}} \\langle \\vec{{N}}, \\vec{{L}} \\rangle \\) (N'e paralel)
\\( \\vec{{L_P}} = \\vec{{L}} - \\vec{{L_N}} \\) (N'e dik)

Gorsel:
<div class="figure"><img src="../../images/light/08-nl.png" alt="L bilesenleri"><div class="caption">Sekil 3-14: L vektorunun N'e paralel ve dik bilesenleri</div></div>
<div class="figure"><img src="../../images/light/08-vec-r.png" alt="R vektoru"><div class="caption">Sekil 3-15: R vektoru - L'nin N'e gore simetrik yansimasi</div></div>

R, L'nin N'e gore simetrigi:
\\( \\vec{{R}} = \\vec{{L_N}} - \\vec{{L_P}} = 2\\vec{{N}} \\langle \\vec{{N}}, \\vec{{L}} \\rangle - \\vec{{L}} \\)

HER ADIMI tek tek, sayisal ornekle acikla.

4. SPECULAR FORMUL
cos(alpha) fonksiyonunun guzel ozellikleri:
- cos(0) = 1 (tam yansima yonunde bakiyoruz - max parlaklik)
- cos(90) = 0 (yana bakiyoruz - parlaklik yok)

Gorsel:
<div class="figure"><img src="../../images/light/07-cos-alpha.png" alt="cos alpha"><div class="caption">Sekil 3-12: cos(alpha) grafigi - 0'da max, 90'da sifir</div></div>

Farkli parlaklik dereceleri icin cos(alpha)^s kullaniyoruz. s = specular exponent.
- s buyuk -> dar parlak nokta (cok parlak)
- s kucuk -> genis parlak alan (az parlak)

Gorsel:
<div class="figure"><img src="../../images/light/07-specular-exponent.png" alt="Specular exponent"><div class="caption">Sekil 3-13: Farkli s degerleri icin cos(alpha)^s grafikleri</div></div>

Specular terim:
\\[ I_S = I_L \\left( \\frac{{\\langle \\vec{{R}}, \\vec{{V}} \\rangle}}{{|\\vec{{R}}| \\cdot |\\vec{{V}}|}} \\right)^s \\]

5. TAM AYDINLATMA DENKLEMI
\\[ I_P = I_A + \\sum_{{i=1}}^{{n}} I_i \\left[ \\frac{{\\langle \\vec{{N}}, \\vec{{L_i}} \\rangle}}{{|\\vec{{N}}| |\\vec{{L_i}}|}} + \\left( \\frac{{\\langle \\vec{{R_i}}, \\vec{{V}} \\rangle}}{{|\\vec{{R_i}}| |\\vec{{V}}|}} \\right)^s \\right] \\]
Her terimi tek tek acikla.

6. SAHNE GUNCELLEME
Kurelere specular deger ekle:
- Kirmizi: s=500 (parlak)
- Mavi: s=500 (parlak)
- Yesil: s=10 (biraz parlak)
- Zemin: s=1000 (cok parlak)
Mat nesneler icin s=-1 (specular hesaplanmaz).

7. SPECULAR SONUC
<div class="figure"><img src="../../images/light/raytracer-03.png" alt="Specular sonuc"><div class="caption">Sekil 3-16: Diffuse + Specular ile render - parlak noktalar belirdi!</div></div>
Kirmizi kurede (s=500) dar parlak nokta, yesil kurede (s=10) genis parlak alan oldugunu acikla.

8. RAYLIB KODU (raylib-box - COKK DETAYLI):
{raylib_code_html.get('ornek06_specular_aydinlatma.c', '')}

Her fonksiyonu DETAYLI acikla:
- Sphere yapisina eklenen specular alani
- ComputeLighting'e eklenen V ve spec parametreleri
- R vektoru hesabi: R = 2*N*dot(N,L) - L
- pow(rdv/(len(R)*len(V)), spec) ile specular terim
- V = -D (kameraya dogru yon)

9. OZET VE SONRAKI ADIMLAR
- Bu bolumde: isik kaynaklari, diffuse ve specular yansima
- Sonraki bolum: GOLGE ve YANSIMALAR (shadows and reflections)

EN AZ 2000 kelime. Matematik turetmeleri COK DETAYLI."""
        },
    ]
