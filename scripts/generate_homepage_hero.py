import base64, glob, json, os, sys, urllib.request

KEY = os.environ["GEMINI_API_KEY"].strip().strip("<>").strip()
REFS = sorted(glob.glob("/tmp/claude-0/-home-user-Agaplantz/60b495ef-f2b3-5139-b446-cb7f61429394/scratchpad/refs/*"))
OUT = sys.argv[1]
SEED = sys.argv[2] if len(sys.argv) > 2 else None

PROMPT = """Create ONE single photorealistic wide 16:9 hero banner image for the homepage of a
luxury rare-plant nursery. Bring EVERY plant from the reference images together into one
coherent, believable scene, all in the same place, lit by the same light.

USE THE FIRST REFERENCE IMAGE AS THE MASTER STYLE AND SET: same board-formed concrete wall,
same light-wood plank potting table, same chrome wire shelving on the right, same warm
late-afternoon sunlight raking in from the left casting soft dappled leaf shadows across the
concrete, same airy bright plant-shop atmosphere.

Place each specimen from the other references, keeping its OWN distinctive foliage,
coloration, variegation pattern and its OWN pot exactly as shown in its reference:

LEFT THIRD (foreground, on a rough natural stone plinth and the table's left end):
- The near-black burgundy velvet Anthurium with red-flushed heart leaves in the embossed
  terracotta pot, sitting on its rough-cut stone slab.
- Behind it, tall: the deep green Anthurium warocqueanum with brilliant white-silver venation
  in the decorated terracotta pot with the chevron rim and leaf relief.
- A polished copper watering can and wooden-handled hand tools resting on the table.

CENTER (on the light-wood plank table, the visual heart of the image):
- TWO DIFFERENT MONSTERAS, side by side, clearly distinct from each other — this is important:
  (a) Monstera albo: large fenestrated leaves split into BOLD SOLID BLOCKS of pure white against
      dark green, half-moon sectors, in the plain GREY CONCRETE CYLINDER pot.
  (b) Monstera Thai Constellation: leaves FRECKLED and SPLASHED all over with fine creamy-yellow
      speckling on green (no solid white half-moons), in the PEARLESCENT IRIDESCENT white-and-gold
      BOWL pot.
- The pink-and-green variegated Alocasia with ruffled rose-pink leaves in the polished brass pot.
- A small clear glass laboratory jar holding a tiny tissue-culture plantlet with pale pink
  petioles and bare white roots, with slim black tweezers resting beside it on the wood — a
  quiet nod to propagation, small and delicate, not dominating.



RIGHT THIRD (a low wooden stool, a hairpin-leg side table, and the chrome wire shelf):
- The variegated Alocasia Frydek, dark green leaves with white splashes and bold white veins,
  in its matte dark-charcoal pot on the small pale wooden stool.
- The variegated Philodendron billietiae with long rippled green-and-butter-yellow leaves in
  the fluted cream ceramic pot.
- The Philodendron with caramel, apricot and cream marbled leaves and red petioles in the white
  pot on the hairpin-leg stand.
- The Philodendron with glowing amber, bronze and orange variegated leaves in the ornate deep-red
  terracotta pot flecked with gold.

ABOVE RIGHT:
- The long strap-leaved dark green Anthurium/Philodendron hanging in the grey pot on a cream
  macrame hanger, its ribbon leaves cascading down into the frame from the top right corner.

COMPOSITION RULES:
- Wide cinematic 16:9 banner. Every plant clearly readable, nothing badly overlapped or cropped
  awkwardly; vary the heights so the eye travels across a graceful arc from left to right.
- Keep the UPPER-LEFT area of the concrete wall relatively clean and open — sunlit empty wall
  with only soft shadow — as breathing room for a website headline. Do not put text there;
  just leave it uncluttered.
- Depth: crisp detailed foreground, gently softened background greenery and bright daylight
  spilling in on the far right.


MANDATORY CHECKLIST — the finished image must contain ALL TWELVE distinct specimens below, each
visible and identifiable, none omitted, none duplicated, each in its own described pot:
 1. near-black burgundy Anthurium, embossed terracotta, on stone slab
 2. deep green Anthurium warocqueanum with white venation, decorated terracotta
 3. Monstera albo, SOLID WHITE sectors, grey concrete cylinder pot
 4. Monstera Thai Constellation, CREAM SPECKLED, pearlescent iridescent bowl pot
 5. pink ruffled variegated Alocasia, polished brass pot
 6. tiny tissue-culture plantlet in a clear glass jar with black tweezers
 7. variegated Alocasia Frydek, white-veined dark leaves, matte charcoal pot on wooden stool
 8. variegated Philodendron billietiae, long rippled green-and-yellow leaves, fluted cream pot
 9. Philodendron with CARAMEL/APRICOT marbled lobed leaves and red petioles, plain white pot on
    black hairpin-leg stand
10. Philodendron with glowing AMBER/ORANGE/BRONZE leaves, ornate deep-red terracotta pot flecked
    with gold
11. long strap-leaved dark green Anthurium hanging in a grey pot on a cream macrame hanger
12. copper watering can and wooden-handled hand tools on the table
Spread them across three depth tiers — floor/stone plinth, table top, and the wire shelf behind —
so every one of the twelve has its own clear space and nothing is hidden.

RENDERING: photorealistic editorial photograph, full-frame DSLR, 35mm lens, f/4, natural warm
color science, extremely fine detail — velvet leaf nap, crisp white venation, terracotta grain,
brushed brass, pearlescent glaze, woven macrame fiber, concrete pores, wood grain. Clean, sharp,
noise free, luxurious and serene. Absolutely NO text, NO letters, NO watermarks, NO logos,
NO people, NO duplicated or malformed plants."""

parts = []
for p in REFS:
    mime = "image/jpeg" if p.lower().endswith((".jpg", ".jpeg")) else "image/png"
    with open(p, "rb") as f:
        parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(f.read()).decode()}})
parts.append({"text": PROMPT})

gen = {"responseModalities": ["TEXT", "IMAGE"],
       "imageConfig": {"aspectRatio": "16:9", "imageSize": "4K"}}
if SEED:
    gen["seed"] = int(SEED)

body = {"contents": [{"role": "user", "parts": parts}], "generationConfig": gen}
req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
try:
    resp = json.load(urllib.request.urlopen(req, timeout=900))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:1200]); sys.exit(1)

ok = False
for cand in resp.get("candidates", []):
    for part in cand.get("content", {}).get("parts", []):
        if "inlineData" in part:
            open(OUT, "wb").write(base64.b64decode(part["inlineData"]["data"])); ok = True
            print("wrote", OUT)
        elif part.get("text"):
            print("NOTE:", part["text"][:300])
if not ok:
    print(json.dumps(resp)[:1200])
