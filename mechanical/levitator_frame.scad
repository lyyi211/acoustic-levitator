// Concave 36+36 arrays; common focus at [0,0,0]. Units: millimetres.
include <generated_geometry.scad>
part = "assembly"; // assembly, cup, frame, fit_coupon
show_transducers = false;
show_focus = false;
$fn = 48;

module radial_axis(p) {
    translate(p)
        rotate([0, acos(p[2]/norm(p)), atan2(p[1],p[0])]) children();
}

module upper_cup() {
    difference() {
        union() {
            intersection() {
                difference() {
                    sphere(r=curvature_radius_mm+shell_thickness_mm, $fn=96);
                    sphere(r=curvature_radius_mm, $fn=96);
                }
                translate([-cup_outer_radius_mm,-cup_outer_radius_mm,rim_z_mm])
                    cube([2*cup_outer_radius_mm,2*cup_outer_radius_mm,
                          curvature_radius_mm+shell_thickness_mm-rim_z_mm+1]);
                cylinder(r=cup_outer_radius_mm,h=curvature_radius_mm+shell_thickness_mm+1);
            }
            for (side=[-1,1])
                translate([side < 0 ? -mount_x_mm-ear_half_width_mm : cup_outer_radius_mm-5,
                           -ear_half_width_mm,rim_z_mm])
                    cube([mount_x_mm+ear_half_width_mm-(cup_outer_radius_mm-5),
                          2*ear_half_width_mm,ear_thickness_mm]);
        }
        for (p=upper_face_centres_mm)
            radial_axis(p) translate([0,0,-2])
                cylinder(d=transducer_diameter_mm+socket_clearance_mm,
                         h=transducer_body_height_mm+2);
        // Rear shoulder seats the can; smaller hole passes both leads.
        for (p=upper_face_centres_mm)
            radial_axis(p) translate([0,0,-2])
                cylinder(d=rear_wire_clearance_mm,h=shell_thickness_mm+5);
        cylinder(d=center_access_diameter_mm,h=curvature_radius_mm+shell_thickness_mm+2);
        for (side=[-1,1])
            translate([side*mount_x_mm,0,rim_z_mm-1])
                cylinder(d=bolt_clearance_mm,h=ear_thickness_mm+2);
    }
}

module support_frame() {
    difference() {
        union() {
            translate([-base_width_mm/2,-base_depth_mm/2,base_bottom_mm])
                cube([base_width_mm,base_depth_mm,base_thickness_mm]);
            for (side=[-1,1]) {
                translate([side*mount_x_mm-ear_half_width_mm,
                           post_y_mm-post_depth_mm/2,base_top_mm-0.2])
                    cube([2*ear_half_width_mm,post_depth_mm,
                          upper_seat_z_mm+ear_thickness_mm-base_top_mm+0.2]);
                for (seat=[lower_seat_z_mm,upper_seat_z_mm])
                    translate([side*mount_x_mm-ear_half_width_mm,-ear_half_width_mm,
                               seat-shelf_thickness_mm])
                        cube([2*ear_half_width_mm,
                              post_y_mm+post_depth_mm/2+ear_half_width_mm,shelf_thickness_mm]);
            }
        }
        for (side=[-1,1]) for (seat=[lower_seat_z_mm,upper_seat_z_mm])
            translate([side*mount_x_mm,0,seat-shelf_thickness_mm-1])
                cylinder(d=bolt_clearance_mm,h=shelf_thickness_mm+2);
    }
}

module transducer_preview() {
    for (p=upper_face_centres_mm) radial_axis(p)
        cylinder(d=transducer_diameter_mm,h=transducer_body_height_mm);
}
module fit_coupon() {
    difference() {
        translate([-(transducer_diameter_mm+8)/2,-(transducer_diameter_mm+8)/2,0])
            cube([transducer_diameter_mm+8,transducer_diameter_mm+8,shell_thickness_mm]);
        translate([0,0,-1]) cylinder(d=transducer_diameter_mm+socket_clearance_mm,
                                  h=transducer_body_height_mm+1);
        translate([0,0,-1]) cylinder(d=rear_wire_clearance_mm,h=shell_thickness_mm+2);
    }
}
if (part == "cup") translate([0,0,-rim_z_mm]) upper_cup();
else if (part == "frame") translate([0,0,-base_bottom_mm]) support_frame();
else if (part == "fit_coupon") fit_coupon();
else if (part == "assembly") {
    color("steelblue") upper_cup();
    color("steelblue") rotate([180,0,0]) upper_cup();
    color("lightgray") support_frame();
    if (show_transducers) {
        color("silver") transducer_preview();
        color("silver") rotate([180,0,0]) transducer_preview();
    }
    if (show_focus) color("orange") sphere(d=2);
} else assert(false,"Unknown part; choose assembly, cup, frame or fit_coupon");
