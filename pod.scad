// Sealed camera pod for terrarium monitoring (Raspberry Pi Camera Module 3 Wide).
// Two printed parts: BODY (wedge + camera cavity + magnet plate) and CAP (window).
// Camera dimensions are from the official Wide mechanical drawing (RP-008155-DS-1), verified 2026-10-24.
//
//   part = "assembly" | "body" | "cap"     body/cap are laid out print-ready
//   mount = "magnet" | "flat"              magnet = pockets for N52 discs, flat = VHB tape
//
// World frame for the assembly: wall plane is Z=0, the enclosure interior is +Z, +Y is up.

part = "assembly";
mount = "magnet";
exit_side = "top";      // which pod edge the ribbon leaves from: "top" | "bottom"
tilt = 40;              // lens pitch down from the wall normal, degrees (<=45 prints without supports)

// --- camera board (Camera Module 3 Wide) ---
cam_w = 24.93;          // PCB width, measured on the clone 2026-10-27
cam_d = 24.12;          // PCB height, measured on the clone 2026-10-27 (official drawing: 23.862)
cam_pcb_t = 1.12;
cam_total = 8.33;       // PCB back to lens front: 7.21 lens above PCB (measured on the clone 2026-10-27) + 1.12 PCB (drawing: 12 overall incl. 2.75 FFC connector on the back)
lens_dy = 2.25;          // lens square centre is 2.0-2.45 mm toward the RIBBON-CONNECTOR edge (confirmed by user 2026-10-27): 4.19 from that edge, 8.66 from the far edge, 10.84 square, 0.1 right of centre; the ribbon exits on that same (top) edge

// --- pod shell ---
fit = 0.5;              // clearance around the PCB
wall = 3.2;
floor_t = 2.4;          // rear wall thickness
conn_w = 22;            // FFC connector on the PCB back (measured 2026-10-27): 22 wide, flush with the ribbon-side edge, 5.75 deep, 0.80 / 2.13 mm from the side edges
conn_depth = 5.75;
conn_gap = 0.5;         // clearance between the connector and the seat posts / pegs on the ribbon side
conn_clear = 3.75;         // space behind the PCB for the FFC connector and ribbon bend
window_gap = 1.5;       // lens front to window
win_d = 17;             // clear aperture: wide enough for 120 deg FOV at window_gap
disc_d = 25.6;          // window disc seat: 25 mm round flat glass tile (CleverDelights B0B64HRC21) + 0.6 mm for its loose tolerance
disc_t = 3.5;           // tile thickness per the listing (verify with calipers when it arrives)
seat_t = disc_t + 0.1;
lip_t = 2.0;            // cap material in front of the disc
cap_t = seat_t + lip_t;
top_ext = 2.4;          // extra cavity length on the ribbon side so the 25.6 mm seat stays inside the gasket groove
chamfer = 1.5;          // outward flare of the aperture so the cap never vignettes
slot_w = 17;            // ribbon slot (16 mm 15-pin / 11.5 mm 22-pin FFC)
slot_h = 2.4;

// --- screws and gasket ---
ear_r = 4; ear_off = 1.5;
pilot_d = 2.1;          // M2.5 self-tapping
clear_d = 2.7;
screw_depth = 10;
groove_in = 0.9; groove_w = 1.4; groove_d = 1.1;   // 1.5 mm O-ring cord or silicone bead

// --- magnets (two pockets, polarity marked in the file as + on both) ---
mag_d = 15;
mag_t = 5;              // thickness of the whole stack in one pocket
skin = 0.6;             // printed skin between magnet and wall: keeps the magnet sealed
mag_fit = 0.3;

$fn = 48;

