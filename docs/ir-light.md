---
title: IR light
---

# IR light

Two ways to light the enclosure at night for the NoIR camera: an LED strip on a dimmer (what runs now) and a home-built Pi-driven driver.

The camera sees 850 nm light, which most animals do not.

## What runs now: LED strip on a Shelly dimmer

- A 12 V 850 nm IR LED strip on its own power supply, outside the enclosure.
- A Shelly Plus RGBW PM drives it: strip + to V+, strip - to output O1, device profile "Lights".
- Home Assistant's Shelly integration exposes it as a dimmable light. A tile with toggle and brightness
  sits under the live feed on the enclosure's dashboard tab.
- Not yet built: a night-only automation tied to the enclosure's light cycle.

The strip has its own supply, so none of the LED current goes through the Pi's power input. The strip route needs no current bench test.

## Alternative: Pi-driven driver (designed, not built)

A home-built driver gives Home Assistant a dimmable "IR light" straight from the Pi.

> **Warning:** do not add the load until `vcgencmd get_throttled` reads `0x0` or only a thermal flag.

### Design

One Pi PWM pin drives a logic-level MOSFET that switches two 850 nm LED chips in series. The LEDs mount
**outside** the acrylic crib, angled 30-45 degrees off the lens axis. Clear acrylic passes 850 nm, and
this avoids the glare you get from lights next to the lens.

| Part | Value | Why |
|---|---|---|
| IR LED chips | 2x 850 nm, in series | about 3.0 V total, so a 5 V rail leaves 2 V for the resistor |
| Current resistor | 5.6 ohm, 2 W | about 350 mA; stays under the 500 mA chip maximum across supply and Vf variation |
| MOSFET | IRLZ44N or IRLB8721 | fully on at 3.3 V gate |
| Gate resistor | 220 ohm | limits gate charge current |
| Gate pull-down | 10 kohm | LEDs stay off while the Pi boots |
| 5 V source | supply side, not the Pi's 5 V pin | keeps LED current out of the Pi's input path |

Worst-case resistor dissipation is 0.85 W; the LEDs add about 1 W. Mount the 20 mm LED stars on metal or a
small heatsink with thermal tape.

### Wiring

```
 5 V (supply side) ----+
                  [ 5.6 ohm 2 W ]
                       |
                  LED1 + -> -  LED2 + -> -
                       |
                    MOSFET drain
 GPIO18 (pin 12) -- 220 ohm -- gate -- 10 kohm -- GND
 GND (pin 14) ------ source ---- supply GND (common with the Pi)
```

### Bench test

Run this before the driver goes near the enclosure.

1. Power the LED branch with the Pi off. Put a multimeter in series (mA range) and read the current.
   Target 300-400 mA. Over 450: raise the resistor. Under 250: lower it a little.
2. Look at the LEDs with a phone camera (IR shows as faint purple-white). Never stare at them.
3. The stars and the resistor should be only warm after two minutes.

### Pi side

[`ir/petcam-ir.py`]({{ site.github.repository_url }}/blob/main/ir/petcam-ir.py) publishes a Home Assistant MQTT light (brightness) and drives hardware PWM at
20 kHz, so camera exposures do not band. The service turns the LEDs off if it stops.

```
echo 'dtoverlay=pwm,pin=18,func=2' | sudo tee -a /boot/firmware/config.txt   # then reboot
sudo apt install python3-paho-mqtt
sudo mkdir -p /opt/petcam-ir && sudo cp petcam-ir.py /opt/petcam-ir/
sudo cp petcam-ir.service /etc/systemd/system/
printf 'MQTT_HOST=<broker>\nMQTT_USER=petcam-ir\nMQTT_PASS=<password>\nMAX_PCT=100\n' | sudo tee /etc/petcam-ir.env
sudo chmod 600 /etc/petcam-ir.env
sudo systemctl enable --now petcam-ir
```

In Home Assistant the light appears through MQTT discovery. A night-on, day-off automation is not yet built.

Next: [Build guide](build-guide)
