---
title: Lessons learned
---

# Lessons learned

What went wrong while building creeperCam, grouped by area, so yours goes better.

## Power

- **A weak USB cable looks like a dead board.** A Pi 3B+ showed solid red and solid green LEDs and
  would not boot, then recovered once the cable and supply were fixed. Check `vcgencmd get_throttled`
  first. `0x50005` means under-voltage now and since boot.

## Camera

- **Clone cameras report module ID `0x0000`.** That is normal, and libcamera still works with the stock tuning file.
- **Measure the real board.** The official drawing put the lens on the edge opposite the ribbon
  connector and 8.3 mm above the PCB. The clone's lens is toward the connector edge and 7.21 mm up. The
  first test cap had its window 4.5 mm off because of the sign error.
- **Check the back of the board too.** The first printed body landed two seat posts on the FFC
  connector. Measure the connector before placing posts.
- **A camera plugged into the DSI port is not detected.** Use the CSI port.

## Optics

- **Magnets near the lens are a real risk.** The autofocus is a voice coil. Keep magnets 30+ mm away; the model checks it.
- **Autofocus hunts in static, dark scenes.** Limit its range (or lock it) and consider manual focus for IR work.
- **IR passes through clear acrylic.** That lets the LEDs live outside the enclosure, which avoids glare and keeps heat and wiring out of the habitat.

## Software and integration

- **Settings changed in the web UI are lost on restart.** Flip the image upside down in the UI and a reboot flips it back. Persist what matters in `mediamtx.yml`.
- **Night sensor noise causes false motion events.** Raise the motion threshold and contour area, turn off contrast improvement, and add IR light.
- **Home Assistant's Frigate integration entry cannot be edited in place.** It has to be re-created when the URL changes.

## Process

- **Print the cap first** and test-fit the bare board before printing the body.
- **Keep every SCAD revision** (`pod.scad.bakN`). The design history on [Enclosures and printed parts](enclosures-and-stls) was only recoverable because of them.

## Detection and clips

- **Light changes count as motion.** When the enclosure light cycles between colours or the IR light switches on, the camera's motion detector fires even though nothing moved, so motion-only recordings contain many empty clips.
- **Frigate's clips have a variable frame rate.** Cutting and joining them with a plain concat produced a video five times too long until the cuts were re-encoded at a constant 15 fps.
- **CLIP image models centre-crop to a square.** Feeding a 16:9 frame whole hides a spider at the left or right edge; splitting the frame into three full-height squares fixed it.
- **Zoomed crops of bedding score as spiders.** Close-up crops of coconut-fibre substrate matched "a hairy spider" with scores above 0.9, so a zoom pass for small spiders caused false hits and was left off.

Next: [Gallery](gallery)
