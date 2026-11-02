# Pet camera pods: bill of materials and sources

Three pods: Brazilian black tarantula, Mexican red knee tarantula, Surinam horned frog.
Prices and stock were checked on 2026-10-24 through search snippets and product pages, not a live cart.
**Check stock and price on the shop page before ordering.** "Unverified" means I did not find a listing.

## Electronics (per pod, x3)

| Part | Qty | Spec | Best source | Price |
|---|---|---|---|---|
| Camera | 3 | IMX708 Wide NoIR 120 deg module (ships with 15-22 and 15-15 pin 150 mm cables) | [Amazon listing](https://www.amazon.com/dp/B0GYW6YZRC) about $33. Fallback: official board, [Micro Center](https://www.microcenter.com/product/662019/raspberry-pi-camera-3-wide-noir) $34.99 or [Adafruit](https://www.adafruit.com/product/5660) $38.50 | $33 ea |
| Computer | 3 | Raspberry Pi Zero 2 W. Get the **"with headers"** version if you add the IR boards (they take 5 V and an enable pin from GPIO). | [Adafruit #5291](https://www.adafruit.com/product/5291) / [#6008 with header](https://www.adafruit.com/product/6008), [PiShop](https://www.pishop.us/product/raspberry-pi-zero-2-w/), [Micro Center](https://www.microcenter.com/product/643085/raspberry-pi-zero-2-w), [CanaKit](https://www.canakit.com/raspberry-pi-zero-2-w.html). US stock **unverified**; some listings showed out of stock. | $15-20 ea |
| Camera cable | 0 | Included with the camera (15-22 pin, 150 mm). Backup only: 30 cm pack if a Pi sits far from its enclosure. | iUniker pack on Amazon, or Pimoroni | $0 |
| microSD | 3 | 32 GB high-endurance | Any (not searched) | $8 ea |
| Power | 3 | 5 V 2.5 A micro-USB | Any (not searched) | $8 ea |

## Pod hardware (per pod, x3)

| Part | Qty | Spec | Source |
|---|---|---|---|
| Screws | 12 (+6) | M2.5 x 6 mm self-tapping, A4/316 stainless | McMaster-Carr or a fastener shop (not searched) |
| Gasket | 1 m | 1.5 mm silicone O-ring cord | [McMaster-Carr 1187N11](https://www.mcmaster.com/products/silicone-o-ring-cord-stock/) (found as 1.5 mm red silicone cord; confirm on the page). Alternative: [RS PRO 1.5 mm silicone cord](https://rs-thinkhub.com/product/rs-pro-silicone-cord-white-15mm-x-5m-lengths-2325745). |
| Window | 3 (+2) | 21 mm dia x 1 mm clear cast acrylic disc | **No stock 21 x 1 mm disc found.** Options: custom laser-cut circles from an Etsy seller or [Delvie's Plastics laser-cut discs](https://delviesplastics.com/products/crystal-clear-laser-cut-discs) (ask for 1 mm), or cut from 1 mm clear acrylic sheet. Or tell me and I will change the model to a stock size such as a 22 mm glass cover disc. |
| Desiccant | 3 | 1 g rechargeable silica gel sachet | Any (not searched) |
| Printed parts | 3 body + 3 cap | ASA or PETG, about 70 g per pod | Own stock |

## Magnets and mounting

| Part | Qty | Spec | Source |
|---|---|---|---|
| Inside magnets | 6 (+2) | N52 disc, about 15 x 5 mm, sealed in the pod | **15 mm is not a stock size at K&J** (they list fractional inches). Use the [K&J N52 disc list](https://www.kjmagnetics.com/products/grade-n52-magnets?filter=56,90) and pick the nearest size, or a metric 15 x 5 mm N52 disc from an Amazon seller (check the photo: one 15 x 5 mm listing found was a block, not a disc). Then set `mag_d` and `mag_t` in `pod.scad` to match. |
| Outside magnets | 6 | Same size, epoxy-coated if available ([K&J](https://www.kjmagnetics.com/d82e-neodymium-epoxy-coated-disc-magnet) sells epoxy-coated discs, [Total Element](https://totalelement.com/products/1-2-x-1-8-inch-strong-neodymium-rare-earth-disc-magnets-n52-with-black-epoxy-coating-24-pack) sells N52 with black epoxy) | as above |
| Anti-slip pads | 6 | 0.5 mm silicone sheet or round rubber bumpons | Any |
| Tether | 6 | Small zip ties | Any |

## Consumables

| Part | Qty | Spec |
|---|---|---|
| Silicone sealant | 1 tube | 100% aquarium-safe silicone |
| Epoxy | 1 syringe | 5-minute two-part, for the magnet pockets only |

## Optional

| Part | Qty | Notes | Source |
|---|---|---|---|
| IR LED board | 2 (+1) | For the spiders only. Needs its own mount 3-5 cm from the lens (**not modelled yet**). 850 nm. | [Waveshare IR LED Board (B)](https://robotshop.com/en/infrared-led-board-rpi-camera.html), 3 W with photoresistor, via RobotShop. Or [Electrokit 12-LED IR ring](https://www.electrokit.com/en/led-ring-for-raspberry-pi-kamera-ir-leds), 5 V with enable pin and PWM. Adafruit's [850 nm IR modules](https://thepihut.com/products/850nm-ir-led-modules) are 3.3 V, so they need a converter: skip. |
| Calipers | 1 | Only needed for checking printed parts now that the drawing is verified. | any |

## Rough total

About $275 without the IR boards. Cameras $105-115, Pi Zeros $45-60, cables, SD cards and power $60-70, magnets $20-30, the rest about $45.

## What the search could not settle

- US stock of the Pi Zero 2 W at any shop.
- A stock 21 x 1 mm acrylic disc and a stock 15 x 5 mm N52 disc.
