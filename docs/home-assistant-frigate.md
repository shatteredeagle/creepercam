---
title: Home Assistant and Frigate
---

# Home Assistant and Frigate

How the camera stream is recorded by Frigate and shown in Home Assistant, including the dashboard config and
how to save a clip.

```
Pi (mediamtx) --RTSP--> Frigate (go2rtc restream, motion, recording) --> Home Assistant
                                   |                                    (Frigate integration
                                   +-- recordings on disk                + Advanced Camera Card)
                                   |
                                   +--> highlight reels (next page)
```

## Frigate

Frigate runs as a container on a home server. One camera takes the Pi's RTSP stream through go2rtc, which
lets several consumers share one stream:

- Detect at 1920x1080, 5 fps, with hardware decoding.
- Object detection is off on purpose: the standard models do not know tarantulas, so recording is
  triggered by motion alone.
- Recordings are kept for 14 days. At 4.6 Mbit/s the stream would use about 50 GB a day if recorded
  continuously, so only motion is stored.
- MQTT to Home Assistant through a dedicated broker login.

### Motion tuning

With the Frigate defaults, the motion sensor fired every 1 to 3 minutes and about 15% of the footage was
kept, caused by sensor noise on a static, dark scene. These camera settings fixed it:

| Setting | Before | After |
|---|---|---|
| `threshold` | 30 | 35 |
| `contour_area` | 10 | 40 |
| `improve_contrast` | true | false |

After the change there were no false motion events in 20 minutes, and the animal's real movement still
triggered recording. Two sources of false motion remain: the enclosure light changing colour and the IR light
switching on. The [highlight reels](highlight-reels) filter those out.

## Home Assistant

- **Live picture:** the Pi stream is added as a generic camera (RTSP) for dashboards.
- **Frigate integration** (HACS, `blakeblackshear/frigate-hass-integration`): provides the camera, the motion
  and recording switches, and clip browsing. Point it at your Frigate URL.
- **Advanced Camera Card** (HACS, `dermotduffy/advanced-camera-card`): a viewer for live video, clips,
  snapshots and recordings, with download buttons.

Dashboard config for the Cameras view (panel layout):

```yaml
views:
  - title: Cameras
    path: cameras
    panel: true
    cards:
      - type: custom:advanced-camera-card
        cameras:
          - camera_entity: camera.pet_cam
            frigate:
              camera_name: pet_cam
        view:
          default: recordings
        menu:
          style: outside
          position: bottom
        timeline:
          style: ribbon
```

Replace `pet_cam` with your camera's name.

**Tip:** `view: default: recordings` opens the card on a gallery of recordings, which is easier to browse than
the timeline. The timeline stays one tap away in the card's menu.

## Saving a clip

- **Advanced Camera Card:** open Recordings or Clips, pick the event, and use the download button.
- **Frigate web interface:** open *Review* or *History*, choose *Export* for a time range, then download it
  from the *Exports* page. Exports are kept until you delete them, so retention does not remove them. A single
  detection can also be downloaded from *Explore*.
- **Daily reel:** [Highlight reels](highlight-reels) shows how to get a ready-made video of each day.

Frigate keeps recordings for the configured number of days only, so export anything you want to keep.

Next: [Highlight reels](highlight-reels).
