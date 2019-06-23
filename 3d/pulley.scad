$fn = 200;

smallD = 35;
bigD = 50;
spacer = 3;
center = 3;
coneH = 3;
holeD = 5;
scal = 0.6;
splines = 16;


module cone(sstart){
	difference(){
		union(){
			translate([0, 0, 0]) cylinder(h=spacer, d=bigD);
			translate([0, 0, spacer]) cylinder(coneH, d1=bigD, d2=smallD);
			translate([0, 0, center + coneH]) cylinder(h=spacer, d=smallD);
		}
		cylinder(d=holeD, h=(coneH*2)+(spacer*2) + center);
	}
	translate([2 -0.1, -holeD/2, 0]) cube([holeD, holeD, spacer + center + coneH]);

	// for (i=[sstart:360/splines:360]){ 
	// 	echo(i);
	// 	rotate([0,0,i]) spline();
	// }
}

module spline(){
	difference(){
		hull(){
			translate([smallD/2, 0, spacer + coneH]) cube([center, scal, center]);
			translate([bigD/2, 0, spacer])cube([0.01, scal, coneH*2 + center]);
		}
		hull(){
			translate([smallD/2 + scal, 0, spacer + coneH + scal]) cube([center, scal, center]);
			translate([bigD/2 + scal, -0.1, spacer+scal])cube([0.01, scal + 0.2, coneH*2 + center]);
		}
		translate([0,0,spacer+coneH+center+1]) cylinder(d=bigD, h=2, center=true);
	}
}

difference(){
	cone(sstart=0);
	translate([0,-bigD/2, spacer + coneH]) cube([smallD, bigD, 10]);
}
translate([-smallD/3, 0, (spacer + coneH+center)-3]) cylinder(r=3, h=6) ;

translate([bigD + 3, 0, 0]){
	difference(){
		cone(sstart=360/2/splines);
		translate([-smallD,-bigD/2, spacer + coneH]) cube([smallD, bigD, 10]);
		translate([-smallD/3, 0, coneH+spacer-3]) cylinder(r=3, h=3) ;
	}
}