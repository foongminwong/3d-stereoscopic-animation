import os
import bpy
import bertini_real
import math
import numpy as np

# Delete any meshes before creating a new mesh
item = 'MESH'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type=item)
bpy.ops.object.delete()
bpy.context.scene.render.use_overwrite = False


def extract_points(self):
    points = []

    for v in self.decomposition.vertices:
        q = [None] * 3

        for i in range(3):
            q[i] = v['point'][i].real
        points.append(q)

    return points

class Anaglyph():

    def __init__(self, data=None):

        if data is None:
            self.decomposition = bertini_real.data.ReadMostRecent()
        else:
            self.decomposition = data

    def generate_fv(self):

        # Extract points
        points = extract_points(self)

        # Extract face
        face = self.decomposition.surface.surface_sampler_data

        # Define vertices, faces
        vertex = [p for p in points]
        faces = [y for x in face for y in x]

        return vertex, faces

    def generate_obj_scene(self, vertex, faces):

        # Retrieve filename
        fileName = os.getcwd().split(os.sep)[-1]

        # Define mesh and object's name
        mesh = bpy.data.meshes.new(fileName)
        object = bpy.data.objects.new(fileName, mesh)

        # Set location and scene of object
        object.location = bpy.context.scene.cursor_location
        bpy.context.scene.objects.link(object)

        # Create mesh (error here, it works)
        mesh.from_pydata(vertex, [], faces)
        mesh.update()

        # Make object active
        bpy.context.scene.objects.active = object

        # Retrieve object dimensions
        object_dimensions = object.dimensions

        # Resize/ Scale object
        bpy.context.object.dimensions = object.dimensions[
            0], object.dimensions[1], 1.5  # resize z to 1.5

        # Grab the current object scale
        object_scale = object.scale

        # Scale them by z scale
        object.scale = (object_scale[2], object_scale[2], object_scale[2])

        # Rescale them (shoudl try ratio method?)
        object.scale = (1.5, 1.5, 1.5)

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

        return object, scene

    def rotate_z(self, object, scene):
        object.rotation_mode = 'XYZ'
        scene.frame_start = 1
        scene.frame_end = 100

        object.rotation_euler = (0, 0, 0)
        object.keyframe_insert('rotation_euler', index=2, frame=1)

        object.rotation_euler = (0, 0, math.radians(180))
        object.keyframe_insert('rotation_euler', index=2, frame=100)

        # Retrieve filename
        fileName = os.getcwd().split(os.sep)[-1]

        scene.render.filepath = "render/rotate_z_"
        scene.render.image_settings.file_format = "AVI_JPEG"

        bpy.ops.render.render(animation=True)

        print("Export " + '\x1b[0;33;40m' + "Anaglyph 3D " + '\x1b[0m' +
              '\x1b[0;35;40m' + fileName + '\x1b[0m' + " successfully")


def create_movie(data=None):
    surface = Anaglyph(data)
    vertex, faces = surface.generate_fv()
    object, scene = surface.generate_obj_scene(vertex, faces)
    surface.rotate_z(object, scene)


create_movie()


bpy.ops.wm.quit_blender()
