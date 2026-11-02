---
title: Hardware
---

# Hardware

The parts of a creeperCam, why each was chosen, and the measurements of the camera clone the pod is built around.

## The animals and enclosures

| Animal | Enclosure | Camera mount |
|---|---|---|
| Brazilian black tarantula (*Grammostola pulchra*), terrestrial, 60-70% humidity | [Tarantula Cribs Large Slider Crib Pro](https://tarantulacribs.com/products/large-slider-crib-pro-clear-bottom), 12 x 8 x 8 in, clear acrylic, sliding magnetic lid | Magnet to the inside of the upper back wall; ribbon out a top vent hole |
| Mexican red knee tarantula (*Brachypelma hamorii*), terrestrial burrower, 50-60% humidity | Same crib | Same |
| Surinam horned frog (*Ceratophrys cornuta*), buried ambusher, high humidity | [Exo Terra 12 x 12 x 12 Pro](https://www.pangeareptile.com/products/exo-terra-12x12x12-pro-terrarium-x-small-wide), glass, screen top | Magnet to the inside of the side glass; ribbon out the rear lid cutout |

The frog enclosure is tight for an adult (4-6 in) and fine for a juvenile.

Not yet verified: the Exo Terra lid cutout details.

## Design decisions

- **Camera inside, not through the wall.** Shooting through acrylic or glass gives glare, and IR
  bounces off both. A pod inside avoids that and works for both materials.
- **Only the lens end is in the humid air.** The Pi and its power stay outside. The pod is gasketed
  and holds a desiccant sachet.
- **Magnets, not tape or hooks.** Rare-earth discs hold the pod through the wall and let you
  reposition it. The inside magnets sit behind a 0.6 mm printed skin, so they never touch humid air
  or the animal. A flat variant for Command Strips also exists.
- **Magnets stay 30+ mm from the lens.** The Camera Module 3 focuses with a voice-coil motor that a
  strong magnet can disturb. The model prints the distance when it renders (39.2 mm for the current design).
- **IR lives outside the enclosure.** Clear acrylic passes 850 nm (a TV remote lit the scene through
  the wall), so the LEDs mount outside, angled 30-45 degrees off the lens axis, which avoids glare.

> **Warning:** never use acetone, solvent glue or isopropyl-heavy cleaner on acrylic. It crazes the
> surface. Use silicone or VHB tape only.

## Computer

| | Used now | Target |
|---|---|---|
| Board | Raspberry Pi 3B+ (bought used) | Pi Zero 2 W, one per pod |
| OS | Raspberry Pi OS Lite 64-bit | same |
| Encoder | Hardware H.264, 1080p15 | same |

The 3B+ is the test unit. It sits outside the tarantula enclosure with the camera ribbon routed
through a vent. A Zero 2 W draws about a quarter of the power and fits a much smaller housing, but
stock and price were poor when this was built.

> **Warning:** power matters more than expected. A 3B+ on weak USB cables brown-out looped (solid red
> and green LEDs, `vcgencmd get_throttled` = `0x50005`). After switching to a better supply it reads
> `0x80008`: no under-voltage, only a soft temperature limit under load. See
> [Lessons learned](lessons-learned).

## Camera

An Amazon "IMX708 Wide NoIR" 120-degree module (a clone of the official Camera Module 3 Wide NoIR),
about $33. Measured on the clone with calipers:

| Measurement | Value |
|---|---|
| PCB | 24.93 x 24.12 mm, 1.12 mm thick (official board: 25 x 23.862) |
| Lens square | 10.84 mm; barrel 7.10 mm |
| Lens front above PCB | 7.21 mm (the official drawing's 8.3 mm figure was too high for this clone) |
| Lens position | 2.25 mm toward the **ribbon-connector edge** (the drawing had it on the opposite edge) |
| Front-side chips | up to 1.66 mm tall |
| FFC connector (back) | 22 mm wide, flush with the ribbon edge, 5.75 mm deep |
| Field of view | 120 deg diagonal, 102 horizontal, 67 vertical |

How it behaves:

- Reads module ID `0x0000`, normal for a clone. libcamera still drives it with the stock
  `imx708_wide_noir` tuning file.
- The autofocus motor works. Low-light performance is good.
- NoIR confirmed: no IR-cut filter, and an IR remote lit the scene through the acrylic wall.

> **Warning:** plug it into the CSI port (between HDMI and the audio jack), not the DSI display port.

## Magnets, window and fasteners

- **Magnets:** N52 discs about 15 x 5 mm (two inside the pod, two outside the wall, opposite
  polarity). Check grade and size on the listing; set `mag_d` and `mag_t` in `pod.scad` to match.
- **Window:** a 25 mm round flat glass tile, 3.5 mm thick, bedded in silicone. No stock 21 x 1 mm
  acrylic disc exists, so the design uses a stock glass size.
- **Gasket:** 1.5 mm silicone cord in the body rim groove.
- **Screws:** M2.5 x 6 self-tapping stainless.

## IR illuminator

A 12 V 850 nm LED strip on its own supply, dimmed by a Shelly Plus RGBW PM and controlled from Home
Assistant. A home-built Pi-driven design (two LED chips, resistor, MOSFET) is documented as an
alternative. See [IR light](ir-light).

## Debug gear

A Waveshare FT232 USB-to-serial cable (3.3 V) reads the Pi boot console, which helps when debugging brown-outs.

Next: [Enclosures and printed parts](enclosures-and-stls)
