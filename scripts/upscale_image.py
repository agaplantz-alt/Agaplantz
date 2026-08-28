import base64, json, os, sys, urllib.request
KEY = os.environ["GEMINI_API_KEY"].strip().strip("<>").strip()
SRC, OUT = sys.argv[1], sys.argv[2]
PROMPT = """Upscale this exact photograph to very high resolution. This is an UPSCALE, not a redesign:
reproduce the image pixel-for-pixel in content and composition — every plant, pot, leaf, shadow,
object and its exact position, size, color and orientation must remain identical. Change NOTHING
about what is in the frame.

Only do this: recover and render fine detail that the low-resolution source could not hold —
crisp leaf venation and edges, velvet leaf texture, terracotta and concrete grain, wood grain,
woven basket fibers, soil particles, the metal of the wire shelving. Remove compression artifacts,
blockiness and blur. Keep the identical framing, crop, aspect ratio, lighting, color grade and
depth of field. Do not add, remove, move or restyle any element. No text, no watermark."""
mime = "image/jpeg" if SRC.lower().endswith((".jpg", ".jpeg")) else "image/png"
body = {"contents": [{"role": "user", "parts": [
    {"inline_data": {"mime_type": mime, "data": base64.b64encode(open(SRC,'rb').read()).decode()}},
    {"text": PROMPT}]}],
    "generationConfig": {"responseModalities": ["TEXT","IMAGE"],
                         "imageConfig": {"aspectRatio": "16:9", "imageSize": "4K"}}}
req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",
    data=json.dumps(body).encode(),
    headers={"Content-Type":"application/json","x-goog-api-key":KEY})
try:
    resp = json.load(urllib.request.urlopen(req, timeout=900))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:800]); sys.exit(1)
for c in resp.get("candidates", []):
    for p in c.get("content", {}).get("parts", []):
        if "inlineData" in p:
            open(OUT,"wb").write(base64.b64decode(p["inlineData"]["data"])); print("wrote", OUT)
