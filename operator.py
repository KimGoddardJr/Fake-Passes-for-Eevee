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

import math




#create the fake passes scenes

class PassMaker(bpy.types.Operator):
    """Create multiple fake render passes for a scene"""
    bl_idname = "scene.render_passes_add"
    bl_label = "FAKE PASSES"
    bl_options = {'REGISTER', 'UNDO'}
    #parameters have to be defined that increment the button with the operation
    button_pushed = 0
                    
    def execute(self,context):
        
        master_scene = bpy.context.scene
    
        scene_types = []
        comp_scenes = []
        
        if self.button_pushed == 0:
            
            for key in master_scene.environment_props.keys():
                
                key_value = getattr(master_scene.environment_props,key)
                if key_value == True:
                    
                    scene_types.append(key)
                    
            if len(scene_types) >= 1:
            
                for type in scene_types:
                    comp_scene = bpy.data.scenes.new(master_scene.name+"_{}".format(type))
                    comp_scenes.append(comp_scene)
                        

                #link content to scenes
                for scene in comp_scenes:

                    for coll in master_scene.collection.children:
                        
                        scene.collection.children.link(coll)
                        
                    for obj in master_scene.collection.objects:
                        
                        scene.collection.objects.link(obj)
                        
                        
                SceneSettings()
                        
                                
                self.button_pushed += 1
                self.report({'INFO'}, "You have created scene passes, go to scene display mode in the outliner")
                    
            else:
                self.report({'INFO'}, "You have created absolutely nothing. Check the passes boxes bruh!")
                
        return  {'FINISHED'}



#update the fake passes


class UpdateFakePasses(bpy.types.Operator):
    """update created fake passes"""
    bl_idname = "scene.update_fake_passes"
    bl_label = "UPDATE"
    bl_options = {'REGISTER', 'UNDO'}
      
                    
    def execute(self,context):
        
        master_scene = bpy.context.scene
        
        keys = master_scene.environment_props.keys()    
            
        bitch_scenes = []
        
        bitch = False
        
        for scene in bpy.data.scenes:
            for key in keys:
                
                if "{}_{}".format(master_scene.name,key) in scene.name:
                    bitch_scenes.append(scene)
                    bitch = True
        
        if bitch == True:
            #update scenes
            for scene in bitch_scenes:
                for coll in scene.collection.children:
                    scene.collection.children.unlink(coll)
                for obj in scene.collection.objects:
                    scene.collection.objects.unlink(obj)
                    
                for coll in master_scene.collection.children:
            
                    scene.collection.children.link(coll)

                for obj in master_scene.collection.objects:
            
                    scene.collection.objects.link(obj)
                        
            self.report({'INFO'}, "You have updated the {} fake passes".format(master_scene.name))
        else:
            self.report({'INFO'}, "I regret to inform you that there is nothing to update")

        
        return  {'FINISHED'}  


op_classes = (PassMaker,UpdateFakePasses)

#functions used in classes

#material creation
def DiffuseOverride(name = 'DiffuseOverride'):
    #create new material
    black_override = bpy.data.materials.new(name)
    #activate nodes
    black_override.use_nodes = True
    
    #remove preexisting node
    for shader in black_override.node_tree.nodes:
        if 'Principled BSDF' in shader.name:
            black_override.node_tree.nodes.remove(shader)
    
    #create a 0 emission shader and connect it to the output
    emission_node = black_override.node_tree.nodes.new('ShaderNodeEmission')    
    #make default color black
    emission_node.inputs[0].default_value = (1,1,1,1)
    
    #place nodes
    mat_output = black_override.node_tree.nodes['Material Output']
    mat_x = mat_output.location[0]
    mat_y = mat_output.location[1]
    
    emission_node.location = ((mat_x-450),mat_y-25)
    
    #define input and output
    emission_output = emission_node.outputs[0]
    mat_input = mat_output.inputs[0]
    
    #link the nodes
    black_override.node_tree.links.new(mat_input,emission_output)
    
    return black_override         
        
#settings in scenes 

def PropUpdate():
        
    #default setting
    bpy.context.scene.environment_props.Cycles_Passes = True
    bpy.context.scene.environment_props.Shadow_Passes = True
    bpy.context.scene.environment_props.Specular_Passes = True
       

