# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
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


import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
                       
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       ) 


#boolean properties that define the passes we want

class EnvironmentProperty(PropertyGroup):
    
                
    Cycles_Passes: BoolProperty(
                name="Cycles",
                description = "make a linked scene with cycles passes and settings",
                default = False
                )            
                
                
    Specular_Passes: BoolProperty(
                name="Specular",
                description = "make a linked shiny shader scene",
                default = False
                )
                
    Shadow_Passes: BoolProperty(
                name="Shadow",
                description = "make a linked white shadow scene",
                default = False
                )

#create an ui mennu to control the procedure

class PassesPanel(bpy.types.Panel):
    """makes a panel"""
    bl_label = "FAKE PASSES GENERATOR"
    bl_idname = "RENDER_PT_MENU"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    
    
    def draw(self, context):
        
        scene = bpy.context.scene
        
        layout = self.layout

        # Create a command button for passes
        row = layout.row().split(factor=0.2)
        row.scale_x = 1.0
        row.scale_y = 2.0
        row.operator("scene.render_passes_add",icon='RENDER_RESULT')
        row.prop(scene.environment_props,"Cycles_Passes")
        row.prop(scene.environment_props,"Specular_Passes")
        row.prop(scene.environment_props,"Shadow_Passes")
        
        row02 = layout.row().split(factor=0.2)
        row02.scale_x = 1.0
        row02.scale_y = 2.0
        row02.operator("scene.update_fake_passes",icon='FILE_REFRESH')


#store classes in tuple
classes = (EnvironmentProperty,PassesPanel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.environment_props = PointerProperty(type=EnvironmentProperty)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.environment_props


