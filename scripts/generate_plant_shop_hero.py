import base64, json, os, sys, urllib.request

KEY = os.environ["GEMINI_API_KEY"].strip().strip("<>").strip()
SRC = "/root/.claude/uploads/60b495ef-f2b3-5139-b446-cb7f61429394/9f04ee4c-image.png"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemini-3-pro-image"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-0/-home-user-Agaplantz/60b495ef-f2b3-5139-b446-cb7f61429394/scratchpad/out.png"

PROMPT = """Recreate this exact photograph at maximum fidelity and ultra-high resolution.

Scene: a sunlit outdoor plant-shop / greenhouse nursery display against a raw board-formed concrete wall, with a light-wood plank potting table in the foreground and a chrome wire shelving rack on the right.

Preserve the identical composition, camera angle, framing and layout of every plant:
- Left foreground: terracotta pots with dark Anthurium/Philodendron plants, a small trailing plant, an aged clay pot, a polished copper watering can with a long spout, wooden-handled hand tools laid on the table, and a small blank wooden sign block.
- Left-center on the table: a white ceramic pot with a variegated green-and-cream Dieffenbachia, a small terracotta nursery pot, a white cylindrical pot.
- Center: a tall clump of very dark velvety green Anthurium warocqueanum-style pendant leaves with pale silver-white venation, rising in front of the concrete wall.
- Center-right on the table: a white pot with a green Philodendron florida/pedatum, and a large white pot holding a heavily variegated white-and-green Monstera deliciosa albo with fenestrated leaves.
- Right foreground: a woven seagrass basket pot holding a nearly pure-white variegated Philodendron florida ghost with cream lobed leaves.
- Upper right: a chrome wire shelf with a cream textured ceramic pot holding a dark Philodendron melanochrysum with long drooping bronze-black leaves; a large dark velvet Anthurium with prominent white veins at far right; air plants (Tillandsia), and assorted tropical foliage receding into blurred greenery and daylight.

Lighting: warm natural late-afternoon sunlight raking from the left, soft dappled leaf shadows falling across the concrete wall and the wooden table, gentle highlights on glossy leaves, bright blown-out daylight in the background right.

Rendering: photorealistic DSLR photograph, 85mm lens look, shallow depth of field with a crisp foreground and softly blurred background, natural color science, extremely fine detail in leaf venation, velvet leaf texture, concrete pore texture, terracotta grain, woven basket fibers, brushed copper and soil surfaces. Clean, sharp, noise-free, gallery-quality resolution. No text, no watermarks, no logos, no people."""

with open(SRC, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

body = {
    "contents": [{
        "role": "user",
        "parts": [
            {"inline_data": {"mime_type": "image/png", "data": img_b64}},
            {"text": PROMPT},
        ],
    }],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {"aspectRatio": "16:9", "imageSize": "4K"},
    },
}

req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": KEY},
)
try:
    resp = json.load(urllib.request.urlopen(req, timeout=600))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:1500]); sys.exit(1)

n = 0
for cand in resp.get("candidates", []):
    for part in cand.get("content", {}).get("parts", []):
        if "inlineData" in part:
            open(OUT, "wb").write(base64.b64decode(part["inlineData"]["data"]))
            n += 1
            print("wrote", OUT, part["inlineData"].get("mimeType"))
        elif part.get("text"):
            print("MODEL TEXT:", part["text"][:400])
if not n:
    print(json.dumps(resp)[:1500])
