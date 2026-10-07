# Ders başına 6 stil denemesi (B hattı). Çıktı: ComfyUI\output\stil_<ders>_<n>_*.png
$uret = "$PSScriptRoot\uret.ps1"
$sabit = "no text, no letters, no numbers, no watermark, no logo"

$stiller = @{
  physics1  = "Calm realistic photograph, natural light, sharp focus, clean uncluttered composition"
  materials = "Calm realistic macro photograph, soft studio light, sharp focus, clean uncluttered composition"
  circuits1 = "Technical macro photograph, shallow depth of field, clean electronics lab, crisp detail"
  digital   = "Technical macro photograph, shallow depth of field, clean electronics lab, crisp detail"
  oop       = "Flat minimal vector illustration, soft pastel palette, clean simple shapes, white background"
  linalg    = "Abstract minimal geometric vector illustration, thin clean lines, soft gradient background"
}

$sahneler = [ordered]@{
  physics1 = @(
    "an ice skater performing a spin with arms pulled tight against the body, on a rink, seen from the side",
    "a child on a playground seesaw, perfectly balanced horizontally, bright park",
    "a skydiver in free fall with an open parachute canopy above, blue sky and clouds",
    "a wooden swing hanging from a tree branch at the highest point of its arc, no person",
    "a metal pendulum clock mechanism close-up, brass pendulum swinging",
    "a rocket lifting off from a launch pad with a bright exhaust plume, seen from a distance"
  )
  materials = @(
    "a cylindrical silicon ingot next to a stack of polished silicon wafers on a dark surface",
    "a cluster of clear quartz crystals with sharp facets on a dark background",
    "a glowing blue LED on a small circuit board in a dark room",
    "a solar panel surface close-up with a grid of blue photovoltaic cells under sunlight",
    "a single integrated circuit chip held in tweezers, bright light",
    "a silicon wafer reflecting rainbow light patterns on its mirror surface"
  )
  circuits1 = @(
    "a through-hole resistor with colored bands lying on a white surface",
    "a solderless breadboard with colored jumper wires and a few components, top view",
    "an 8-pin op-amp integrated circuit chip on a green circuit board",
    "a toroidal transformer with copper winding on a workbench",
    "an electrolytic capacitor and a ceramic capacitor on a circuit board",
    "a digital multimeter with two probes touching a resistor on a breadboard"
  )
  digital = @(
    "an FPGA development board with switches and LEDs on a desk, top view",
    "a four-digit seven-segment LED display lit up on a dark background",
    "a CPU processor chip on a motherboard socket, close-up",
    "a printed circuit board with fine parallel copper traces forming a data bus",
    "a row of memory RAM modules inserted in a motherboard, close-up",
    "a ribbon cable connecting two circuit boards, shallow depth of field"
  )
  oop = @(
    "a cookie cutter shape pressed into dough with several identical cookies beside it",
    "a family tree with a grandparent at the top branching down to children and grandchildren, simple figures",
    "a universal remote control with one set of buttons controlling a television, a speaker and a lamp",
    "a stack of plates being added to and removed from the top only",
    "an ATM machine with a card slot and a cash dispenser slot, simple front view",
    "a house blueprint on a table next to a small finished house model"
  )
  linalg = @(
    "a three-dimensional cube casting a shadow onto a flat wall, abstract",
    "a mirror reflection of a triangle across a straight line, symmetrical composition",
    "a grid of dots slightly rotated and stretched, showing a linear transformation",
    "two arrows starting from one point forming a parallelogram on a plane",
    "a tilted flat plane in three-dimensional space with a perpendicular arrow standing on it",
    "a scatter of points with a straight best-fit line passing through the middle"
  )
}

$n = 0
foreach ($ders in $sahneler.Keys) {
  $i = 0
  foreach ($sahne in $sahneler[$ders]) {
    $i++; $n++
    $istem = "$($stiller[$ders]). $sahne. $sabit"
    $c = & $uret -Istem $istem -Tohum (100 + $n) -Onek ("stil_{0}_{1}" -f $ders, $i)
    "{0} {1}: {2}" -f $ders, $i, $c
  }
}