def SceneSettings():
    
    Cycles_Passes = bpy.context.scene.environment_props.Cycles_Passes
    Shadow_Passes = bpy.context.scene.environment_props.Shadow_Passes
    Specular_Passes = bpy.context.scene.environment_props.Specular_Passes
    
    for scene in bpy.data.scenes:
        
        #set cycles in scene and required passes
        
        if "Cycles_Passes" in scene.name and Cycles_Passes == True and scene.use_nodes == False:
            #set render engine to cycles
            scene.render.engine = 'CYCLES'
            #set cycles render settings
            scene.cycles.samples = 1
            scene.cycles.preview_samples = 1
            scene.cycles.max_bounces = 0
            
            #set filepath to the same as masterscene
            scene.render.filepath = bpy.context.scene.render.filepath+"\\CYCLES\\MASTER_PASSES"
            #render.use_single_layer = True
            #image settings
            image_settings = scene.render.image_settings
            
            image_settings.file_format = 'OPEN_EXR_MULTILAYER'
            image_settings.color_depth = '32'
            image_settings.exr_codec = 'ZIP' 
            
            
            
            for view_layer in scene.view_layers:
                #give the view layer the same name as the scene
                view_layer.name=scene.name
                #turn on cryptomattes
                view_layer.cycles['use_pass_crypto_object'] = True
                view_layer.cycles['use_pass_crypto_material'] = True
                view_layer.cycles['use_pass_crypto_asset'] = True
                view_layer.cycles['pass_crypto_depth'] = 6
                view_layer.cycles['pass_crypto_accurate'] = True
                #layers to render
                #view_layer.use_pass_ambient_occlusion = True
                view_layer.use_pass_uv = True
                view_layer.use_pass_vector = True
                view_layer.use_pass_z = True
                view_layer.use_pass_normal = True
                #render diffuse texture
                view_layer.use_pass_diffuse_color = True
                #set pitchblack material
                #view_layer.material_override = bpy.data.materials[BlackOverride().name]
                
            #https://docs.blender.org/api/current/bpy.types.CompositorNode.html#bpy.types.CompositorNode
            #setup render layer splitting
            scene.use_nodes = True
            #render layer for output
            #render_layers = scene.node_tree.nodes.new('CompositorNodeRLayers')
            render_layers = scene.node_tree.nodes['Render Layers']
            #assign the current scene to Render Layer
            render_layers.scene = scene
            #crypto layer for input
            cryptos = scene.node_tree.nodes.new('CompositorNodeOutputFile')
            cryptos.base_path = scene.render.filepath+'\\CRYPTO\\crypto_'
            cryptos.inputs.remove(cryptos.inputs[0])
            #vector layer for input
            vector_layers = scene.node_tree.nodes.new('CompositorNodeOutputFile')
            vector_layers.base_path = scene.render.filepath+'\\VECTORS\\vector_'
            vector_layers.inputs.remove(vector_layers.inputs[0])
            #depth layer output
            depth = scene.node_tree.nodes.new('CompositorNodeOutputFile')
            depth.base_path = scene.render.filepath+'\\DEPTH\\depth_'
            depth.inputs.remove(depth.inputs[0])
            #AO layer output
            #AO = scene.node_tree.nodes.new('CompositorNodeOutputFile')
            #AO.base_path = scene.render.filepath+'\\AO\\ao_'
            #AO.inputs.remove(AO.inputs[0])
            #DiffCol layer output
            diffcol = scene.node_tree.nodes.new('CompositorNodeOutputFile')
            diffcol.base_path = scene.render.filepath+'\\DIFFUSE\\diffuseColor_'
            diffcol.inputs.remove(diffcol.inputs[0])
            
            #place nodes
            rl_x = render_layers.location[0]
            rl_y = render_layers.location[1]
            
            cryptos.location = (rl_x+500,rl_y-250)
            
            vector_layers.location = (cryptos.location[0],cryptos.location[1]+250)
            
            depth.location = (vector_layers.location[0],vector_layers.location[1]+100)
            
            #AO.location = (cryptos.location[0]+250,cryptos.location[1]+50)
            
            diffcol.location = (cryptos.location[0]+250,cryptos.location[1]+50)
            
            #HQ output settings
            for node in scene.node_tree.nodes:
                 if node.type == 'OUTPUT_FILE':
                     
                     node.format.file_format = 'OPEN_EXR_MULTILAYER'
                     node.format.color_mode = 'RGBA'
                     node.format.color_depth = '32'
                     node.format.exr_codec = 'ZIPS'
                     
            #create as many inputs in 'cryptos' as there are cryptopasses and give them the name
            #https://docs.blender.org/api/current/bpy.types.NodeInputs.html
            #empty array 
            crypto_outputs = []
            vector_outputs = []
            depth_outputs = []
            #ao_outputs = []
            diffcol_outputs = []
            
            for i,output in enumerate(render_layers.outputs):
                if 'Crypto' in output.name:
                    cryptos.file_slots.new(output.name)
                    #append output crypto data to array        
                    crypto_outputs.append(render_layers.outputs[i])
                    
                if output.type == 'VECTOR':
                    vector_layers.file_slots.new(output.name)
                    #append output vector data to array        
                    vector_outputs.append(render_layers.outputs[i])
                    
                if 'Depth' in output.name:
                    depth.file_slots.new(output.name)
                    #append output vector data to array        
                    depth_outputs.append(render_layers.outputs[i])
                    
                #if 'AO' in output.name:
                #   AO.file_slots.new(output.name)
                    #append output vector data to array        
                #  ao_outputs.append(render_layers.outputs[i])
                    
                if 'DiffCol' in output.name:
                    diffcol.file_slots.new(output.name)
                    diffcol_outputs.append(render_layers.outputs[i])
                    
                 
                 #link cryptos     
                for i,cr_input in enumerate(cryptos.inputs):
                
                    scene.node_tree.links.new(cr_input,crypto_outputs[i])
                    
                #link vectors
                for i,v_input in enumerate(vector_layers.inputs):
                
                    scene.node_tree.links.new(v_input,vector_outputs[i])
                    
                #link depths
                for i,d_input in enumerate(depth.inputs):
                
                    scene.node_tree.links.new(d_input,depth_outputs[i])
                    
                #link ao
                #for i,ao_input in enumerate(AO.inputs):
                
                #    scene.node_tree.links.new(ao_input,ao_outputs[i])
                    
                #link diffuse
                for i,diff_input in enumerate(diffcol.inputs):
                
                    scene.node_tree.links.new(diff_input,diffcol_outputs[i])



def register():
    for cls in op_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in op_classes:
        bpy.utils.unregister_class(cls)

