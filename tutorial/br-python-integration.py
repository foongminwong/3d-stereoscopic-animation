import os
import bpy
import bmesh
import bertini_real
import numpy as np

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

#Define vertices, faces, edges
points = extract_points(data)

face = data.surface.surface_sampler_data

vertex = []

for p in points:
    vertex.append(p)

faces = []

for x in face:
    for y in x:
        faces.append(y)

# Retrieve filename
fileName = os.getcwd().split(os.sep)[-1]

#Define mesh and object
mesh = bpy.data.meshes.new(fileName)
object = bpy.data.objects.new(fileName, mesh)
 
#Set location and scene of object
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#Create mesh
mesh.from_pydata(vertex,[],faces)
mesh.update(calc_edges=True)



# Make object active
bpy.context.scene.objects.active = object

# Scale object
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



