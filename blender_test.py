import bpy

#color changing code from http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Materials_and_textures

def makeMaterial(name, diffuse, specular, alpha):

    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT'
    mat.diffuse_intensity = 1.0
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat

def setMaterial(ob, mat):

    me = ob.data

    me.materials.append(mat)

#cleaning the scene from http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Interface
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

red = makeMaterial('Red',(1,0,0),(1,1,1),1)
origin = (0,0,0)
bpy.ops.mesh.primitive_uv_sphere_add(location=origin)
bpy.ops.transform.translate(value=(1,0,0))
setMaterial(bpy.context.object, red)
