import os
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_laser

dxfFileName = sys.argv[1]

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())

# Etching
param = {
        'fileName'    :  dxfFileName,
        'layers'      :  ['engrave'],
        'dxfTypes'    :  ['LINE','ARC'],
        'laserPower'  :  350,
        'feedRate'    :  60,
        'convertArcs' :  True,
        'startCond'   : 'minX',
        'direction'   : 'ccw',
        'ptEquivTol'  :  0.4e-3,
        }

vectorEtch = cnc_laser.VectorCut(param)
prog.add(vectorEtch)

# Cutting
param = {
        'fileName'    :  dxfFileName,
        'layers'      :  ['vector'],
        'dxfTypes'    :  ['LINE','ARC','CIRCLE'],
        'laserPower'  :  600,
        'feedRate'    :  25,
        'convertArcs' :  True,
        'startCond'   : 'minX',
        'direction'   : 'ccw',
        'ptEquivTol'  :  0.4e-3,
        }

vectorCut = cnc_laser.VectorCut(param)
prog.add(vectorCut)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)

baseName, ext = os.path.splitext(dxfFileName)
ngcFileName = '{0}.ngc'.format(baseName)
prog.write(ngcFileName)
