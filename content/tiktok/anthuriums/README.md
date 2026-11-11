# Anthurium TC carousels (TikTok)

Two posts, 19 slides each, 1080×1920 JPG (TikTok allows 35 slides per carousel, so 18 plants
× 2 slides are split in two). Each plant gets the same pair as the Alocasia post:

1. **MATURE PLANT**: the mature photo from the Shopify listing (image 2), tagged "Representative photo"
2. **TISSUE CULTURE · WHAT YOU GET**: the real plantlet photo (image 1), with CA$ price as of 2026-11-10

Each post ends with a "How it works / Shop the drop" slide.

- `slides/post-1/`, `anthurium-post-1.zip`: Forgetii Var., Red Crystallinum × Michelle, Clarinervium Var.,
  Warocqueanum, Magnificum × Forgetii Var., SKG Red × Tezula Red, AOS × Papi Var., Veitchii, Bonplandii Narrow Mix Var.
- `slides/post-2/`, `anthurium-post-2.zip`: Magnificum × Crystallinum Dark Form Var., Black Velvet, Crystallinum × Dorayaki,
  Dark Phoenix Mint Var., Bonplandii Narrow Albo Var., KOS × Crystallinum Crackin' Veins, Vittarifolium Var.,
  Queen of Hearts, DocBlock Red Crystallinum Michelle F2

Rebuild after editing `plants.json` (handle, name, subtitle, price):

    python3 build.py <tissue-culture photo dir> <mature photo dir> slides

Suggested caption:
> Rare Anthuriums, lab-grown 🌱 Mature plant vs. what you get, swipe to see both. Which one is going on your shelf?
> #AgaPlantz #RarePlants #Anthurium #TissueCulture #PlantTok #RareHouseplants #PlantsOfCanada

## Best sellers post (20 slides, `bestsellers/`, `anthurium-bestsellers.zip`)

Top 10 Anthuriums by units sold, last 12 months (Shopify analytics, 2026-11-11):
Warocqueanum 21 · Wendlingeri 18 · Delta Force 14 · Pallidiflorum 14 · Black Velvet 13 ·
Vittarifolium 9 · Veitchii 7 · King of Clarinervium × Silver Tiger 7 · Queen of Hearts 7 ·
Bonplandii Narrow Pink Variegated 6. Same mature + what-you-get pair per plant, no outro,
matching the 20-slide Alocasia post.

    python3 build.py <tc dir> <mature dir> bestsellers bestsellers.json 10 --no-outro
