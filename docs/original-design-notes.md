---
title: Original design notes
---

# Original design notes

The project's first design plan, kept for reference. The other pages supersede it where they differ; the changes are listed at the end.

## Concept

Sealed, magnet-mounted camera pods for three terrarium enclosures. One Pi Zero 2 W and one
Camera Module 3 Wide NoIR per enclosure. The Pi stays outside; only the camera sits in a printed
pod inside, joined by a ribbon cable.

## The animals and enclosures

| Animal | Enclosure | Mount |
|---|---|---|
| Brazilian black tarantula (*Grammostola pulchra*), terrestrial, about 60-70% humidity | [Tarantula Cribs Large Slider Crib Pro](https://tarantulacribs.com/products/large-slider-crib-pro-clear-bottom), 12 x 8 x 8 in, acrylic, sliding magnetic lid | Magnet to the inside of the upper back wall; ribbon out a top vent hole |
| Mexican red knee tarantula (*Brachypelma hamorii*), terrestrial burrower, about 50-60% humidity | Same crib | Same |
| Surinam horned frog (*Ceratophrys cornuta*), buried ambusher, high humidity | [Exo Terra 12 x 12 x 12 Pro](https://www.pangeareptile.com/products/exo-terra-12x12x12-pro-terrarium-x-small-wide), glass, screen top (lid details not verified) | Magnet to the inside of the side glass, or clamp to the screen with two magnets; ribbon out the rear lid cutout |

## Design decisions

- **Camera inside, not through the wall.** Shooting through acrylic or glass gives glare, and
  IR bounces off both. A pod inside avoids that and works for both materials.
- **Only the lens end is in the humid air.** The Pi and its power stay outside. The frog pod is
  fully gasketed and has a desiccant sachet; the spider pods use the same part.
- **Magnets, not tape or hooks.** Rare-earth discs hold the pod through the wall and let you
  reposition it. The inside magnets sit behind a 0.6 mm printed skin, so they never touch humid
  air or the animal.
- **Magnets stay at least 30 mm from the lens.** Camera Module 3 has a voice-coil autofocus that a
  strong magnet can disturb. The model reports the distance on render (34 mm at this stage).
- **The crib lid slides**, so the pod is on the wall, not the lid.
- **IR is fine inside a 12" cube.** A 0.5-2 W LED board adds well under a degree of heat. The real
  problem is glare: keep the LEDs 3-5 cm from the lens, angled off the glass. Skip IR for the frog.
- **Never use acetone, solvent glue or isopropyl-heavy cleaner on the acrylic cribs.** It crazes
  the surface. Silicone or VHB only.

## Camera facts from the official drawing

From the official Wide mechanical drawing (RP-008155-DS-1):

- PCB 25 x 23.862 mm, 1.12 mm thick, M2.2 holes 2.0 mm from the edges (rows at 2.0 and 14.5 mm).
- Lens centre is 2.47 mm off the PCB centre, on the edge opposite the FFC connector.
- Lens front stands 8.3 mm above the PCB. The FFC connector adds 2.75 mm on the back (12 mm total).
- 120 deg diagonal, 102 deg horizontal, 67 deg vertical.

Measurements of the clone actually used differ; see [Hardware](hardware).

## Files

| File | What |
|---|---|
| `pod.scad` | Parametric source (OpenSCAD) |
| `body.stl`, `cap.stl` | Print-ready parts |
| `assembly.stl`, `preview.png` | For viewing only |
| `BOM.md` | Parts, sources, prices |

Render: `openscad -D 'part="body"' -o body.stl pod.scad` (also `cap`, `assembly`).

Key parameters in `pod.scad`:

| Parameter | Default | Notes |
|---|---|---|
| `tilt` | 40 | Lens pitch down from the wall normal. Up to 45 prints without supports. |
| `mount` | `"magnet"` | `"flat"` leaves out the pockets (for tape). |
| `exit_side` | `"top"` | Ribbon edge; the lens-offset edge is the opposite one. |
| `mag_d`, `mag_t` | 15, 5 | Match the discs you buy. |
| `win_d`, `disc_d` | 17, 21 | Aperture and window disc. |
| `mag_extra` | 9 | Extra plate length that keeps the magnets 30+ mm from the lens. |

Output at this stage: pod 31.9 x 30.8 x 22.7 mm, plate 38 x 81.5 x 7 mm, lens 25 mm off the wall.

## Print

- ASA (best for humidity) or PETG. Body prints with its wall face on the bed; cap prints with
  its outer face down. Both print support-free at 40 deg tilt.
- 0.2 mm layers, 5+ perimeters so the walls are watertight. Coat the body with epoxy or
  acetone-smooth the ASA (not near the acrylic cribs) if the layer lines weep.
- Print the **cap first** (about 20 minutes) and test-fit the bare camera board and window disc.

## Assemble (per pod)

1. Press the window disc into the cap's recess and run a bead of aquarium silicone around its edge.
   Let it cure fully.
2. Drop the 1.5 mm O-ring cord into the body rim groove.
3. Connect the camera to the Zero cable, thread the ribbon through the top slot, and seat the PCB
   on the four corner posts (lens toward the window).
4. Add the desiccant sachet behind the PCB.
5. Fit the cap and drive four M2.5 x 6 self-tapping screws.
6. Seal the ribbon slot with silicone.
7. Insert the magnets into the plate pockets (all the same way up), pot them with epoxy, and let it cure.
8. Stick the anti-slip pad on the wall face.
9. Place the outside magnets (opposite polarity) on the other side of the wall, and tether the pod to a vent hole.

## Software plan

Not yet verified at the time of writing; the [Software](software) page documents what was built.

- Raspberry Pi OS Lite on each Zero, camera enabled.
- MediaMTX with its Raspberry Pi camera source gives an RTSP stream. Feed it to Home Assistant
  (go2rtc or Frigate). Zero 2 W has a hardware H.264 encoder up to 1080p.
- The frog mostly sits still: motion-triggered clips catch feeding strikes better than 24/7 streaming.
- Use hostnames, not fixed IPs.

## What changed since

- The window is a 25 mm glass tile, not a 21 mm acrylic disc, and the lens offset sign was corrected. See [Enclosures and printed parts](enclosures-and-stls).
- The hook mount for the Exo Terra screen top was dropped in favour of the magnet mount.
- Not yet verified: an IR LED bracket (850 nm, 3-5 cm from the lens) was never modelled; IR now comes from an LED strip outside the enclosure ([IR light](ir-light)).
