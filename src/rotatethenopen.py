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

    # Duplicate the current image for our door-opening work;
    # this ensures our selections do not disturb the user’s image.
    source_img = pdb.gimp_image_duplicate(img)
    source_layer = pdb.gimp_image_get_active_layer(source_img)

    # Create a new image that will hold all the generated frames as layers.
    anim_img = pdb.gimp_image_new(width, height, RGB)
    frames = []  # To keep track of our frame layers

    ##############################
    # Phase 1: 360° Rotation Frames
    ##############################
    for i in range(num_rot_frames):
        angle_deg = i * (360.0 / num_rot_frames)
        angle_rad = math.radians(angle_deg)
        # Create a new layer from the original drawable that belongs to anim_img.
        rot_layer = pdb.gimp_layer_new_from_drawable(drawable, anim_img)
        pdb.gimp_image_insert_layer(anim_img, rot_layer, None, -1)
        # Rotate the layer about the image center.
        pdb.gimp_item_transform_rotate(rot_layer, angle_rad, True, mid_x, mid_y)
        frames.append(rot_layer)

    ############################################
    # Phase 2: French-Door "Cross" Opening Frames
    ############################################
    # In each frame, we split the source image into four quadrants
    # and paste them with offsets so that the effect mimics doors opening.
    for i in range(1, num_open_frames + 1):
        factor = float(i) / num_open_frames
        dx = int(factor * mid_x)
        dy = int(factor * mid_y)
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

    ###################################################################################
    # Phase 3: Create the Final "Locked" Door Frame and Add the Mini 20% Scaled Overlay
    ###################################################################################
    # Duplicate the final door-opening frame (from phase 2).
    final_door_layer = frames[-1]
    locked_layer = pdb.gimp_layer_copy(final_door_layer, True)
    pdb.gimp_image_insert_layer(anim_img, locked_layer, None, -1)
    # Shift the locked layer horizontally by mid_x so that its left side aligns (locks to the left).
    pdb.gimp_layer_translate(locked_layer, mid_x, 0)

    # Create a mini overlay from the original rotated drawable.
    mini_layer = pdb.gimp_layer_new_from_drawable(drawable, anim_img)
    pdb.gimp_image_insert_layer(anim_img, mini_layer, None, -1)
    new_width = int(width * 0.2)
    new_height = int(height * 0.2)
    pdb.gimp_layer_scale(mini_layer, new_width, new_height, True)
    # Place the mini layer at the bottom left of the canvas.
    pdb.gimp_layer_set_offsets(mini_layer, 0, height - new_height)

    # Merge the mini overlay onto the locked door layer to create a final composite frame.
    # (Make sure mini_layer is above locked_layer in the layer stack.)
    final_composite = pdb.gimp_image_merge_down(anim_img, mini_layer, EXPAND_AS_NECESSARY)
    frames.append(final_composite)

    # (Optionally, you could remove or hide the unshifted final door frame if you only want the locked version.)
    pdb.gimp_image_set_active_layer(anim_img, final_composite)

    # Clean up our duplicate copy.
    pdb.gimp_image_delete(source_img)
    pdb.gimp_image_undo_enable(img)
    pdb.gimp_message("New animation image created with %d layers." % (len(frames)))

    # Display the new image with all frames as layers.
    pdb.gimp_display_new(anim_img)

register(
    "python_fu_cross_gif",
    "Generate an animated image with 360 rotation, door opening, locked cross, and mini overlay",
    "Creates an animated image where the current image rotates 360°, then opens up like French doors into a cross layout. In the final open state the image is shifted (locked to the left) and a 20% scaled copy of the rotated image is overlaid at the bottom left.",
    "Joho","Joho","2025",
    "<Image>/Filters/Animation/Crossopen",
    "*",
    [
        (PF_INT, "num_rot_frames", "Number of rotation frames", 200),
        (PF_INT, "num_open_frames", "Number of door opening frames", 60)
    ],
    [],
    python_fu_cross_gif
)

main()
