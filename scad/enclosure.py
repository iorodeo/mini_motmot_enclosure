"""
Creates an enclosure
"""
from py2scad import *

INCH2MM = 25.4

# Inside dimensions
x,y,z = 7.5*INCH2MM, 3.25*INCH2MM, 1.5*INCH2MM
hole_list = []

# Offset of pcb from  walls
pcb_offset_x = 0.5*INCH2MM
pcb_offset_y = 0.125*INCH2MM

# Size of teensy pcb and hole spacings
teensy_x = 2.25*INCH2MM
teensy_y = 3.0*INCH2MM
teensy_hole_x = 2.0*INCH2MM 
teensy_hole_y = 2.75*INCH2MM

teensy_bnc_x = 0.5*INCH2MM
teensy_bnc_z = 0.76*INCH2MM

teensy_usb_x = -0.5*INCH2MM
teensy_usb_z = 0.7*INCH2MM

# Size of buffer pcb and hole spacings
buffer_x = 4.0*INCH2MM
buffer_y = 1.25*INCH2MM
buffer_hole_x = 2.0*INCH2MM
buffer_hole_y = 1.0*INCH2MM

buffer_bnc_number = 4
buffer_bnc_x_start = -1.5*INCH2MM
buffer_bnc_spacing = 1.0*INCH2MM
buffer_bnc_z = teensy_usb_z

mount_hole_diam = 0.12* INCH2MM
bnc_hole_diam = 14.0
usb_hole_size = (14.0, 12.0, 1.0)

# Find position for center of teensy PCB
teensy_center_x = -0.5*x + 0.5*teensy_x + pcb_offset_x
teensy_center_y = -0.5*y + 0.5*teensy_y + pcb_offset_y

# Find positin for center of buffer PCB
buffer_center_x = 0.5*x - 0.5*buffer_x - pcb_offset_x
buffer_center_y = -0.5*y + 0.5*buffer_y + pcb_offset_y

# Create mount holes for teensy
for i in (-1,1):
    for j in (-1,1):
        hole_x = teensy_center_x + i*0.5*teensy_hole_x
        hole_y = teensy_center_y + j*0.5*teensy_hole_y
        hole = {
                'panel'     : 'bottom',
                'type'      : 'round',
                'location'  : (hole_x,hole_y),
                'size'      : mount_hole_diam,
                }
        hole_list.append(hole)
        
# Create mount holes for buffer
for i in (-1,1):
    for j in (-1,1):
        hole_x = buffer_center_x + i*0.5*buffer_hole_x
        hole_y = buffer_center_y + j*0.5*buffer_hole_y
        hole = {
                'panel'     : 'bottom',
                'type'      : 'round',
                'location'  : (hole_x,hole_y),
                'size'      : mount_hole_diam,
                }
        hole_list.append(hole)

# Add BNC hole for teensy
hole_x = teensy_center_x + teensy_bnc_x
hole_z = -0.5*z + teensy_bnc_z
hole = {
        'panel'    : 'front',
        'type'     : 'round',
        'location' : (hole_x,hole_z),
        'size'     : bnc_hole_diam,
        }
hole_list.append(hole)

# Add USB hole for teensy
hole_x = teensy_center_x + teensy_usb_x
hole_z = -0.5*z + teensy_usb_z
hole = {
        'panel'    : 'front',
        'type'     : 'rounded_square',
        'location' : (hole_x,hole_z),
        'size'     : usb_hole_size, 
        }
hole_list.append(hole)

# Add array of BNC holes for buffer
for i in range(buffer_bnc_number):
    hole_x = buffer_center_x + buffer_bnc_x_start + i*buffer_bnc_spacing
    hole_z = -0.5*z + buffer_bnc_z
    hole = {
            'panel'    : 'front',
            'type'     : 'round',
            'location' : (hole_x,hole_z),
            'size'     : bnc_hole_diam,
            }
    hole_list.append(hole)


# Create enclosure parameters
params = {
        'inner_dimensions'        : (x,y,z), 
        'wall_thickness'          : (1.0/8.0)*INCH2MM, 
        'lid_radius'              : 0.25*INCH2MM,  
        'top_x_overhang'          : 0.2*INCH2MM,
        'top_y_overhang'          : 0.2*INCH2MM,
        'bottom_x_overhang'       : 0.2*INCH2MM,
        'bottom_y_overhang'       : 0.2*INCH2MM, 
        'lid2front_tabs'          : (0.2,0.5,0.8),
        'lid2side_tabs'           : (0.25, 0.75),
        'side2side_tabs'          : (0.5,),
        'lid2front_tab_width'     : 0.75*INCH2MM,
        'lid2side_tab_width'      : 0.75*INCH2MM, 
        'side2side_tab_width'     : 0.5*INCH2MM,
        'standoff_diameter'       : 0.25*INCH2MM,
        'standoff_offset'         : 0.05*INCH2MM,
        'standoff_hole_diameter'  : 0.116*INCH2MM, 
        'hole_list'               : hole_list,
        }

enclosure = Basic_Enclosure(params)
enclosure.make()

part_assembly = enclosure.get_assembly(
        explode=(0,0,0),
        show_top=True,
        show_bottom=True,
        show_left=True,
        show_right=True,
        show_front=True,
        show_back=True,
        )

part_projection = enclosure.get_projection()

prog_assembly = SCAD_Prog()
prog_assembly.fn = 50
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly.scad')

prog_projection = SCAD_Prog()
prog_projection.fn = 50
prog_projection.add(part_projection)
prog_projection.write('enclosure_projection.scad')

