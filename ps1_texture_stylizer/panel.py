import bpy


class IMAGE_PT_ps1_stylizer(bpy.types.Panel):
    bl_label = "PS1 Texture Stylizer"
    bl_idname = "IMAGE_PT_ps1_stylizer"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "PS1"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.ps1_texture_settings
        layout.prop(settings, "source")
        layout.prop(settings, "resolution")
        layout.prop(settings, "colors")
        layout.prop(settings, "dither")
        if settings.dither != 'NONE':
            layout.prop(settings, "bayer_size")
            layout.prop(settings, "dither_strength")
        layout.prop(settings, "precision")
        layout.prop(settings, "contrast")
        layout.prop(settings, "saturation")
        layout.prop(settings, "brightness")
        layout.prop(settings, "alpha_mode")
        if settings.alpha_mode == 'BINARY':
            layout.prop(settings, "alpha_threshold")
        layout.operator("image.ps1_stylize", icon='IMAGE_DATA')
        row = layout.row(align=True)
        row.operator("image.ps1_export", icon='EXPORT')
        row.operator("image.ps1_create_material", icon='MATERIAL')


def register():
    bpy.utils.register_class(IMAGE_PT_ps1_stylizer)


def unregister():
    bpy.utils.unregister_class(IMAGE_PT_ps1_stylizer)

