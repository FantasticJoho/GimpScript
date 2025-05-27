#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import math

def python_fu_create_rotated_scaled_translated_layers(image, drawable, num_frames):
    # Check for a minimum frame count.
    if num_frames < 2:
        pdb.gimp_message("Please choose at least 2 frames to create a complete transformation.")
        return

    pdb.gimp_image_undo_group_start(image)
    
    # Store the original dimensions of the drawable.
    orig_width  = drawable.width
    orig_height = drawable.height

    # Compute the rotation increment so that the final frame rotates 360°.
    rotation_increment = 360.0 / (num_frames - 1)
    
    # Loop through all the frames.
    for i in range(num_frames):
        # Duplicate the original layer.
        new_layer = pdb.gimp_layer_copy(drawable, True)
        pdb.gimp_image_add_layer(image, new_layer, 0)
        
        # -------- Rotate the Layer --------
        angle_degrees = rotation_increment * i
        angle_radians = math.radians(angle_degrees)
        # Use the layer's center as the pivot.
        center_x = new_layer.width / 2.0
        center_y = new_layer.height / 2.0
        pdb.gimp_item_transform_rotate(new_layer, angle_radians, False, center_x, center_y)
        
        # -------- Scale the Layer --------
        # Compute a linear scale factor: 100% for frame 0 to 20% for the final frame.
        scale_factor = 1.0 - (float(i) / (num_frames - 1)) * (1.0 - 0.2)
        new_width  = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)
        pdb.gimp_layer_scale(new_layer, new_width, new_height, True)
        
        # -------- Reposition the layer --------
        # Move the layer so that its bottom left corner is at the bottom left of the image.
        offset_x = 0
        offset_y = image.height - new_height
        pdb.gimp_layer_set_offsets(new_layer, offset_x, offset_y)
    
    pdb.gimp_image_undo_group_end(image)
    gimp.displays_flush()

# Register the script so it appears in GIMP's menu.
register(
    "python_fu_create_rotated_scaled_translated_layers",
    "Create Rotated, Scaled, and Translated Frames",
    "Duplicates the selected layer over a number of frames. Each duplicate is rotated by an equal increment (ending at 360°), "
    "scaled down linearly from 100% to 20%, and repositioned so that its bottom left aligns with the image's bottom left.",
    "Joho", "Joho", "2025",
    "<Image>/Filters/Animation/Rotate x Scale",  # Menu location.
    "*",  # Image types.
    [
        (PF_INT, "num_frames", "Number of Frames", 300)
    ],
    [],
    python_fu_create_rotated_scaled_translated_layers
)

main()
