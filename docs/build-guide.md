---
title: Build guide
---

# Build guide

Step-by-step instructions to replicate a creeperCam, from first boot to a pod running on an enclosure wall.

Order: Pi and stream first (proves the camera), then Home Assistant and Frigate, then print the pod,
then IR. Allow a weekend for the first pod, most of it print time.

## 1. Pi and camera

1. Flash Raspberry Pi OS Lite 64-bit (hostname of your choice, SSH on, Wi-Fi set).
2. With the Pi powered off, plug the camera into the **CSI** port (between HDMI and the audio jack).
3. Use a short, thick, 3 A-rated USB power cable. Weak cables cause brown-outs that look like a dead board.
4. Boot and run `bash pi-setup.sh`, then `rpicam-hello --list-cameras`.
5. Replace `/etc/mediamtx/mediamtx.yml` with the config in [Software](software), then
   `sudo systemctl enable --now mediamtx`.
6. Open `rtsp://<pi-host>:8554/cam` in VLC, or deploy the web UI (`bash webui/deploy.sh user@pi-host`).
7. Check that `vcgencmd get_throttled` reads `0x0`.

## 2. Frigate and Home Assistant

1. Run Frigate (Docker) with the camera config in [Home Assistant and Frigate](home-assistant-frigate).
2. Add a Frigate MQTT login in your broker and point Frigate's `mqtt` block at it.
3. Install the Frigate integration and the Advanced Camera Card from HACS.
4. Add the dashboard config from that page.
5. Wave a hand in front of the camera and confirm a clip appears. If motion fires constantly, tune `motion.threshold`.

## 3. Print the pod

1. Render or download `cap-v5.stl` and `body-v5.stl` (or `body-v5-flat.stl` for a tape mount).
2. Print in ASA or PETG, 0.2 mm layers, 5+ perimeters. Print the **cap first** and check it fits the bare camera board.
3. **Measure your own camera** (PCB size, lens height, lens offset, connector). Clones differ from the
   official drawing. Put your numbers in `pod.scad` and re-render. [Hardware](hardware) lists what was measured on the clone used here.

## 4. Assemble the pod

1. Bed the 25 mm glass tile into the cap recess with aquarium silicone and let it cure fully.
2. Lay 1.5 mm silicone cord in the body rim groove.
3. Seat the camera on the body's posts with the lens toward the window and the ribbon through the top slot.
4. Add a 1 g desiccant sachet behind the board.
5. Fit the cap and drive four M2.5 x 6 self-tapping screws.
6. Seal the ribbon slot with silicone.
7. Press the magnets into the plate pockets (all the same way up) and pot them with 5-minute epoxy.
8. Put matching outside magnets (opposite polarity) on the other side of the wall and tether the pod to a vent hole.

> **Warning:** never use acetone, solvent glue or isopropyl-heavy cleaner on acrylic.

## 5. Focus and test

1. Open the live view. If it hunts, set `rpiCameraAfRange: macro`, or lock focus manually (see [Software](software)).
2. Leave it running for a few days and check for fogging behind the window, that the magnets hold, and that the night footage is usable.

## 6. IR light (optional)

See [IR light](ir-light). The strip-and-Shelly route needs no current bench test; the Pi-driven route does.

Next: [Parts list](bom)