cav_w = cam_w + fit;
cav_h = cam_d + fit + top_ext;
ex = exit_side == "top" ? 1 : -1;
// PCB sits against the far wall; the extension is on the ribbon side
board_cy = -ex * (cav_h / 2 - fit / 2 - cam_d / 2);
lens_y = board_cy + lens_dy;   // world-of-pod Y of the lens centre (lens_dy is relative to the PCB centre)
// seat post / peg centre Y: ribbon-side ones sit just past the connector so they do not land on it
// cap peg centre Y: original corner positions (1.5 mm in from each PCB edge), unlike the base posts which clear the connector
function peg_y(sy) = sy == ex ? board_cy + ex * (cam_d / 2 - 1.5) : sy * (cav_h / 2 - 1.75);
function seat_y(sy) = sy == ex ? board_cy + ex * (cam_d / 2 - conn_depth - conn_gap - 1.75) : sy * (cav_h / 2 - 1.75);
out_w = cav_w + 2 * wall;
out_h = cav_h + 2 * wall;
ledge_z = floor_t + conn_clear;
lens_z = ledge_z + cam_total;
rim_z = lens_z + window_gap;
peg_len = rim_z - (ledge_z + cam_pcb_t) - 0.1;
ear_x = out_w / 2 + ear_off;
ear_y = out_h / 2 + ear_off;

base_t = mag_t + skin + 1.4;
plate_w = 2 * mag_d + 8;

// pod placement in the wall frame
mag_extra = 9;                                    // extra plate so the magnets stay clear of the autofocus coil
mag_zone = mount == "magnet" ? mag_d + 6 + mag_extra + (base_t + 3) * tan(tilt)   // plate length below the pod
                             : 2;                                              // flat (tape / Command Strips): no plate, the wedge footprint is the contact area
Yb = mag_zone;                                     // bottom-rear edge of the pod, on the wall
py = Yb + (out_h / 2) * cos(tilt);
pz = (out_h / 2 + ear_off + ear_r) * sin(tilt);   // lowest ear edge touches the wall
Ytr = py + (out_h / 2) * cos(tilt);
Ztr = pz + (out_h / 2) * sin(tilt);
Ytop0 = Ytr + Ztr * tan(tilt);                     // top face plane meets the wall

module place_pod() { translate([0, py, pz]) rotate([tilt, 0, 0]) children(); }

module ear(x, y) { translate([x, y, 0]) cylinder(r = ear_r, h = rim_z); }

module core() { translate([-out_w / 2, -out_h / 2, 0]) cube([out_w, out_h, rim_z]); }

module rect_ring(w, h, d) {
  difference() {
    translate([-w / 2 - groove_w - groove_in, -h / 2 - groove_w - groove_in, 0])
      cube([w + 2 * (groove_w + groove_in), h + 2 * (groove_w + groove_in), d]);
    translate([-w / 2 - groove_in, -h / 2 - groove_in, -0.1])
      cube([w + 2 * groove_in, h + 2 * groove_in, d + 0.2]);
  }
}

module pod_cuts() {
  // camera cavity
  translate([-cav_w / 2, -cav_h / 2, floor_t]) cube([cav_w, cav_h, rim_z]);
  // gasket groove in the rim
  translate([0, 0, rim_z - groove_d]) rect_ring(cav_w, cav_h, groove_d + 0.1);
  // screw pilots
  for (sx = [-1, 1], sy = [-1, 1])
    translate([sx * ear_x, sy * ear_y, rim_z - screw_depth]) cylinder(d = pilot_d, h = screw_depth + 0.1);
  // ribbon slot through the chosen edge
  sy = exit_side == "top" ? 1 : -1;
  translate([-slot_w / 2, sy > 0 ? cav_h / 2 - 1 : -out_h / 2 - 1, floor_t + 1])
    cube([slot_w, wall + 2, slot_h]);
}

module corner_posts() {
  // PCB seat: four corner posts at ledge height
  for (sx = [-1, 1], sy = [-1, 1])
    translate([sx * (cav_w / 2 - 1.75), seat_y(sy), (floor_t + ledge_z) / 2 - 0.05])
      cube([3.5, 3.5, ledge_z - floor_t + 0.1], center = true);
}

module top_stops() {
  // keep the PCB from sliding along Y (ribbon push/pull): blocks in the cavity extension, beside the ribbon slot, fit/2 clear of the PCB edge
  edge_y = ex * (cav_h / 2 - top_ext);
  x0 = slot_w / 2 + 1;
  for (sx = [-1, 1])
    translate([sx > 0 ? x0 : -cav_w / 2 - 0.5, ex > 0 ? edge_y : edge_y - top_ext - 0.5, floor_t - 0.05])
      cube([cav_w / 2 - x0 + 0.5, top_ext + 0.5, ledge_z + cam_pcb_t - floor_t + 0.05]);
}

