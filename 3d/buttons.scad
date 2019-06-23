$fn=100;


height = 7;
width = 12;
separator = 4;
holeblock = 8;
hole = 2;
lower = height - 3.8;
tolerance = 0.3;
holeblock_h = height + 4;

difference(){
	union(){
		translate([0,  0, 0]) cube([width, holeblock, holeblock_h    ]);
		translate([0,  8, 0]) cube([width, separator, height+2       ]);
		translate([0, 12, 0]) cube([width, width,     height         ]);
		translate([0, 24, 0]) cube([width, separator, holeblock_h - 3]);
		translate([0, 28, 0]) cube([width, width,     lower          ]);
		translate([0, 40, 0]) cube([width, separator, holeblock_h    ]);
		translate([0, 44, 0]) cube([width, width,     height         ]);
		translate([0, 56, 0]) cube([width, separator, height+2       ]);
		translate([0, 60, 0]) cube([width, holeblock, holeblock_h    ]);
	}
	translate([width/2, 64, -tolerance]) cylinder(r=hole, h=holeblock_h + (tolerance*2));
	translate([width/2,  4, -tolerance]) cylinder(r=hole, h=holeblock_h + (tolerance*2));
}

// 0 - 14 - 16 -  16 - 14