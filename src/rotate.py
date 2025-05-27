#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import math

def python_fu_create_rotated_layers(image, drawable, num_frames):
    # Ensure that at least two frames are provided.
    if num_frames < 2:
        pdb.gimp_message("Please choose at least 2 frames to create a complete rotation.")
        return

    # Begin an undo group so that the operation can be undone with a single action.
    pdb.gimp_image_undo_group_start(image)
    
    # Calculate the rotation increment in degrees.
    rotation_increment = 360.0 / (num_frames - 1)
    
    # Loop through the number of frames.
    for i in range(num_frames):
        # Duplicate the original layer.
        new_layer = pdb.gimp_layer_copy(drawable, True)
        # Add the duplicated layer at the top of the layer stack.
        pdb.gimp_image_add_layer(image, new_layer, 0)
        
        # Calculate the rotation angle for this frame (in degrees and then convert to radians).
        angle_degrees = rotation_increment * i
        angle_radians = math.radians(angle_degrees)
        
        # Determine the center of the layer (pivot).
        center_x = new_layer.width / 2.0
        center_y = new_layer.height / 2.0
        
        # Rotate the new layer around its center.
        pdb.gimp_item_transform_rotate(new_layer, angle_radians, False, center_x, center_y)
    
    # End the undo group and refresh the image display.
    pdb.gimp_image_undo_group_end(image)
    gimp.displays_flush()

# Register the script in GIMP so it will appear in the menu.
register(
    "python_fu_create_rotated_layers",
    "Create Rotated Frames",
    "Duplicates the selected layer to create frames that rotate in equal increments, "
    "ending with a final frame that is identical to the original.",
    "Joho", "Joho", "2025",
    "<Image>/Filters/Animation/Only Rotate",  # Menu location.
    "*",  # Image types.
    [
        (PF_INT, "num_frames", "Number of Frames", 300)
    ],
    [],
    python_fu_create_rotated_layers
)

main()