module body_world() {
  difference() {
    union() {
      hull() { place_pod() core(); translate([-out_w / 2, Yb, 0]) cube([out_w, Ytop0 - Yb, 0.01]); }
      for (sx = [-1, 1], sy = [-1, 1]) {
        // ears: hull each one down to the wall so nothing floats
        hull() {
          place_pod() ear(sx * ear_x, sy * ear_y);
          translate([sx * ear_x, py + sy * ear_y * cos(tilt), 0]) cylinder(r = ear_r, h = 0.01);
        }
      }
      if (mount == "magnet") translate([-plate_w / 2, 0, 0]) cube([plate_w, Yb + 0.5, base_t]);
    }
    place_pod() pod_cuts();
    if (mount == "magnet")
      for (sx = [-1, 1])
        translate([sx * (mag_d / 2 + 1), mag_d / 2 + 3, skin])
          cylinder(d = mag_d + mag_fit, h = base_t);
  }
  place_pod() corner_posts();
  place_pod() top_stops();
}

module cap_local() {
  difference() {
    union() {
      translate([-out_w / 2, -out_h / 2, 0]) cube([out_w, out_h, cap_t]);
      for (sx = [-1, 1], sy = [-1, 1]) translate([sx * ear_x, sy * ear_y, 0]) cylinder(r = ear_r, h = cap_t);
    }
    // window aperture with outward chamfer, centred on the lens
    translate([0, lens_y, -0.1]) cylinder(d = win_d, h = cap_t + 0.2);
    translate([0, lens_y, cap_t - chamfer]) cylinder(d1 = win_d, d2 = win_d + 2 * chamfer, h = chamfer + 0.01);
    // disc seat, open to the inside face
    translate([0, lens_y, -0.1]) cylinder(d = disc_d, h = seat_t + 0.1);
    for (sx = [-1, 1], sy = [-1, 1])
      translate([sx * ear_x, sy * ear_y, -0.1]) cylinder(d = clear_d, h = cap_t + 0.2);
  }
  // pegs that pin the PCB corners against the posts. Trimmed to stay outside the glass seat (plus a 0.3 mm solid ring)
  // so every peg stands on solid cap material.
  for (sx = [-1, 1], sy = [-1, 1])
    difference() {
      translate([sx * (cav_w / 2 - 1.75), peg_y(sy), -peg_len / 2 + 0.01]) cube([3.5, 3.5, peg_len], center = true);
      translate([0, lens_y, -peg_len - 1]) cylinder(d = disc_d + 0.6, h = peg_len + 2);   // reaches past the pegs' 0.01 overlap so no sliver is left over the seat
    }
}

if (part == "assembly") {
  body_world();
  place_pod() translate([0, 0, rim_z]) cap_local();
} else if (part == "body") {
  body_world();                                          // wall face already on the bed
} else if (part == "cap") {
  translate([0, 0, cap_t]) rotate([180, 0, 0]) cap_local();   // outer face on the bed
}

// --- sanity numbers, printed on render ---
lens_world_Y = py + lens_y * cos(tilt) - lens_z * sin(tilt);
lens_world_Z = pz + lens_y * sin(tilt) + lens_z * cos(tilt);
mag_Y = mag_d / 2 + 3;
echo(str("pod outer ", out_w, " x ", out_h, " x ", rim_z + cap_t, " mm; plate ", plate_w, " x ", Ytop0, " x ", base_t));
if (mount == "magnet") echo(str("lens to magnet distance: ", sqrt(pow(lens_world_Y - mag_Y, 2) + pow(lens_world_Z - base_t / 2, 2)), " mm (keep >= 30)"));
echo(str("lens projects ", lens_world_Z, " mm off the wall"));
echo(str("disc seat clears the gasket groove by ", (cav_h / 2 + groove_in) - (lens_y + disc_d / 2), " mm at the ribbon side (want >= 0.3); cap thickness ", cap_t, " mm"));
echo(str("wall footprint: ", out_w, " x ", Ytop0 - Yb, " mm (flat mount contact area ", out_w * (Ytop0 - Yb), " mm2)"));
