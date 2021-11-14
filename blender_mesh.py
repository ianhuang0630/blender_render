import os
import sys
import numpy as np
import bpy
sys.path.append(os.getcwd()) # for some reason the working directory is not in path

def load_obj(fn):
    fin = open(fn, 'r')
    lines = [line.rstrip() for line in fin]
    fin.close()

    vertices = []; normals = []; faces=[];
    for line in lines:
        if line.startswith('v '):
            vertices.append(np.float32(line.split()[1:4]))
        elif line.startswith('f '):
            faces.append(np.int32([item.split('/')[0] for item in line.split()[1:4]]))
    f = np.vstack(faces) - 1 
    v = np.vstack(vertices)
    return v, f

def load_colors(fn):
    colors = []
    with open(fn, 'r') as f:
        rgbs = f.readlines()
        for rgb in rgbs:
            colors.append([int(el) for el in rgb.rstrip().split()])
    return np.array(colors)/255

obj_filename = sys.argv[6]
colors_filename = sys.argv[7]
output_filename = sys.argv[8]
magnification = 3

verts, faces = load_obj(obj_filename)
verts = verts * magnification
colors = load_colors(colors_filename)

# # rotate for blender
coord_rot = np.array([[-1, 0, 0], 
                    [0, 0, 1], 
                    [0, 1, 0]])
verts = np.matmul(verts, coord_rot.transpose())

if 'object' in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects['object'], do_unlink=True)

if 'sphere' in bpy.data.meshes:
    bpy.data.meshes.remove(bpy.data.meshes['sphere'], do_unlink=True)

if 'object' in bpy.data.meshes:
    bpy.data.meshes.remove(bpy.data.meshes['object'], do_unlink=True)

# vert_colors = np.repeat(colors, verts.shape[0], axis=0).astype(dtype='float64')
vert_colors = colors[faces.reshape(-1), :]

verts[:, 2] -= verts.min(axis=0)[2]

print(verts.shape, faces.shape, vert_colors.shape)
verts = verts.tolist()
faces = faces.tolist()
vert_colors = vert_colors.tolist()
#

scene = bpy.context.scene
mesh = bpy.data.meshes.new('object')
mesh.from_pydata(verts, [], faces)
mesh.validate()

mesh.vertex_colors.new(name='Col') # named 'Col' by default
mesh_vert_colors = mesh.vertex_colors['Col']

for i, c in enumerate(mesh.vertex_colors['Col'].data):
    c.color = vert_colors[i] + [1.0]

print(i)
obj = bpy.data.objects.new('object', mesh)
obj.data.materials.append(bpy.data.materials['sphere_material'])
# scene.objects.link(obj)
# NEW:
bpy.context.collection.objects.link(obj)
# 
output_filename = output_filename # 'bleh'
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = output_filename
bpy.ops.render.render(write_still=True)
