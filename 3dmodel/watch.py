import cadquery as cq

WALL = 1.5
INNER_RADIUS = 21
PCB_THICKNESS = 1.6
BATTERY_HOLDER_HEIGHT = 4.5
BATTERY_HOLDER_POSITION_1 = (17.5, 0)
BATTERY_HOLDER_POSITION_2 = (-17.5, 0)
BOTTOM_PART_HEIGHT = 6

### Watch Face ###
body = cq.Workplane("XY" )\
        .circle(INNER_RADIUS).extrude(BOTTOM_PART_HEIGHT)\
        .faces("+Z").shell(WALL, kind='arc')\
        .cut(cq.Workplane("XY").circle(1.5).extrude(10)\
            .rotate((0, 0, 0),(-19, 10.5, 0), 90)\
            .translate((10-3.5,19-3,3.7)))

connection_shell = cq.Workplane("XY" )\
        .circle(INNER_RADIUS).extrude(BOTTOM_PART_HEIGHT+1.5)\
        .faces("+Z").shell(0.8, kind='arc')\
        .cut(cq.Workplane("XY").circle(1.5).extrude(10)\
            .rotate((0, 0, 0),(-19, 10.5, 0), 90)\
            .translate((10-3.5,19-3,3.7)))

battery_holder_left = cq.Workplane("XY" )\
        .box(20,1.5,BATTERY_HOLDER_HEIGHT)\
        .translate((0,-11.0,2))
battery_holder_right = battery_holder_left.mirror(mirrorPlane="XZ")

watchface_holder_1 = cq.Workplane("XY" )\
        .circle(0.8)\
        .extrude(BATTERY_HOLDER_HEIGHT+PCB_THICKNESS)\
        .translate(BATTERY_HOLDER_POSITION_1)
watchface_holder_2 = watchface_holder_1.mirror(mirrorPlane="YZ")

### LEGS ###
leg_base = cq.Workplane("XY")\
        .line(28.5, 0)\
        .line(0, 5)\
        .line(-28.5, 4)\
        .line(-28.5, -4)\
        .line(0, -5)\
        .close().extrude(6)
cut1 = cq.Workplane("XY").circle(80).extrude(10).translate((0,-76.5,-10))\
             .rotate((0,0,0),(1,0,0),90)
cut2 = cq.Workplane("XY").circle(80).extrude(10).translate((0,-71.75,-10))\
             .rotate((0,0,0),(1,0,0),90)
cut3_watch_base = cq.Workplane("XY").circle(WALL+INNER_RADIUS).extrude(10)
cut4 = cq.Workplane("XY").circle(1).extrude(30)\
                .translate((26,0.4,-15))\
                .rotate((0, 0, 0),(1, 0, 0), 90)
cut5 = cut4.mirror(mirrorPlane="YZ")

right_leg = leg_base\
        .cut(cut1)\
        .cut(leg_base.cut(cut2))\
            .edges("|Y").fillet(1.5)\
        .translate((0,11,-1.5))\
        .cut(cut3_watch_base)\
        .cut(cut4).cut(cut5)
        
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