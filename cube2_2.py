import os
import bpy
import bmesh
from math import pi
import sys
bpy.context.scene.render.engine = 'CYCLES'
for material in bpy.data.materials:
    if material.name.startswith("rubik"):
        material.user_clear()
        bpy.data.materials.remove(material)

# Creating new material
def CreateMaterial(name, r, g, b):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    diffuse = nodes.get("Diffuse BSDF")
    output = nodes.get("Material Output")
    nodes.remove(diffuse)
    mat.diffuse_color = (r, g, b)

    # Creating principled shader
    node_princ = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_princ.inputs[0].default_value = (r, g, b, 1)
    node_princ.location = 0,0

    # link nodes
    links = mat.node_tree.links
    link = links.new(node_princ.outputs[0], output.inputs[0])
    return mat

addmat_black = CreateMaterial ("rubik_black", 0.025, 0.025, 0.025)
addmat_red = CreateMaterial ("rubik_red", 0.475, 0, 0)
addmat_white = CreateMaterial ("rubik_white", 0.8, 0.8, 0.8)
addmat_blue = CreateMaterial ("rubik_blue", 0, 0, 0.475)
addmat_green = CreateMaterial ("rubik_green", 0, 0.475, 0)
addmat_orange = CreateMaterial ("rubik_orange", 0.754, 0.110, 0)
addmat_yellow = CreateMaterial ("rubik_yellow", 0.754, 0.443, 0)

bpy.app.debug = True # Allowing to view vertices indexes

scn = bpy.context.scene
scn.frame_start = 1
current_frame = 20

bpy.context.scene.frame_set(current_frame)

for i in bpy.data.objects: # To be able to launch the script multiple time
    if i.name.startswith("rubik"):
        bpy.data.objects.remove(i)


for i in range(27):
    bpy.ops.mesh.primitive_cube_add(radius=0.25, location=(-0.50 * (int(i / 3) % 3), 0.50 * int(i / 9), 0.50 * (i % 3))) # Creating a cube
    bpy.context.object.name = "rubiks"+str(i)
  
    bpy.context.object.data.materials.append(addmat_black)
    bpy.context.object.data.materials.append(addmat_white)
    bpy.context.object.data.materials.append(addmat_red)
    bpy.context.object.data.materials.append(addmat_green)
    bpy.context.object.data.materials.append(addmat_blue)
    bpy.context.object.data.materials.append(addmat_yellow)
    bpy.context.object.data.materials.append(addmat_orange)

# Extrude all faces
def extrude(name, faces, index, trans, size, material):
    for j in range(9):
        for i in bpy.data.objects:
            if i.name == "rubiks"+str(faces[j]):
                vg = i.vertex_groups.new(name)
                vg.add(index, 0, "ADD")
                bpy.context.scene.objects.active = i
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.context.object.vertex_groups.active = vg
                bpy.ops.object.vertex_group_select()
                bpy.ops.mesh.extrude_faces_indiv()
                bpy.ops.transform.translate(value=trans)
                bpy.ops.transform.resize(value=(size, size, size))
                bpy.ops.object.mode_set(mode = 'OBJECT')
                vg.remove(index)
                bpy.ops.object.mode_set(mode = 'EDIT')
                i.active_material_index = material[j]
                bpy.ops.object.material_slot_assign()
                bpy.ops.object.mode_set(mode = 'OBJECT')

def allocateMaterial(CubeSide):
    mat = []
    for i in range(9):
        if CubeSide[i] == "U":
            mat.append(3)
        elif CubeSide[i] == "R":
            mat.append(6)
        elif CubeSide[i] == "F":
            mat.append(1)
        elif CubeSide[i] == "D":
            mat.append(4)
        elif CubeSide[i] == "L":
            mat.append(2)
        elif CubeSide[i] == "B":
            mat.append(5)
    return mat


backMat = [5, 5, 5, 5, 5, 5, 5, 5, 5]
leftMat = [2, 2, 2, 2, 2, 2, 2, 2, 2]
upMat = [3, 3, 3, 3, 3, 3, 3, 3, 3]
rightMat = [6, 6, 6, 6, 6, 6, 6, 6, 6]
frontMat = [1, 1, 1, 1, 1, 1, 1, 1, 1]
downMat = [4, 4, 4, 4, 4, 4, 4, 4, 4]

'''upMat = allocateMaterial(cubestring[0:9])
rightMat = allocateMaterial(cubestring[9:18])
frontMat = allocateMaterial(cubestring[18:27])
downMat = allocateMaterial(cubestring[27:36])
leftMat = allocateMaterial(cubestring[36:45])
backMat = allocateMaterial(cubestring[45:54])'''

back = [8, 5, 2, 7, 4, 1, 6, 3, 0]
extrude("back", back, [1, 5, 0, 4], (0, -0.05, 0), 0.9, backMat)
left = [2, 11, 20, 1, 10, 19, 0, 9, 18]
extrude("left", left, [4, 5, 6, 7], (0.05, 0, 0), 0.9, leftMat)
up = [2, 5, 8, 11, 14, 17, 20, 23, 26]
extrude("up", up, [1, 3, 5, 7], (0, 0, 0.05), 0.9, upMat)
right = [26, 17, 8, 25, 16, 7, 24, 15, 6]
extrude("right", right, [0, 1, 2, 3], (-0.05, 0, 0), 0.9, rightMat)
front = [20, 23, 26, 19, 22, 25, 18, 21, 24]
extrude("front", front, [2, 3, 6, 7], (0, 0.05, 0), 0.9, frontMat)
down = [18, 21, 24, 9, 12, 15, 0, 3, 6]
extrude("down", down, [0, 2, 4, 6], (0, 0, -0.05), 0.9, downMat)

# Front White = 1
# Left Red = 2
# Up Green = 3
# Down Blue = 4
# Back Yellow = 5
# Right Orange = 6

# Moves
def pause(nb):
    global current_frame
    for i in range(nb):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

def moveRight():
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    global textChange
    bpy.ops.object.select_all(action='DESELECT')
    for i in right:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * 10) / 180, axis=(1, 0, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    right = [right[6], right[3], right[0], right[7], right[4], right[1], right[8], right[5], right[2]]
    frontcpy = list(front)
    front[2] = down[2]
    front[5] = down[5]
    front[8] = down[8]
    down[2] = back[6]
    down[5] = back[3]
    down[8] = back[0]
    back[6] = up[2]
    back[3] = up[5]
    back[0] = up[8]
    up[2] = frontcpy[2]
    up[5] = frontcpy[5]
    up[8] = frontcpy[8]

def moveRightReverse():
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    bpy.ops.object.select_all(action='DESELECT')
    for i in right:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * -10) / 180, axis=(1, 0, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    right = [right[2], right[5], right[8], right[1], right[4], right[7], right[0], right[3], right[6]]
    frontcpy = list(front)
    front[2] = up[2]
    front[5] = up[5]
    front[8] = up[8]
    up[2] = back[6]
    up[5] = back[3]
    up[8] = back[0]
    back[6] = down[2]
    back[3] = down[5]
    back[0] = down[8]
    down[2] = frontcpy[2]
    down[5] = frontcpy[5]
    down[8] = frontcpy[8]

pause(1)
moveRightReverse()
pause(1)
moveRightReverse()
pause(1)
moveRight()
pause(1)
moveRight()
pause(1)
    
    
    