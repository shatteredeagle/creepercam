# Petcam IR light (home-built)

One Pi GPIO pin drives a logic-level MOSFET that switches two 850 nm IR LED chips (Vrabocry 10-pack,
Amazon B0C77JCTXP, 1.4-1.6 V each, 400-500 mA max). Home Assistant gets an `IR light` with brightness.
The LEDs mount OUTSIDE the acrylic crib (clear acrylic passes 850 nm; a TV remote lit the camera through it).

Status 2026-10-27: designed, not built or deployed. Do NOT add the load until the Pi reports
`vcgencmd get_throttled` = `0x0` (it still shows 0x50005 on the Pi 3B+ `petcam-test`).

## Parts per cube

| Part | Value | Why |
|---|---|---|
| IR LED chips | 2x, wired in series | about 3.0 V total, so a 5 V rail leaves 2 V for the resistor |
| Current resistor | **5.6 ohm, 2 W** (1 W works, 2 W runs cooler) | I = (5.0 - 3.0 - 0.05) / 5.6 = about 350 mA; 310 mA at Vf 3.2 V, 390 mA at Vf 2.8 V, 430 mA if the supply reads 5.25 V. All below the 500 mA maximum |
| MOSFET | logic-level N-channel, through-hole: IRLZ44N or IRLB8721 | fully on at 3.3 V gate, 0.35 A is trivial for it |
| Gate resistor | 220 ohm, GPIO to gate | limits the gate charge current |
| Gate pull-down | 10 kohm, gate to GND | LEDs stay off while the Pi boots or the pin floats |
| 5 V source | the supply side (split cable or terminal block before the Pi), NOT the Pi's 5 V pin | do not pull LED current through the Pi's input path while that path is suspect |

Resistor dissipation worst case: 0.39 A squared x 5.6 = 0.85 W. LEDs together about 1 W: stick the
20 mm stars to something metal or a small heatsink with thermal tape.
One chip instead of two: use 10 ohm 2 W (I = about 345 mA), the resistor then burns about 1.2 W.

## Wiring

```
 5 V (supply side) ----+--------------------------+
                       |                          |
                  [ 5.6 ohm 2 W ]                 |  (Pi gets its own 5 V as usual)
                       |
                  LED1 + -> -  LED2 + -> -
                       |
                    MOSFET drain
 GPIO18 (header pin 12) -- 220 ohm -- gate
                              |
                           10 kohm
                              |
 GND (header pin 14) ------ source ---- supply GND  (common ground with the Pi)
```

MOSFET pins (IRLZ44N, flat side facing you, legs down): gate, drain, source left to right.
Check polarity of each LED star (+ and - are printed on the board) and connect LED1 out to LED2 in.

## Bench test BEFORE it goes near the cube

1. Power the LED branch from a bench supply or the real 5 V supply with the Pi OFF and the gate pulled to 3.3 V
   by hand (or just run the LED branch directly, no MOSFET, for one second).
2. Put a multimeter in series (mA range, 10 A jack if it has one) and read the current. Target 300-400 mA.
   Over 450 mA: raise the resistor. Under 250 mA: lower it a little.
3. Look at the LEDs with the phone camera (IR shows as faint purple-white). Never stare at them.
4. Check the LED stars and the resistor are only warm after 2 minutes.

## Pi setup

```
# on the Pi (petcam-test)
echo 'dtoverlay=pwm,pin=18,func=2' | sudo tee -a /boot/firmware/config.txt   # then reboot
sudo apt install python3-paho-mqtt
sudo mkdir -p /opt/petcam-ir && sudo cp petcam-ir.py /opt/petcam-ir/
sudo cp petcam-ir.service /etc/systemd/system/
printf 'MQTT_HOST=<broker>\nMQTT_USER=petcam-ir\nMQTT_PASS=...\nMAX_PCT=100\n' | sudo tee /etc/petcam-ir.env
sudo chmod 600 /etc/petcam-ir.env
sudo systemctl enable --now petcam-ir
```

The Mosquitto login `petcam-ir` still has to be added in the HA Mosquitto add-on options (keep teams-mqtt
and frigate). PWM runs at 20 kHz so camera exposures do not band. Dimming steps are 1-255; the
service turns the LEDs off if it stops.

## HA side

The light appears by MQTT discovery as `light.petcam_ir_ir_light` (check the real entity id). Planned
automation: on when `sensor.daylight_phase` is night, off otherwise; also a tile on the camera dashboard.
