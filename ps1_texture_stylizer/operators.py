import bpy
from bpy.props import EnumProperty, IntProperty, FloatProperty, PointerProperty
from bpy.types import Operator, PropertyGroup

from .processing import process_pixels


class PS1Settings(PropertyGroup):
    resolution: EnumProperty(name="Output Resolution", items=[('64', "64 × 64", ""), ('128', "128 × 128", ""), ('256', "256 × 256", "")], default='128')
    colors: EnumProperty(name="Colors", items=[(str(n), str(n), "") for n in (4, 8, 16, 32, 64, 128, 256)], default='64')
    dither: EnumProperty(name="Dithering", items=[('NONE', "None", ""), ('BAYER', "Bayer Ordered", "")], default='BAYER')
    bayer_size: EnumProperty(name="Bayer Matrix", items=[('2', "2 × 2", ""), ('4', "4 × 4", ""), ('8', "8 × 8", "")], default='4')
    dither_strength: FloatProperty(name="Dither Strength", min=0.0, max=1.0, default=0.5)
    precision: IntProperty(name="Color Precision (levels/channel)", min=2, max=256, default=32)
    contrast: FloatProperty(name="Contrast", min=0.0, max=2.0, default=1.1)
    saturation: FloatProperty(name="Saturation", min=0.0, max=2.0, default=0.9)
    brightness: FloatProperty(name="Brightness", min=-1.0, max=1.0, default=0.0)
    alpha_mode: EnumProperty(name="Alpha", items=[('PRESERVE', "Preserve", "Keep source alpha"), ('BINARY', "Binary Threshold", "Make alpha transparent or opaque")], default='PRESERVE')
    alpha_threshold: FloatProperty(name="Alpha Threshold", min=0.0, max=1.0, default=0.5)
    source: PointerProperty(name="Source Image", type=bpy.types.Image)


class IMAGE_OT_ps1_process(Operator):
    bl_idname = "image.ps1_stylize"
    bl_label = "Process Texture Copy"
    bl_description = "Create a processed copy and leave the original unchanged"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.ps1_texture_settings
        image = settings.source or context.space_data.image if context.space_data and hasattr(context.space_data, 'image') else settings.source
        if image is None:
            self.report({'ERROR'}, "Choose a source image in the PS1 panel")
            return {'CANCELLED'}
        width, height = image.size
        if width < 1 or height < 1 or image.channels < 3:
            self.report({'ERROR'}, "Source image has no usable RGB pixel buffer")
            return {'CANCELLED'}
        try:
            from array import array
            source = array('f', [0.0]) * (width * height * 4)
            image.pixels.foreach_get(source)
            size = int(settings.resolution)
            pixels = process_pixels(source, width, height, size, int(settings.colors), settings.dither,
                                    int(settings.bayer_size), settings.dither_strength,
                                    settings.precision, settings.contrast, settings.saturation,
                                    settings.brightness, settings.alpha_mode, settings.alpha_threshold)
            output = bpy.data.images.new(f"{image.name}_ps1_{size}", width=size, height=size, alpha=True)
            output.pixels.foreach_set(pixels)
            output.update()
            output.file_format = 'PNG'
            context.scene.ps1_texture_settings.source = output
            context.scene.ps1_last_output = output.name
            self.report({'INFO'}, f"Created {output.name}; original preserved")
        except Exception as exc:
            self.report({'ERROR'}, f"Could not process image: {exc}")
            return {'CANCELLED'}
        return {'FINISHED'}


class IMAGE_OT_ps1_export(Operator):
    bl_idname = "image.ps1_export"
    bl_label = "Export Processed PNG"
    bl_options = {'REGISTER'}
    filepath: bpy.props.StringProperty(subtype='FILE_PATH', default="//texture_ps1.png")
    filter_glob: bpy.props.StringProperty(default="*.png", options={'HIDDEN'})

    def execute(self, context):
        image = bpy.data.images.get(context.scene.ps1_last_output)
        if image is None:
            self.report({'ERROR'}, "Process a texture first")
            return {'CANCELLED'}
        try:
            image.save(filepath=self.filepath, save_copy=True)
        except Exception as exc:
            self.report({'ERROR'}, f"PNG export failed: {exc}")
            return {'CANCELLED'}
        self.report({'INFO'}, f"Saved {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class IMAGE_OT_ps1_material(Operator):
    bl_idname = "image.ps1_create_material"
    bl_label = "Create PS1 Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        image = bpy.data.images.get(context.scene.ps1_last_output)
        if image is None:
            self.report({'ERROR'}, "Process a texture first")
            return {'CANCELLED'}
        material = bpy.data.materials.new(f"{image.name}_Material")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        texture = nodes.new('ShaderNodeTexImage')
        texture.image = image
        texture.interpolation = 'Closest'
        bsdf = nodes.get('Principled BSDF')
        if bsdf:
            material.node_tree.links.new(texture.outputs['Color'], bsdf.inputs['Base Color'])
            alpha_input = bsdf.inputs.get('Alpha')
            if alpha_input:
                material.node_tree.links.new(texture.outputs['Alpha'], alpha_input)
        if context.object and context.object.type == 'MESH':
            if context.object.data.materials:
                context.object.data.materials[0] = material
            else:
                context.object.data.materials.append(material)
        self.report({'INFO'}, f"Created {material.name} with Closest interpolation")
        return {'FINISHED'}


CLASSES = (PS1Settings, IMAGE_OT_ps1_process, IMAGE_OT_ps1_export, IMAGE_OT_ps1_material)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ps1_texture_settings = PointerProperty(type=PS1Settings)
    bpy.types.Scene.ps1_last_output = bpy.props.StringProperty(options={'HIDDEN'})


def unregister():
    del bpy.types.Scene.ps1_last_output
    del bpy.types.Scene.ps1_texture_settings
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

