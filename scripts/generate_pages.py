#!/usr/bin/env python3
"""
Bilgisayar Grafikleri - Sıfırdan
Ana içerik üretici betik.
Görselleri indirir, raylib kodlarını yazar, OpenAI ile Türkçe HTML sayfaları üretir.
"""

import os
import sys
import time
import argparse
import requests
from pathlib import Path

try:
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError:
    print("Gerekli paketler yukleniyor...")
    os.system(f"{sys.executable} -m pip install openai python-dotenv requests")
    from openai import OpenAI
    from dotenv import load_dotenv

from chapter_prompts import SYSTEM_PROMPT, get_chapters, get_light_chapters

# ═══════════════════════════════════════════
# YAPILANDIRMA
# ═══════════════════════════════════════════
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAYLIB_DIR = PROJECT_DIR / "raylib-kod"

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("HATA: OPENAI_API_KEY bulunamadi!")
    sys.exit(1)

client = OpenAI(api_key=api_key)
MODEL = "gpt-4o"

# ═══════════════════════════════════════════
# GÖRSEL İNDİRME
# ═══════════════════════════════════════════
SECTION_CONFIG = {
    "raytracing": {
        "images_dir": PROJECT_DIR / "images" / "raytracing",
        "pages_dir": PROJECT_DIR / "bolumler" / "raytracing",
        "get_chapters": get_chapters,
        "images": {
            "figure-2-1.jpg":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/image-000.jpg",
            "figure-2-2.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/image-001.png",
            "figure-2-3.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/03-camera-orientation.png",
            "figure-2-4.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/03-viewport.png",
            "figure-2-5.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/03-basic-raytracer.png",
            "figure-2-6.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/04-parametric.png",
            "figure-2-7.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/04-sphere.png",
            "figure-2-8.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/04-sphere-solutions.png",
            "figure-2-9.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/04-parameter-space.png",
            "figure-2-10.png": "https://gabrielgambetta.com/computer-graphics-from-scratch/images/04-simple-scene.png",
            "figure-2-11.png": "https://gabrielgambetta.com/computer-graphics-from-scratch/images/raytracer-01.png",
        },
    },
    "light": {
        "images_dir": PROJECT_DIR / "images" / "light",
        "pages_dir": PROJECT_DIR / "bolumler" / "light",
        "get_chapters": get_light_chapters,
        "images": {
            "05-point-light.png":      "https://gabrielgambetta.com/computer-graphics-from-scratch/images/05-point-light.png",
            "05-directional-light.png": "https://gabrielgambetta.com/computer-graphics-from-scratch/images/05-directional-light.png",
            "06-light-spread.png":     "https://gabrielgambetta.com/computer-graphics-from-scratch/images/06-light-spread.png",
            "06-diffuse-diagram.png":  "https://gabrielgambetta.com/computer-graphics-from-scratch/images/06-diffuse-diagram.png",
            "06-qrp.png":              "https://gabrielgambetta.com/computer-graphics-from-scratch/images/06-qrp.png",
            "06-sphere-normal.png":    "https://gabrielgambetta.com/computer-graphics-from-scratch/images/06-sphere-normal.png",
            "raytracer-02.png":        "https://gabrielgambetta.com/computer-graphics-from-scratch/images/raytracer-02.png",
            "06-rough-surface.png":    "https://gabrielgambetta.com/computer-graphics-from-scratch/images/06-rough-surface.png",
            "06-mirror.png":           "https://gabrielgambetta.com/computer-graphics-from-scratch/images/06-mirror.png",
            "07-specular-decay.png":   "https://gabrielgambetta.com/computer-graphics-from-scratch/images/07-specular-decay.png",
            "07-specular-diagram.png": "https://gabrielgambetta.com/computer-graphics-from-scratch/images/07-specular-diagram.png",
            "07-cos-alpha.png":        "https://gabrielgambetta.com/computer-graphics-from-scratch/images/07-cos-alpha.png",
            "07-specular-exponent.png":"https://gabrielgambetta.com/computer-graphics-from-scratch/images/07-specular-exponent.png",
            "08-nl.png":               "https://gabrielgambetta.com/computer-graphics-from-scratch/images/08-nl.png",
            "08-vec-r.png":            "https://gabrielgambetta.com/computer-graphics-from-scratch/images/08-vec-r.png",
            "raytracer-03.png":        "https://gabrielgambetta.com/computer-graphics-from-scratch/images/raytracer-03.png",
        },
    },
}

def download_images(images_dir, image_map):
    images_dir.mkdir(parents=True, exist_ok=True)
    for name, url in image_map.items():
        path = images_dir / name
        if path.exists():
            print(f"  [atla] {name}")
            continue
        try:
            print(f"  [indir] {name}...")
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            path.write_bytes(r.content)
        except Exception as e:
            print(f"  [hata] {name}: {e}")

# ═══════════════════════════════════════════
# HTML ŞABLONU
# ═══════════════════════════════════════════
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Bilgisayar Grafikleri Sifirdan</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../css/style.css">
    <script src="../../js/main.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/c.min.js"></script>
    <script>hljs.highlightAll();</script>
    <script type="text/javascript" async
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
</head>
<body>
    <header class="site-header" style="padding: 1.5rem;">
        <a href="../../index.html" style="color:#fff;text-decoration:none;">
            <h1 style="font-size:1.5rem;margin:0;">&#x1F5A5; Bilgisayar Grafikleri &mdash; Sifirdan</h1>
        </a>
    </header>
    <nav class="breadcrumb">
        <a href="../../index.html">Ana Sayfa</a> &gt;
        <a href="../../index.html#raytracing">Isin Izleme</a> &gt;
        <span>{title}</span>
    </nav>
    <main class="chapter-content">
{content}
    </main>
    <nav class="chapter-nav">
        {prev_link}
        {next_link}
    </nav>
    <footer class="site-footer">
        <p>Esinlenme kaynagi: <a href="https://gabrielgambetta.com/computer-graphics-from-scratch/" target="_blank">Computer Graphics from Scratch</a> &mdash; Gabriel Gambetta</p>
    </footer>
