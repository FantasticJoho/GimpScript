#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
import math

def sonar_disappearance(image, drawable, num_frames):
    # Assurez-vous qu'il y a exactement 2 calques.
    if len(image.layers) != 2:
        pdb.gimp_message("Ce script requiert exactement 2 calques : un nommé 'foreground' et un calque de fond.")
        return
    
    # Identifier le calque 'foreground' et le calque de fond.
    foreground_layer = None
    background_layer = None
    for layer in image.layers:
        if layer.name.lower() == "foreground":
            foreground_layer = layer
        else:
            background_layer = layer

    if foreground_layer is None:
        pdb.gimp_message("Aucun calque nommé 'foreground' n'a été trouvé. Veuillez renommer le calque en 'foreground' puis réessayez.")
        return

    # On masque seulement le calque 'foreground' d'origine pour ne pas interférer avec l'animation.
    foreground_layer.visible = False
    # Le calque de fond reste visible, de façon à être toujours présent pour se dévoiler derrière le masque.

    # S'assurer que num_frames est un entier.
    num_frames = int(num_frames)

    # Début du groupe d'annulation.
    pdb.gimp_image_undo_group_start(image)
    gimp.progress_init("Création de l'effet sonar...")

    # Récupérer les dimensions de l'image et calculer le centre ainsi que le rayon maximal.
    width = image.width
    height = image.height
    center_x = width // 2
    center_y = height // 2
    max_radius = math.sqrt(center_x**2 + center_y**2)

    # Boucle pour créer des calques avec un masque circulaire croissant sur le 'foreground'.
    for i in range(num_frames):
        gimp.progress_update(float(i) / num_frames)

        # Calcul du rayon actuel (progression linéaire ; ajustez pour un easing non linéaire).
        radius = int((i / float(num_frames)) * max_radius)

        # Dupliquer le calque 'foreground'.
        new_layer = pdb.gimp_layer_copy(foreground_layer, True)
        image.add_layer(new_layer, 0)  # Ajout en haut de la pile (les nouveaux calques se placent ainsi au-dessus du fond).

        # Créer un masque blanc (entièrement visible) pour le nouveau calque.
        mask = pdb.gimp_layer_create_mask(new_layer, ADD_WHITE_MASK)
        new_layer.add_mask(mask)

        # Annuler toute sélection active.
        pdb.gimp_selection_none(image)

        # Sélectionner une ellipse centrée sur (center_x, center_y) avec le rayon calculé.
        pdb.gimp_image_select_ellipse(image, CHANNEL_OP_REPLACE,
                                      center_x - radius, center_y - radius,
                                      2 * radius, 2 * radius)

        # Fixer la couleur de premier plan à noir (pour masquer dans le masque).
        pdb.gimp_context_set_foreground((0, 0, 0))
        pdb.gimp_edit_fill(mask, FOREGROUND_FILL)

        # Désélectionner la sélection.
        pdb.gimp_selection_none(image)

    # Nous n'ajoutons plus de frame final, car le calque de fond est toujours visible en dessous.
    # Ainsi, à travers les zones masquées des calques copies du foreground, le fond est révélé en continue.

    # Mise à jour de l'affichage et fin du groupe d'annulation.
    gimp.displays_flush()
    pdb.gimp_image_undo_group_end(image)

register(
    "sonar_disappearance2",
    "Créer un effet d'effacement sonar avec révélation permanente du fond",
    "Génère des frames à partir du calque 'foreground' avec un masque circulaire expansif qui laisse transparaître le calque de fond en permanence.",
    "Virginie", "GPL", "2025",
    "<Image>/Filters/Animation/Sonar Disappearance with Background Reveal2",
    "*",
    [
        (PF_INT, "num_frames", "Nombre de frames", 20)
    ],
    [],
    sonar_disappearance
)

main()
