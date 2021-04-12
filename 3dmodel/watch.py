import cadquery as cq

WALL = 1.5
INNER_RADIUS = 20
PCB_THICKNESS = 1.6
BATTERY_HOLDER_HEIGHT = 4.5
BATTERY_HOLDER_POSITION = (0,-11.0,2)
WATCHFACE_HOLDER_POSITION_1 = (17.5, 0, 2)
WATCHFACE_SCREW_POSITION_1 = (17.5, 0, 1)
BOTTOM_PART_HEIGHT = 6
TOLERANCE=0.1
CONNECTION_CAP_SIZE = 0.8
LEG_SIZE = 2*INNER_RADIUS+14
LEG_HOLE_OFFSET = INNER_RADIUS + 5
STRAP_SIZE = 19

### Watch Face ###
button_hole = cq.Workplane("XY").circle(1.5).extrude(10)\
            .rotate((0, 0, 0),(-19, 10.5, 0), 90)\
            .translate((10-3.5,19-3,3.7))
            
body = cq.Workplane("XY" )\
        .circle(INNER_RADIUS-TOLERANCE).extrude(BOTTOM_PART_HEIGHT)\
        .faces("+Z").shell(WALL+TOLERANCE, kind='arc')\
        .cut(button_hole)

connection_shell = cq.Workplane("XY" )\
        .circle(INNER_RADIUS-CONNECTION_CAP_SIZE-TOLERANCE)\
        .extrude(BOTTOM_PART_HEIGHT+1.5)\
        .faces("+Z").shell(CONNECTION_CAP_SIZE, kind='arc')\
        .cut(button_hole)

battery_holder_left = cq.Workplane("XY" )\
        .box(20,1.5,BATTERY_HOLDER_HEIGHT)\
        .translate(BATTERY_HOLDER_POSITION)
battery_holder_right = battery_holder_left.mirror(mirrorPlane="XZ")

cut_watchface_screw_hole = cq.Workplane("XY" )\
        .circle(0.8)\
        .extrude(4)\
        .translate(WATCHFACE_SCREW_POSITION_1)

watchface_holder_1 = cq.Workplane("XY").box(4,10,BATTERY_HOLDER_HEIGHT)\
                    .translate(WATCHFACE_HOLDER_POSITION_1)\
                    .edges("|Z").fillet(1.1)\
                    .cut(cut_watchface_screw_hole)

watchface_holder_2 = watchface_holder_1.mirror(mirrorPlane="YZ")

### LEGS ###
leg_base = cq.Workplane("XY")\
        .line(LEG_SIZE/2, 0)\
        .line(0, 5)\
        .line(-(LEG_SIZE/2), 4)\
        .line(-(LEG_SIZE/2), -4)\
        .line(0, -5)\
        .close().extrude(6)

cut1_bottom_profile = cq.Workplane("XY").circle(80)\
                    .extrude(10)\
                    .translate((0,-76.5,-10))\
                    .rotate((0,0,0),(1,0,0),90)
cut2_top_profile = cq.Workplane("XY").circle(80)\
                    .extrude(10).translate((0,-71.75,-10))\
                    .rotate((0,0,0),(1,0,0),90)
cut3_watch_base = cq.Workplane("XY").circle(WALL+INNER_RADIUS).extrude(10)
cut4_strap_hole = cq.Workplane("XY").circle(1).extrude(30)\
                .translate((LEG_HOLE_OFFSET,0.4,-15))\
                .rotate((0, 0, 0),(1, 0, 0), 90)
cut5_strap_hole = cut4_strap_hole.mirror(mirrorPlane="YZ")

right_leg = leg_base\
        .cut(cut1_bottom_profile)\
        .cut(leg_base.cut(cut2_top_profile))\
        .edges("|Y").fillet(1.5)\
        .translate((0,STRAP_SIZE/2+TOLERANCE,-1.5))\
        .cut(cut3_watch_base)\
        .cut(cut4_strap_hole).cut(cut5_strap_hole)
        
left_leg = right_leg.mirror(mirrorPlane="XZ")

result = body\
            .union(connection_shell)\
            .union(right_leg)\
            .union(left_leg)\
            .union(battery_holder_left)\
            .union(battery_holder_right)\
            .union(watchface_holder_1)\
            .union(watchface_holder_2)

top_body = cq.Workplane("XY")\
    .polyline([(0,INNER_RADIUS),
               (0,INNER_RADIUS+WALL),
               (2.5,INNER_RADIUS+WALL),
               (2.5+WALL,INNER_RADIUS),
               (2.5+WALL,INNER_RADIUS-2),
               (2.5,INNER_RADIUS-2),
               (2.5,INNER_RADIUS)])\
    .close()\
    .revolve(axisStart=(1, 0), axisEnd=(0, 0), angleDegrees=360)\
    .rotate((0, 0, 0),(0, 1, 0), 90).translate((-50,0,4))

show_object(result)
show_object(top_body)