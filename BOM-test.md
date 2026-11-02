# Pet camera pod: one-pod test kit

Goal: build one pod, put it on a spider, and judge the night footage before buying the other two.
Full three-pod list and sources: `BOM.md`. Prices are rough US estimates (checked 2026-10-26); check stock before ordering.

## Electronics

| Part | Qty | Spec | Source | Price |
|---|---|---|---|---|
| Camera | 1 | IMX708 Wide NoIR 120 deg module, ships with a 15-22 pin and a 15-15 pin 150 mm cable | [Amazon listing](https://www.amazon.com/dp/B0GYW6YZRC) about $33. Fallback: official board, [Micro Center](https://www.microcenter.com/product/662019/raspberry-pi-camera-3-wide-noir) $34.99 or [Adafruit](https://www.adafruit.com/product/5660) $38.50 | $33 |
| Computer | 1 | Pi Zero 2 W **with headers** (the IR board may need GPIO power or an enable pin) | [Adafruit #6008](https://www.adafruit.com/product/6008), [PiShop](https://www.pishop.us/product/raspberry-pi-zero-2w-with-headers/) | $17-22 |
| Camera cable | 0 | Included with the camera (15-22 pin, 150 mm). A longer 30 cm cable is only a backup if the Pi sits far from the enclosure. | iUniker 16 + 30 cm pack on Amazon, or Pimoroni | $0 |
| microSD | 1 | 32 GB high-endurance | any | $8 |
| Power | 1 | 5 V 2.5 A micro-USB | any | $8 |
| IR light | 1 | 850 nm IR LED board | [Waveshare IR LED Board (B)](https://robotshop.com/en/infrared-led-board-rpi-camera.html) or [Electrokit 12-LED ring](https://www.electrokit.com/en/led-ring-for-raspberry-pi-kamera-ir-leds). **No mount in the model yet**: for the test, hold it 3-5 cm from the lens with tape. | $12-25 |

## Pod hardware

| Part | Qty | Spec |
|---|---|---|
| Screws | 4 (+2 spare) | M2.5 x 6 mm self-tapping, A4/316 stainless |
| Gasket | 1 short length | 1.5 mm silicone O-ring cord, about 120 mm: [McMaster 1187N11](https://www.mcmaster.com/products/silicone-o-ring-cord-stock/) |
| Window | 2 | 21 x 1 mm clear acrylic disc (1 spare). **No stock source found**: custom laser-cut, or tell me and I'll change the model to a stock size. |
| Desiccant | 1 | 1 g rechargeable silica gel sachet |
| Printed parts | 1 body + 1 cap | ASA or PETG, about 70 g |

## Magnets and mounting

| Part | Qty | Spec |
|---|---|---|
| Inside magnets | 2 (+1 spare) | N52 disc, about 15 x 5 mm. 15 mm isn't a stock K&J size: use the nearest [K&J N52 size](https://www.kjmagnetics.com/products/grade-n52-magnets?filter=56,90), then set `mag_d` and `mag_t` in `pod.scad` |
| Outside magnets | 2 | Same size, epoxy-coated if you can |
| Anti-slip pad | 2 | Silicone sheet or bumpons |
| Tether | 2 | Small zip ties |

## Consumables

- 1 tube of 100% aquarium-safe silicone
- 1 syringe of 5-minute epoxy (magnet pockets only)

## Amazon links (searched 2026-10-26; confirm price, stock and the exact variant on each page)

| Part | Amazon listing | Note |
|---|---|---|
| Camera | [IMX708 Wide NoIR 120 deg module](https://www.amazon.com/dp/B0GYW6YZRC) | About $33. Board 24.9 x 24.0 mm, lens block 10.8 mm, matches the official drawing. Includes 15-22 and 15-15 pin 150 mm cables. Official board as fallback: [Amazon](https://www.amazon.com/Raspberry-Pi-Camera-Module-NoIR/dp/B0BRY6VLR6). |
| Pi Zero 2 W | [Pi Zero 2 W with pre-soldered header](https://www.amazon.com/Raspberry-Pre-Soldered-Quad-Core-Cortex-A53-Bluetooth/dp/B09LTCF8DD) | Third-party seller, colored header. Adafruit #6008 is the safer source. |
| Camera cable | included with the camera | Backup: [iUniker 16 cm + 30 cm pack](https://www.amazon.com/Camera-Cable-iUniker-Raspberry-Ribbon/dp/B07H8Z4XLL). |
| microSD | [SanDisk High Endurance 32 GB](https://www.amazon.com/SanDisk-Endurance-microSDHC-Adapter-Monitoring/dp/B07P14QHB7) | |
| Power | [PepperTech 5 V 2.5 A micro-USB](https://www.amazon.com/PepperTech-Digital-Micro-USB-Raspberry-Pi-Black/dp/B09KX7859C) | |
| IR light | [DORHEA 3 W 850 nm IR board, 2-pack](https://www.amazon.com/Infrared-Illuminator-Adjustable-Resistor-Raspberry/dp/B07FM6LL3V) | Has a photoresistor. Listings warn the 3 W LED runs hot. Power wiring unverified. |
| Screws | [uxcell M2.5 x 6 self-tapping, 50 pcs](https://www.amazon.com/uxcell-50pcs-Stainless-Tapping-Screws/dp/B01M0P074Q) | Stainless, grade not stated (probably 304, not 316). Fine for the spider test. |
| Silicone cord | [Petabo 1 m, 1.5 mm solid silicone](https://www.amazon.com/Silicone-Diameter-1mm-20mm-Rubber-Gasket/dp/B0DMQRQ9RP) | Pick the 1.5 mm option. |
| Window disc | none found | No 20-22 mm x 1 mm disc on Amazon. |
| Desiccant | [Vbeijll 1 g x100, indicating, rechargeable](https://www.amazon.com/Vbeijll-Premium-Desiccant-Packets-Indicating/dp/B0DP6MPG4Y) | |
| Magnets | [15 x 5 mm NdFeB discs](https://www.amazon.com/clp/B0C5V3GZYM) | Grade not stated, so not confirmed N52. Check the listing before buying. |
| Silicone sealant | [Aqueon 100% silicone, 3 oz](https://www.amazon.com/Aqueon-100165003-Silicone-3-oz/dp/B0002ASD2K) | Small tube, enough for the test. |
| Epoxy | [Gorilla 5-minute epoxy syringe](https://www.amazon.com/Gorilla-Epoxy-Minute-ounce-Syringe/dp/B01MDS31JX) | Pack of 4, more than you need. |

## Rough total

About $145. The camera, Zero, SD card and power supply alone are about $70.

## Before you order

1. Pick the window-disc option (custom acrylic, or a stock size and I change the model).
2. Pick the magnet size so `mag_d` matches.
3. When the camera arrives, check the lens height above the PCB (the pod assumes 8.3 mm, with 1.5 mm of window gap) and that it is truly NoIR (no green IR-cut glass in the lens).

## What the test should tell you

- Does the Module 3 Wide NoIR give usable night footage with the IR board on a spider enclosure? If not, the next step is an IMX462 "starlight" camera for the spider pods, which means re-measuring the pod.
- Does the pod stay sealed over a few days in the enclosure (no fogging, no moisture behind the window)?
- Does the magnet mount hold through the acrylic wall (the crib walls are about 3x standard thickness)?
