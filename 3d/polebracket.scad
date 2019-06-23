include <BOSL/constants.scad>
include <BOSL/shapes.scad>

$fn=100;

poleR = 25;
holeR = 3;
nutR = 6;
nutD = 6;
holeblkL = 15;
blockW = 30;
blockH = 8 + poleR - 5;
blockL = (poleR + holeblkL) * 2;
opening = 2;
echo(blockL);

difference(){
	cuboid([blockL, blockW, blockH], center=false, fillet=2);
	#translate([blockL/2, 0, -opening]) rotate([-90, 0, 0]) cylinder(r=poleR, h=blockW);

	translate([holeblkL/2, blockW/2, 0]) cylinder(r=holeR, h=blockH);
	translate([holeblkL/2, blockW/2, blockH - nutD]) cylinder(r=nutR, h=nutD);
	translate([blockL - holeblkL/2, blockW/2, 0]) cylinder(r=holeR, h=blockH);
	translate([blockL - holeblkL/2, blockW/2, blockH - nutD]) cylinder(r=nutR, h=nutD);
}

translate([100,0,0])

difference(){
	cuboid([blockL, blockW, blockH], center=false, fillet=3);
	translate([blockL/2, 0, -opening]) rotate([-90, 0, 0]) cylinder(r=poleR, h=blockW);
	translate([holeblkL/2, blockW/2, 0]) cylinder(r=holeR, h=blockH);
	translate([blockL - holeblkL/2, blockW/2, 0]) cylinder(r=holeR, h=blockH);
}