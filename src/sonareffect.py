#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
import math

def sonar_disappearance(image, drawable, num_frames):
    # Ensure exactly 2 layers exist.
    if len(image.layers) != 2:
        pdb.gimp_message("This script requires exactly 2 layers: one named 'foreground' and one background layer.")
        return
    
    # Identify the 'foreground' layer and the background layer.
    foreground_layer = None
    background_layer = None
    for layer in image.layers:
        if layer.name.lower() == "foreground":
            foreground_layer = layer
        else:
            background_layer = layer

    if foreground_layer is None:
        pdb.gimp_message("No layer named 'foreground' found. Please rename the layer to 'foreground' and try again.")
        return

    # Hide the original layers so that only the generated frames appear.
    foreground_layer.visible = False
    background_layer.visible = False

    # Ensure num_frames is an integer.
    num_frames = int(num_frames)

    # Start an undo group.
    pdb.gimp_image_undo_group_start(image)
    gimp.progress_init("Creating sonar effect...")

    # Get image dimensions and calculate the center and maximum radius.
    width = image.width
    height = image.height
    center_x = width // 2
    center_y = height // 2
    max_radius = math.sqrt(center_x**2 + center_y**2)

    # Loop to create layers with an expanding circular mask from the foreground.
    for i in range(num_frames):
        gimp.progress_update(float(i) / num_frames)

        # Calculate current radius (linear progression; for a non-linear easing, adjust here).
        radius = int((i / float(num_frames)) * max_radius)

        # Duplicate the foreground layer.
        new_layer = pdb.gimp_layer_copy(foreground_layer, True)
        image.add_layer(new_layer, 0)

        # Create a white mask (fully visible) for the new layer.
        mask = pdb.gimp_layer_create_mask(new_layer, ADD_WHITE_MASK)
        new_layer.add_mask(mask)

        # Clear any active selection.
        pdb.gimp_selection_none(image)

        # Select an ellipse centered at (center_x, center_y) with the calculated radius.
        pdb.gimp_image_select_ellipse(image, CHANNEL_OP_REPLACE,
                                      center_x - radius, center_y - radius,
                                      2 * radius, 2 * radius)

        # Set the foreground color to black for the mask fill.
        pdb.gimp_context_set_foreground((0, 0, 0))
        pdb.gimp_edit_fill(mask, FOREGROUND_FILL)

        # Deselect the selection.
        pdb.gimp_selection_none(image)

    # Finally, add a frame showing the background layer completely.
    final_frame = pdb.gimp_layer_copy(background_layer, True)
    image.add_layer(final_frame, 0)

    # Update display and end undo group.
    gimp.displays_flush()
    pdb.gimp_image_undo_group_end(image)

register(
    "sonar_disappearance",
    "Create a sonar-like disappearance effect with background reveal",
    "Generates frames from the 'foreground' layer with an expanding circular mask, then adds a final frame revealing the background layer.",
    "Virginie", "GPL", "2025",
    "<Image>/Filters/Animation/Sonar Disappearance with Background Reveal",
    "*",
    [
        (PF_INT, "num_frames", "Number of Frames", 20)
    ],
    [],
    sonar_disappearance
)

main()
