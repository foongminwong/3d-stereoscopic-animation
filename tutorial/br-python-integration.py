import os
import bpy
import bertini_real
import math
import numpy as np

# Delete any meshes before starting create a new mesh
item='MESH'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type=item)
bpy.ops.object.delete()

bertini_real.data.gather()
data = bertini_real.data.ReadMostRecent()

def extract_points(data):
    points = []
    
    for v in data.vertices:
        q = [None] * 3
        
        for i in range(3):
            q[i] = v['point'][i].real
        points.append(q)
    return points


#Define vertices, faces
points = extract_points(data)

face = data.surface.surface_sampler_data

vertex = [p for p in points]

faces = [y for x in face for y in x]

# Retrieve filename
fileName = os.getcwd().split(os.sep)[-1]

#Define mesh and object
mesh = bpy.data.meshes.new(fileName)
object = bpy.data.objects.new(fileName, mesh)

#Set location and scene of object
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)

#Create mesh (error here, it works)
mesh.from_pydata(vertex,[],faces)
mesh.update()

# Make object active
bpy.context.scene.objects.active = object


# Retrieve object dimensions
object_dimensions = object.dimensions

# Resize/ Scale object
bpy.context.object.dimensions = object.dimensions[0],object.dimensions[1],3; # resize z to 3

# Grab the current object scale
object_scale = object.scale

# Scale them by z scale
object.scale = (object_scale[2],object_scale[2],object_scale[2])

# Rescale them (shoudl try ratio method?)
object.scale = (2,2,2)

# go edit mode
bpy.ops.object.mode_set(mode='EDIT')

# select all faces
bpy.ops.mesh.select_all(action='SELECT')

# recalculate outside normals 
bpy.ops.mesh.normals_make_consistent(inside=False)

# go object mode again
bpy.ops.object.editmode_toggle()

context = bpy.context
scene = context.scene

scene.render.use_multiview = True

bpy.context.scene.render.image_settings.views_format = 'STEREO_3D'

bpy.context.scene.cycles.film_exposure = 7.00

#-----Start rotation----#
"""
object.rotation_mode = 'XYZ'

scene.frame_start = 1
scene.frame_end = 100

object.rotation_euler = (0, 0, 0)
object.keyframe_insert('rotation_euler', index=2 ,frame=1)


object.rotation_euler = (0, 0,math.radians(180))
object.keyframe_insert('rotation_euler', index=2 ,frame=80)
"""

obj = bpy.context.active_object
startanim = 0
endeanim =300
bpy.data.scenes['Scene'].frame_start = startanim
bpy.data.scenes['Scene'].frame_end = endeanim

# rotate nothing
obj.rotation_euler=(0.0,0.0,0.0)
obj.keyframe_insert(data_path='rotation_euler',frame=0)

# rotate at the z-axis
obj.rotation_euler=(0,0,math.pi * 2)
obj.keyframe_insert(data_path='rotation_euler',frame=100)

# rotate at the y-axis
obj.rotation_euler=(0,math.pi * 2,math.pi * 2)
obj.keyframe_insert(data_path='rotation_euler',frame=200)

# rotate at the x-axis
obj.rotation_euler=(math.pi * 2,math.pi * 2,math.pi * 2)
obj.keyframe_insert(data_path='rotation_euler',frame=300)


scene.render.use_stamp = 1
scene.render.stamp_background = (0,0,0,0)

scene.render.filepath = "render/rotate"
scene.render.image_settings.file_format = "AVI_JPEG"
bpy.ops.render.render(animation=True)

print("Export " + '\x1b[0;33;40m' + "Anaglyph 3D " + '\x1b[0m' + '\x1b[0;35;40m' + fileName + '\x1b[0m' + " successfully")

bpy.ops.wm.quit_blender()

