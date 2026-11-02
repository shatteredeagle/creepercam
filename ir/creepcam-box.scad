// CreepCam box: Pi 3B+ + MOSFET perfboard + two 20 mm IR LED stars in one printed enclosure.
// The back face sticks to the outside of the acrylic crib (VHB); the LEDs shine through the wall.
// The camera ribbon leaves through the slot on the bottom edge and goes in through a vent hole.
// DRAFT v1 2026-10-27: nothing printed yet, check every opening against the real parts.
//
//   openscad -D 'part="body"' -o creepcam-body.stl creepcam-box.scad
//   openscad -D 'part="lid"'  -o creepcam-lid.stl  creepcam-box.scad
// part = "body" | "lid" | "both" (assembled preview, lid lifted)

part = "both";

$fn = 48;

// --- Raspberry Pi 3B+ (standard orientation: GPIO header along the top long edge) ---
pi_l = 85;  pi_w = 56;  pi_t = 1.4;
hole_x = 3.5; hole_y = 3.5; hole_dx = 58; hole_dy = 49; // M2.5 holes
post_h = 4;               // board standoff height above the floor
comp_h = 17.5;            // tallest part above the PCB (USB/Ethernet stack)
// Edge connectors measured from the board's left edge along the bottom long edge (y = 0)
usb_pwr_x = 10.6;         // micro-USB power
csi_x = 45;               // camera ribbon connector

// --- LED / MOSFET compartment, to the right of the Pi ---
ext_l = 50;               // extra length for the perfboard and the LED stars
star_d = 20.4;            // 20 mm LED star plus clearance
star_recess = 1.8;        // star thickness plus clearance, pocket on the inside of the back plate
led_window_d = 13;        // through hole so the LED dome shines out of the back
star_pitch = 26;          // distance between the two star centres (along y)

// --- Shell ---
wall = 2;
back = 2.4;               // back plate (the face that touches the acrylic)
clr = 0.6;                // clearance around the Pi
in_l = pi_l + clr*2 + ext_l;
in_w = pi_w + clr*2;
in_h = post_h + pi_t + comp_h + 1.5;
out_l = in_l + wall*2; out_w = in_w + wall*2; out_h = in_h + back;
screw_d = 2.6;            // pilot for M3 self-tapping, in the corner posts

// Pi origin inside the cavity (lower-left corner of the board)
px = wall + clr; py = wall + clr; pz = back + post_h;

module corner_posts() {
  for (x = [wall + 3, out_l - wall - 3], y = [wall + 3, out_w - wall - 3])
    translate([x, y, back]) difference() {
      cylinder(d = 7, h = in_h);
      translate([0, 0, in_h - 10]) cylinder(d = screw_d, h = 11);
    }
}

module pi_posts() {
  for (x = [hole_x, hole_x + hole_dx], y = [hole_y, hole_y + hole_dy])
    translate([px + x, py + y, back]) {
      cylinder(d = 5.5, h = post_h);
      cylinder(d = 2.3, h = post_h + pi_t + 0.8); // pin through the Pi's mounting hole
    }
}

module star_pockets(cut = true) {
  sx = wall + clr + pi_l + clr + ext_l/2;       // compartment centre line
  sy0 = out_w/2 - star_pitch/2;
  for (i = [0, 1]) translate([sx, sy0 + i*star_pitch, 0]) {
    translate([0, 0, -0.01]) cylinder(d = led_window_d, h = back + 0.02);
    translate([0, 0, back - star_recess]) cylinder(d = star_d, h = star_recess + 0.01);
    // wire notch from each star toward the perfboard side
    translate([-star_d/2 - 4, -1.5, back - star_recess]) cube([star_d/2 + 4, 3, star_recess + 0.01]);
  }
}

module perfboard_posts() {
  // 30 x 20 mm perfboard standing on four small posts in the compartment, clear of the stars
  x0 = wall + clr + pi_l + clr + 3;
  y0 = wall + 3;
  for (dx = [0, 26], dy = [0, 16])
    translate([x0 + dx, y0 + dy, back]) cylinder(d = 4, h = 4);
}

module body() {
  difference() {
    union() {
      difference() {
        cube([out_l, out_w, out_h]);
        translate([wall, wall, back]) cube([in_l, in_w, out_h]);
      }
      corner_posts();
      pi_posts();
      perfboard_posts();
    }
    star_pockets();
    // micro-USB power opening, bottom long edge
    translate([px + usb_pwr_x - 6.5, -0.1, pz + pi_t - 0.5]) cube([13, wall + 0.2 + clr, 7.5]);
    // camera ribbon slot, bottom long edge (22 mm wide FFC, 3 mm tall, near the PCB top)
    translate([px + csi_x - 12, -0.1, pz + pi_t - 0.5]) cube([24, wall + 0.2 + clr, 4]);
    // vent slots in the top part of the left short wall (SD card side, nothing plugged there)
    for (i = [0:3]) translate([-0.1, wall + 8 + i*10, pz + 2]) cube([wall + 0.2, 4, 12]);
    // pass-through hole for the USB side of the Pi: Ethernet/USB face the compartment, no opening needed
  }
}

module lid() {
  lid_t = 2.4;
  difference() {
    union() {
      cube([out_l, out_w, lid_t]);
      // inner lip that locates the lid in the shell opening
      translate([wall + 0.3, wall + 0.3, lid_t]) difference() {
        cube([in_l - 0.6, in_w - 0.6, 1.6]);
        translate([1.6, 1.6, -0.1]) cube([in_l - 0.6 - 3.2, in_w - 0.6 - 3.2, 1.8]);
      }
    }
    // screw holes over the corner posts
    for (x = [wall + 3, out_l - wall - 3], y = [wall + 3, out_w - wall - 3])
      translate([x, y, -0.1]) {
        cylinder(d = 3.3, h = lid_t + 0.2);
        translate([0, 0, lid_t - 1.4]) cylinder(d1 = 3.3, d2 = 6, h = 1.5);
      }
    // vent slots over the Pi
    for (i = [0:6]) translate([wall + 8 + i*9, wall + 8, -0.1]) cube([3, in_w - 16, lid_t + 0.2]);
  }
}

if (part == "body") body();
else if (part == "lid") lid();
else {
  body();
  translate([0, 0, out_h + 12]) lid();
  // Pi ghost for fit-checking in the preview
  %translate([px, py, pz]) cube([pi_l, pi_w, pi_t]);
}

echo(str("outer size ", out_l, " x ", out_w, " x ", out_h, " mm; body + lid"));
