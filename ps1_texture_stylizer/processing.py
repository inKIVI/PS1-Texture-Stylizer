"""Pure image-buffer processing; no third-party modules are required."""

from array import array


def _bayer(size):
    matrix = ((0,),)
    while len(matrix) < size:
        old_size = len(matrix)
        matrix = tuple(
            tuple(
                (4 * matrix[y % old_size][x % old_size] +
                 ((0, 2), (3, 1))[y // old_size][x // old_size])
                for x in range(old_size * 2)
            )
            for y in range(old_size * 2)
        )
    return matrix


BAYER = {size: _bayer(size) for size in (2, 4, 8)}


def _clamp(value):
    return max(0.0, min(1.0, value))


def process_pixels(source, width, height, target, colors, dither, bayer_size, strength,
                   precision, contrast, saturation, brightness, alpha_mode, alpha_threshold):
    """Nearest-resample and process RGBA float pixels from Blender's image buffer."""
    result = array('f', [0.0]) * (target * target * 4)
    matrix = BAYER.get(bayer_size, BAYER[4])
    matrix_size = len(matrix)
    levels = max(2, colors - 1)
    channel_levels = max(2, precision - 1)
    for y in range(target):
        sy = min(height - 1, int((y + 0.5) * height / target))
        for x in range(target):
            sx = min(width - 1, int((x + 0.5) * width / target))
            src = (sy * width + sx) * 4
            dst = (y * target + x) * 4
            r, g, b, a = source[src:src + 4]
            gray = r * 0.2126 + g * 0.7152 + b * 0.0722
            r = gray + (r - gray) * saturation
            g = gray + (g - gray) * saturation
            b = gray + (b - gray) * saturation
            r = (r - 0.5) * contrast + 0.5 + brightness
            g = (g - 0.5) * contrast + 0.5 + brightness
            b = (b - 0.5) * contrast + 0.5 + brightness
            if dither != 'NONE':
                threshold = ((matrix[y % matrix_size][x % matrix_size] + 0.5) /
                             (matrix_size * matrix_size) - 0.5) * strength / levels
                r, g, b = r + threshold, g + threshold, b + threshold
            r = round(_clamp(r) * levels) / levels
            g = round(_clamp(g) * levels) / levels
            b = round(_clamp(b) * levels) / levels
            r = round(r * channel_levels) / channel_levels
            g = round(g * channel_levels) / channel_levels
            b = round(b * channel_levels) / channel_levels
            if alpha_mode == 'BINARY':
                a = 1.0 if a >= alpha_threshold else 0.0
            result[dst:dst + 4] = array('f', (r, g, b, _clamp(a)))
    return result

