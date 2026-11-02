---
title: Parts list
---

# Parts list

What to buy for one pod or three, with rough prices.

Prices are rough US estimates from October 2026. Check stock and price before buying. The full lists with
store links are in the repository: [`BOM-test.md`]({{ site.github.repository_url }}/blob/main/BOM-test.md) (one pod) and [`BOM.md`]({{ site.github.repository_url }}/blob/main/BOM.md) (three pods).

## One pod (test kit), about $145

| Part | Qty | Notes | Price |
|---|---|---|---|
| IMX708 Wide NoIR 120 deg camera module | 1 | Amazon clone about $33; official board $35-39 | $33 |
| Raspberry Pi 3B+ or Zero 2 W (with headers) | 1 | Headers needed for the IR driver | $17-22 |
| microSD, 32 GB high-endurance | 1 | | $8 |
| 5 V 2.5-3 A micro-USB supply and short thick cable | 1 | Do not skimp: brown-outs look like dead boards | $8 |
| 12 V 850 nm IR LED strip + Shelly Plus RGBW PM + 12 V supply | 1 | What runs now; see [IR light](ir-light). Alternative: 2 LED chips, resistor, MOSFET and perfboard ($12-25) | about $40-60 |
| M2.5 x 6 self-tapping screws, stainless | 4 (+2) | | few $ |
| 1.5 mm silicone cord | about 120 mm | Gasket | few $ |
| 25 mm round flat glass tile, 3.5 mm thick | 2 | Window; verify thickness with calipers | few $ |
| 1 g silica desiccant sachet | 1 | | few $ |
| N52 magnets, about 15 x 5 mm | 2 inside + 2 outside (+1 spare) | Confirm grade and size | $10 |
| Silicone sealant (100% aquarium-safe) and 5-minute epoxy | 1 each | Epoxy only for magnet pockets | $15 |
| ASA or PETG filament | about 70 g | | own stock |

## Three pods

About $275 to $320 without IR:

| Group | Cost |
|---|---|
| Cameras | $105-115 |
| Pi Zeros | $45-60 |
| Cables, SD cards and power | $60-70 |
| Magnets | $20-30 |
| Everything else | about $45 |

## Choices to know about

- **Window:** no stock 21 x 1 mm acrylic disc exists; the design uses the 25 mm glass tile instead.
- **Magnets:** 15 mm is not a stock K&J size. Pick the nearest and set `mag_d` and `mag_t` in `pod.scad`.
- **Camera:** the clone's dimensions differ from the official drawing. Re-measure if you buy a different one.

Next: [Lessons learned](lessons-learned)
