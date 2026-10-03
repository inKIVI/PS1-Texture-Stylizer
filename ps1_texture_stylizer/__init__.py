"""PS1 Texture Stylizer Blender add-on. Compatible with Blender 4.2+ (tested API target: 4.5 LTS)."""

bl_info = {
    "name": "PS1 Texture Stylizer",
    "author": "OpenAI",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "Image Editor > Sidebar > PS1",
    "description": "Create low-resolution, palette-limited retro texture copies",
    "category": "Image",
}

import bpy

from . import operators, panel


def register():
    operators.register()
    panel.register()


def unregister():
    panel.unregister()
    operators.unregister()


if __name__ == "__main__":
    register()

