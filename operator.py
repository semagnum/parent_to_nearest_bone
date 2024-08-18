import math 

import bpy
from mathutils import Vector


def closest_bone(ob, armature):
    """Finds closest bone in armature to the object"""
    # go to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # finds the minimum value from a list of tuples that store the distance and the bone itself
    # and stores the resulting bone
    armature_matrix_world = armature.matrix_world
    closest = min([
        (math.dist(get_geometry_center(ob), armature_matrix_world @ bone.center), bone.name)
        for bone in armature.data.edit_bones
    ])

    _, closest_bone_name = closest

    # back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return closest_bone_name


def get_head_position(ar, bone):
    """Gets the bone head's position of the bone in object space"""
    bpy.ops.object.mode_set(mode='EDIT')
    head = ar.data.edit_bones[bone].head
    bpy.ops.object.mode_set(mode='OBJECT')

    return head


def get_center_position(armature, bone):
    """Gets the bone's center position in object space"""
    bpy.ops.object.mode_set(mode='EDIT')
    center = armature.data.edit_bones[bone].center
    bpy.ops.object.mode_set(mode='OBJECT')

    return center


def get_geometry_center(ob):
    """Returns geometric center of the object, calculating the average of the bounding box min and max."""
    matrix_world = ob.matrix_world

    bounding_max = matrix_world @ Vector(ob.bound_box[6])
    bounding_min = matrix_world @ Vector(ob.bound_box[0])

    return (bounding_max + bounding_min) * 0.5


def parent_to_bone_kt(obj, armature, parent_bone):
    """The parenting is done using bpy.ops because
    it's the only way I found for preserving
    the transform of the object in the process.
    All other methods resulted in weird relocation of the object.

    The drawback is that this process
    involves deselecting and reselecting each object.
    This may be slow for large selection sets.
    """

    bpy.ops.object.select_all(action='DESELECT')
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature

    # set active bone in edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    armature.data.edit_bones.active = armature.data.edit_bones[parent_bone]
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type='BONE', keep_transform=True)


class ParentToNearestBone(bpy.types.Operator):
    """Parents all selected objects to the nearest Bone in Active Armature,
    comparing the Bone's center to each Object's geometric center.
    """
    bl_idname = 'object.parent_to_nearest_bone'
    bl_label = 'Parent to Nearest Bone'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        my_objects = [ob for ob in context.selected_objects if ob.type != 'ARMATURE']
        armature = context.active_object
        
        for obj in my_objects:
            parent_to_bone_kt(obj, armature, closest_bone(obj, armature))

        return {'FINISHED'}