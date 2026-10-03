# 🎮 PS1 Texture Stylizer

Turn a modern image into a small, crisp texture inspired by early 3D games. Choose a resolution, reduce the colors, and add a controllable Bayer dithering pattern.

> **Blender 4.2 or newer.** This is an early version. It creates a new image and keeps your original untouched.

## What it does

- Resizes images to **64 × 64**, **128 × 128**, or **256 × 256** using Nearest Neighbor for sharp pixels.
- Reduces the number of colors and RGB color precision.
- Adds Bayer dithering at 2 × 2, 4 × 4, or 8 × 8, with adjustable strength.
- Adjusts contrast, saturation, and brightness.
- Keeps transparency or converts it to a simple transparent/opaque mask.
- Exports a PNG and can create a Blender material using **Closest** texture filtering.

## Install the add-on

1. On this GitHub page, click **Code → Download ZIP**, then extract the downloaded archive.
2. Open the extracted `PS1-Texture-Stylizer-main` folder, then locate `ps1_texture_stylizer`.
3. Right-click the `ps1_texture_stylizer` folder and compress it into a ZIP file. Keep the folder itself inside the ZIP.
4. In Blender, open **Edit → Preferences → Add-ons**. Open the menu in the top-right and choose **Install from Disk…**.
5. Select the ZIP you just made, then enable **PS1 Texture Stylizer** in the add-ons list.

The ZIP must contain a folder named `ps1_texture_stylizer` with `__init__.py`, `operators.py`, `panel.py`, and `processing.py` inside it.

## Make your first texture

1. Open an image in Blender's **Image Editor**: **Image → Open**.
2. Move your mouse over the Image Editor and press **N** to show its sidebar.
3. Open the **PS1** tab and choose your image in **Source Image**.
4. Choose a resolution and color count. Adjust dithering if you like.
5. Click **Process Texture Copy**. The new image appears in Blender; your original stays unchanged.
6. Click **Export Processed PNG** and choose where to save the result.

### Create a material

After processing, click **Create PS1 Material**. Blender makes a material with the new texture and **Closest** filtering. If a mesh is selected, the material is assigned to it.

## Quick settings tips

- **Chunkier pixels:** try 64 × 64.
- **More detail:** try 128 × 128 or 256 × 256.
- **Fewer colors:** lower **Colors**.
- **More visible dithering:** choose Bayer and raise **Dither Strength** a little.
- **Sprites and leaves:** keep **Alpha** set to **Preserve**. Choose **Binary Threshold** for a hard cutout and adjust **Alpha Threshold**.

## Can't find the PS1 tab?

Make sure the add-on is enabled in **Preferences → Add-ons**, that your image is open in the **Image Editor**, and that you pressed **N** to show the sidebar.

## Notes

The add-on uses Blender and Python's built-in features; no extra packages are needed. Batch processing, saved presets, live preview, noise, and additional effects are not included yet.

Found a problem or have an idea? Open an issue in this repository.

