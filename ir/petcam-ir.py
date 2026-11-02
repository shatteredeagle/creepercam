#!/usr/bin/env python3
"""IR light for a petcam pod: Home Assistant MQTT light (brightness) on a Pi hardware-PWM pin.

GPIO18 (PWM0) -> gate resistor -> logic-level MOSFET -> IR LEDs (see README.md).
Needs `dtoverlay=pwm,pin=18,func=2` in /boot/firmware/config.txt and a reboot.
Config comes from /etc/petcam-ir.env (MQTT_HOST, MQTT_USER, MQTT_PASS, optional NAME, MAX_PCT).
"""
import json, os, signal, sys, time
import paho.mqtt.client as mqtt

NAME = os.environ.get("NAME", "petcam_ir")
HOST = os.environ["MQTT_HOST"]
PORT = int(os.environ.get("MQTT_PORT", "1883"))
MAX_PCT = float(os.environ.get("MAX_PCT", "100"))  # hard cap on duty; the resistor already limits current
FREQ_HZ = 20000  # well above camera frame/exposure rates, so no banding
CHIP = "/sys/class/pwm/pwmchip0"
PWM = f"{CHIP}/pwm0"
STATE_FILE = f"/var/lib/{NAME}.json"
BASE = f"homeassistant/light/{NAME}"
STATE_T, CMD_T, AVAIL_T = f"{NAME}/state", f"{NAME}/set", f"{NAME}/availability"

def w(path, val):
    with open(path, "w") as f:
        f.write(str(val))

def pwm_init():
    if not os.path.isdir(PWM):
        w(f"{CHIP}/export", 0)
        time.sleep(0.3)
    w(f"{PWM}/enable", 0)
    w(f"{PWM}/period", int(1e9 / FREQ_HZ))
    w(f"{PWM}/duty_cycle", 0)
    w(f"{PWM}/enable", 1)

def set_duty(brightness):  # 0..255 -> duty
    pct = min(MAX_PCT, brightness / 255 * 100)
    w(f"{PWM}/duty_cycle", int(int(1e9 / FREQ_HZ) * pct / 100))

state = {"state": "OFF", "brightness": 128}
try:
    state.update(json.load(open(STATE_FILE)))
except Exception:
    pass

def apply(client=None):
    set_duty(state["brightness"] if state["state"] == "ON" else 0)
    try:
        json.dump(state, open(STATE_FILE, "w"))
    except OSError:
        pass
    if client:
        client.publish(STATE_T, json.dumps(state), retain=True)

def on_connect(client, *_):
    cfg = {
        "name": "IR light", "unique_id": NAME, "schema": "json", "brightness": True,
        "supported_color_modes": ["brightness"], "state_topic": STATE_T,
        "command_topic": CMD_T, "availability_topic": AVAIL_T,
        "device": {"identifiers": [NAME], "name": NAME, "manufacturer": "DIY"},
    }
    client.publish(f"{BASE}/config", json.dumps(cfg), retain=True)
    client.publish(AVAIL_T, "online", retain=True)
    client.subscribe(CMD_T)
    apply(client)

def on_message(client, _u, msg):
    try:
        cmd = json.loads(msg.payload)
    except ValueError:
        return
    if "brightness" in cmd:
        state["brightness"] = max(1, min(255, int(cmd["brightness"])))
    if cmd.get("state") in ("ON", "OFF"):
        state["state"] = cmd["state"]
    apply(client)

def main():
    pwm_init()
    apply()
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:  # paho-mqtt 1.x
        client = mqtt.Client()
    client.username_pw_set(os.environ["MQTT_USER"], os.environ["MQTT_PASS"])
    client.will_set(AVAIL_T, "offline", retain=True)
    client.on_connect, client.on_message = on_connect, on_message

    def stop(*_):
        set_duty(0)  # LEDs off if the service stops
        sys.exit(0)
    signal.signal(signal.SIGTERM, stop)
    client.connect(HOST, PORT, 60)
    client.loop_forever(retry_first_connection=True)

if __name__ == "__main__":
    main()
