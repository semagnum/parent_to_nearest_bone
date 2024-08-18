# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

if 'bpy' in locals():  # already reloaded
    import importlib
    importlib.reload(locals()['operator'])

bl_info = {
    "name": "Parent to Nearest bone",
    "author": "Pablo Gentile",
    "version": (0, 9, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Object > Parent > Parent to Nearest Bone",
    "description": "Parents selected objects to their nearest bones",
    "warning": "",
    "doc_url": "https://github.com/g3ntile/parentToNearestBone#readme",
    "category": "Object",
}

import bpy

from .operator import ParentToNearestBone


def menu_func_center(self, _context):
    self.layout.operator(ParentToNearestBone.bl_idname, text=ParentToNearestBone.bl_label)


def register():
    bpy.utils.register_class(ParentToNearestBone)
    bpy.types.VIEW3D_MT_object_parent.append(menu_func_center)


def unregister():
    bpy.utils.unregister_class(ParentToNearestBone)
    bpy.types.VIEW3D_MT_object_parent.remove(menu_func_center)


if __name__ == '__main__':
    register()

