#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import math

def python_fu_cross_gif(img, drawable, num_rot_frames, num_open_frames):
    # Disable undo on the source image for performance.
    pdb.gimp_image_undo_disable(img)

    width = img.width
    height = img.height
    mid_x = width // 2
    mid_y = height // 2

    # Duplicate the current image for door-opening copy work.
    source_img = pdb.gimp_image_duplicate(img)
    source_layer = pdb.gimp_image_get_active_layer(source_img)

    # Create a new image to hold all animation frames.
    anim_img = pdb.gimp_image_new(width, height, RGB)
    frames = []  # To keep track of our frame layers

    #### Phase 1: Rotation frames ####
    for i in range(num_rot_frames):
        angle_deg = i * (360.0 / num_rot_frames)
        angle_rad = math.radians(angle_deg)
        # Create a new layer from the original drawable that belongs to anim_img.
        rot_layer = pdb.gimp_layer_new_from_drawable(drawable, anim_img)
        pdb.gimp_image_insert_layer(anim_img, rot_layer, None, -1)
        # Rotate the layer about the center of the image.
        pdb.gimp_item_transform_rotate(rot_layer, angle_rad, True, mid_x, mid_y)
        frames.append(rot_layer)

    #### Phase 2: French-door (cross) opening frames ####
    for i in range(1, num_open_frames + 1):
        factor = float(i) / num_open_frames
        dx = int(factor * mid_x)
        dy = int(factor * mid_y)
        # Create a new transparent layer in anim_img for this frame.
        door_layer = pdb.gimp_layer_new(anim_img, width, height, RGBA_IMAGE, "Door Frame %d" % i, 100, NORMAL_MODE)
        pdb.gimp_image_insert_layer(anim_img, door_layer, None, -1)
        pdb.gimp_image_set_active_layer(anim_img, door_layer)

        # Top-left quadrant:
        pdb.gimp_image_select_rectangle(source_img, CHANNEL_OP_REPLACE, 0, 0, mid_x, mid_y)
        pdb.gimp_edit_copy(source_layer)
        floating_sel = pdb.gimp_edit_paste(door_layer, False)
        pdb.gimp_layer_set_offsets(floating_sel, -dx, -dy)
        pdb.gimp_floating_sel_anchor(floating_sel)

        # Top-right quadrant:
        pdb.gimp_image_select_rectangle(source_img, CHANNEL_OP_REPLACE, mid_x, 0, width - mid_x, mid_y)
        pdb.gimp_edit_copy(source_layer)
        floating_sel = pdb.gimp_edit_paste(door_layer, False)
        pdb.gimp_layer_set_offsets(floating_sel, mid_x + dx, -dy)
        pdb.gimp_floating_sel_anchor(floating_sel)

        # Bottom-left quadrant:
        pdb.gimp_image_select_rectangle(source_img, CHANNEL_OP_REPLACE, 0, mid_y, mid_x, height - mid_y)
        pdb.gimp_edit_copy(source_layer)
        floating_sel = pdb.gimp_edit_paste(door_layer, False)
        pdb.gimp_layer_set_offsets(floating_sel, -dx, mid_y + dy)
        pdb.gimp_floating_sel_anchor(floating_sel)

        # Bottom-right quadrant:
        pdb.gimp_image_select_rectangle(source_img, CHANNEL_OP_REPLACE, mid_x, mid_y, width - mid_x, height - mid_y)
        pdb.gimp_edit_copy(source_layer)
        floating_sel = pdb.gimp_edit_paste(door_layer, False)
        pdb.gimp_layer_set_offsets(floating_sel, mid_x + dx, mid_y + dy)
        pdb.gimp_floating_sel_anchor(floating_sel)

        pdb.gimp_selection_none(source_img)
        frames.append(door_layer)

    # Set the first frame as active.
    pdb.gimp_image_set_active_layer(anim_img, frames[0])
    
    # Instead of saving to disk, display the new image with all frames as layers.
    pdb.gimp_display_new(anim_img)
    
    # Clean up our duplicate source image.
    pdb.gimp_image_delete(source_img)
    
    pdb.gimp_image_undo_enable(img)
    pdb.gimp_message("New animation image created with %d layers." % (len(frames)))

register(
    "python_fu_cross_gif",
    "Generate an animated image with rotating and opening door frames",
    "Creates an animated image where the current image first rotates continuously and then opens into four pieces in a cross layout. The animation frames are added as layers to a new image.",
    "Your Name",
    "Your Name",
    "2025",
    "<Image>/Filters/Animation/Cross GIF (Layers Only)",
    "*",
    [
        (PF_INT, "num_rot_frames", "Number of rotation frames", 72),
        (PF_INT, "num_open_frames", "Number of door opening frames", 20)
    ],
    [],
    python_fu_cross_gif)

main()
