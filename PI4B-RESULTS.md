# Pi 4B results (2026-10-27)

**Verdict: dead board.** The 5 V input is healthy, but the 3.3 V rail is stuck at about 1.88 V and nothing boots. Not worth more time. No rework suggested.

## Steps done

1. **Power, no SD, nothing attached, known-good USB cable.** Solid red + solid green LEDs, no blink pattern. Abnormal for a 4B.
2. **Voltage (multimeter, board powered, black probe on pin 6 GND).**
   - TP1 reading: about 3.09 V. TP2 not found on the board. TP1 identity unconfirmed, so this reading was set aside.
   - Pin 2 (5 V): 5.09 to 5.1 V. Power input, supply and cable are fine.
   - Pin 17 and pin 1 (3.3 V rail): 1.87 V and 1.878 V, steady to within a millivolt. Rail is held low.
   - One early probe slip on pin 17 made the board "blip" (likely a momentary short to a neighbour). Redone with clip-on connectors, no further blips.
3. **Thermal camera, board powered 15 to 30 s.** Nothing hotter than the rest of the board. No hard short.
4. **Recovery SD (Raspberry Pi Imager, Bootloader, SD Card Boot), only card inserted.** Solid red + solid green, same as before. (Which HDMI ports were tried was not recorded.)

## Not done

- Serial test: skipped. With the 3.3 V rail at 1.88 V the SoC is not running, so there is nothing to capture.
- Visual inspection photos: not sent.

## Conclusion

Power in is good, 3.3 V rail is bad, nothing is hot, and the bootloader recovery card does nothing. Most likely a dead PMIC (or a rail fault) on the board. The creeperCam project does not depend on it and runs on the 3B+.
