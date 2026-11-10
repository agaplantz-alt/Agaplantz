"""Render the Anthurium tissue-culture TikTok carousel (1080x1920 JPGs).

Usage: python3 build.py <photo_dir> <out_dir>
photo_dir holds the Shopify featured images, named <product-handle>.<ext>.
"""
import base64, html, json, pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
PHOTOS = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
PLANTS = json.loads((HERE / "plants.json").read_text())

def data_uri(handle):
    f = next(PHOTOS.glob(handle + ".*"))
    mime = "image/png" if f.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=block');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden}
body{font-family:Poppins,sans-serif;color:#f4f1ea;position:relative;
 background:radial-gradient(120% 70% at 50% 25%,#3a423c 0%,#1c211e 55%,#0e110f 100%)}
.bg{position:absolute;inset:-80px;background-size:cover;background-position:center;
 filter:blur(60px) saturate(.6) brightness(.45);opacity:.55}
.leaf{position:absolute;top:200px;right:40px;font-size:0}
.wrap{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center}
.pill{margin-top:330px;background:#f4f1ea;color:#1b1f1c;font-weight:700;font-size:30px;
 letter-spacing:.2em;padding:16px 34px;border-radius:999px;box-shadow:0 6px 20px rgba(0,0,0,.35)}
.genus{margin-top:38px;font-weight:700;font-size:40px;letter-spacing:.28em;color:#d9d6cf}
.name{margin-top:6px;font-weight:800;font-size:var(--fs,96px);line-height:1.02;letter-spacing:-.03em;
 text-align:center;padding:0 60px;text-shadow:0 4px 18px rgba(0,0,0,.45)}
.sub{margin-top:14px;font-weight:700;font-size:40px;color:#c6e57a;letter-spacing:.01em;text-align:center}
.card{position:relative;margin-top:44px;width:900px;height:880px;border-radius:36px;overflow:hidden;
 background:#fff;box-shadow:0 24px 60px rgba(0,0,0,.5)}
.card img{width:100%;height:100%;object-fit:contain;background:#fff}
.tag{position:absolute;top:26px;left:26px;background:rgba(40,40,40,.82);color:#fff;font-weight:700;
 font-size:26px;padding:10px 22px;border-radius:999px}
.price{position:absolute;top:26px;right:26px;background:#c6e57a;color:#1b1f1c;font-weight:800;
 font-size:28px;padding:10px 22px;border-radius:999px}
/* cover */
.grid{margin-top:50px;display:grid;grid-template-columns:repeat(3,290px);gap:16px}
.grid div{height:290px;border-radius:26px;overflow:hidden;background:#fff;box-shadow:0 12px 30px rgba(0,0,0,.4)}
.grid img{width:100%;height:100%;object-fit:cover}
.lead{margin-top:40px;font-weight:600;font-size:36px;color:#d9d6cf;text-align:center;line-height:1.35}
.cta{margin-top:56px;background:#c6e57a;color:#1b1f1c;font-weight:800;font-size:46px;padding:26px 54px;border-radius:999px}
.steps{margin-top:48px;display:flex;flex-direction:column;gap:22px;width:860px}
.steps div{background:rgba(244,241,234,.08);border:2px solid rgba(244,241,234,.15);border-radius:28px;
 padding:26px 34px;font-size:36px;font-weight:600;line-height:1.3}
.steps b{color:#c6e57a}
"""

def page(body, bg=""):
    bgdiv = f'<div class="bg" style="background-image:url({bg})"></div>' if bg else ""
    return f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{bgdiv}<div class=wrap>{body}</div></body></html>"

def name_size(name):
    n = len(name)
    return 112 if n <= 11 else 96 if n <= 15 else 80 if n <= 19 else 68

def plant_slide(p):
    uri = data_uri(p["handle"])
    body = f"""
    <div class=pill>TISSUE CULTURE · WHAT YOU GET</div>
    <div class=genus>ANTHURIUM</div>
    <div class=name style="--fs:{name_size(p['name'])}px">{html.escape(p['name'])}</div>
    <div class=sub>{html.escape(p['sub'])}</div>
    <div class=card><img src="{uri}"><div class=tag>Ships as a 2–4 in plantlet</div>
      <div class=price>CA${p['price']}</div></div>"""
    return page(body, uri)

def cover():
    imgs = "".join(f'<div><img src="{data_uri(p["handle"])}"></div>' for p in PLANTS[:6])
    body = f"""
    <div class=pill>TISSUE CULTURE DROP</div>
    <div class=genus>RARE</div>
    <div class=name style="--fs:150px">Anthuriums</div>
    <div class=sub>{len(PLANTS)} collector plants · swipe →</div>
    <div class=grid>{imgs}</div>"""
    return page(body)

def outro():
    body = """
    <div class=pill>HOW IT WORKS</div>
    <div class=genus>AGAPLANTZ</div>
    <div class=name style="--fs:104px">Grow your own<br>collector plant</div>
    <div class=steps>
      <div><b>1.</b> Pick your Anthurium at agaplantz.com</div>
      <div><b>2.</b> We ship a lab-grown 2–4 in plantlet</div>
      <div><b>3.</b> Acclimate it and watch it grow up</div>
    </div>
    <div class=cta>Shop the drop · link in bio</div>"""
    return page(body)

slides = [cover()] + [plant_slide(p) for p in PLANTS] + [outro()]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    for i, s in enumerate(slides, 1):
        tmp = OUT / "_slide.html"; tmp.write_text(s)
        pg.goto(tmp.resolve().as_uri()); pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(OUT / f"{i:02d}.jpg"), type="jpeg", quality=92)
    tmp.unlink(); b.close()
print(f"rendered {len(slides)} slides -> {OUT}")
