import bpy
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
      
points = extract_points(data)

face = data.surface.surface_sampler_data

vertex = []

for p in points:
    vertex.append(p)

faces = []

for x in face:
    for y in x:
        faces.append(y)
    #faces.append(face)
#Define vertices, faces, edges
#vertex = [(0,0,0),(0,4,0),(4,4,0),(4,0,0),(0,0,4),(0,4,4),(4,4,4),(4,0,4)]
#faces = [(0,1,2,3), (4,5,6,7), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)]
#vertex = [tuple(l) for l in vertex]
#faces = [tuple(l) for l in faces]

#print(len(faces))
#print(len(vertex))

#Define mesh and object
mesh = bpy.data.meshes.new("Sphere")
object = bpy.data.objects.new("Sphere", mesh)
 
#Set location and scene of object
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#Create mesh
mesh.from_pydata(vertex,[],faces)
#mesh.update()
mesh.update(calc_edges=True)