</body>
</html>"""

# ═══════════════════════════════════════════
# RAYLIB KOD YARDIMCISI
# ═══════════════════════════════════════════
def make_raylib_html(code, filename):
    """Raylib C kodunu HTML-safe kod bloğu olarak formatla."""
    safe = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<div class="code-filename">{filename}</div>\n'
        f'<pre><code class="language-c">{safe}</code></pre>'
    )

def load_raylib_codes():
    """raylib-kod/ klasöründen C dosyalarını oku ve HTML-safe hale getir."""
    codes = {}
    for cfile in RAYLIB_DIR.glob("*.c"):
        raw = cfile.read_text(encoding="utf-8")
        codes[cfile.name] = make_raylib_html(raw, cfile.name)
    return codes

# ═══════════════════════════════════════════
# İÇERİK ÜRETİMİ
# ═══════════════════════════════════════════
def generate_content(prompt, retries=2):
    """OpenAI API ile içerik üret."""
    for attempt in range(retries + 1):
        try:
            print(f"    [api] istek gonderiliyor (deneme {attempt+1})...")
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=8192,
                temperature=0.7,
            )
            content = response.choices[0].message.content
            # Eğer model markdown code fence ile sarıyorsa temizle
            if content.startswith("```html"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            return content.strip()
        except Exception as e:
            print(f"    [hata] {e}")
            if attempt < retries:
                print(f"    [bekle] 5 saniye...")
                time.sleep(5)
            else:
                return f"<h2>Icerik uretilemedi</h2><p>Hata: {e}</p>"

def build_page(chapter, pages_dir):
    """Tek bir sayfa üret ve kaydet."""
    print(f"\n{'='*50}")
    print(f"  BOLUM: {chapter['title']}")
    print(f"{'='*50}")

    content = generate_content(chapter["prompt"])

    prev_link = ""
    if chapter["prev"]:
        prev_link = f'<a href="{chapter["prev"][0]}" class="prev">{chapter["prev"][1]}</a>'

    next_link = ""
    if chapter["next"]:
        next_link = f'<a href="{chapter["next"][0]}" class="next">{chapter["next"][1]}</a>'

    html = HTML_TEMPLATE.format(
        title=chapter["title"],
        content=content,
        prev_link=prev_link,
        next_link=next_link,
    )

    path = pages_dir / chapter["filename"]
    path.write_text(html, encoding="utf-8")
    print(f"  [kaydet] {path}")
    return path

# ═══════════════════════════════════════════
# ANA FONKSİYON
# ═══════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Bilgisayar Grafikleri - Icerik Uretici")
    parser.add_argument("section", nargs="?", default="raytracing",
                        choices=SECTION_CONFIG.keys(),
                        help="Uretilecek bolum (varsayilan: raytracing)")
    parser.add_argument("--only", type=int, nargs="*",
                        help="Sadece belirtilen bolum numaralarini uret (1-indexed)")
    args = parser.parse_args()

    cfg = SECTION_CONFIG[args.section]
    images_dir = cfg["images_dir"]
    pages_dir = cfg["pages_dir"]

    print("=" * 55)
    print(f"  BILGISAYAR GRAFIKLERI - ICERIK URETICI [{args.section.upper()}]")
    print("=" * 55)

    # 1. Görselleri indir
    print("\n[1/3] Gorseller indiriliyor...")
    download_images(images_dir, cfg["images"])

    # 2. Raylib kodlarını oku
    print("\n[2/3] Raylib kodlari okunuyor...")
    raylib_html = load_raylib_codes()
    for name in raylib_html:
        print(f"  [ok] {name}")

    # 3. Sayfaları üret
    print("\n[3/3] Turkce sayfalar uretiliyor (OpenAI API)...")
    pages_dir.mkdir(parents=True, exist_ok=True)

    chapters = cfg["get_chapters"](raylib_html)

    if args.only:
        indices = [i - 1 for i in args.only if 1 <= i <= len(chapters)]
        chapters_to_gen = [(chapters[i], i) for i in indices]
    else:
        chapters_to_gen = [(ch, i) for i, ch in enumerate(chapters)]

    generated = []
    for idx, (chapter, _orig_idx) in enumerate(chapters_to_gen):
        print(f"\n  [{idx+1}/{len(chapters_to_gen)}] {chapter['title']}")
        path = build_page(chapter, pages_dir)
        generated.append(path)
        if idx < len(chapters_to_gen) - 1:
            print("  [bekle] 2 saniye (rate limit)...")
            time.sleep(2)

    print("\n" + "=" * 55)
    print("  TAMAMLANDI!")
    print("=" * 55)
    print(f"\n  Uretilen sayfalar:")
    for p in generated:
        print(f"    - {p}")
    print(f"\n  Gorseller: {images_dir}")
    print(f"  Sayfalar:  {pages_dir}")
    print(f"\n  Onizleme icin index.html dosyasini tarayicida acin.")

if __name__ == "__main__":
    main()
