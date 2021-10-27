#!/usr/bin/env python

from gimpfu import *

def convert_layers(image, drawable, linear, copy_layer):
    
    pdb.gimp_image_undo_group_start(image)

    pdb.gimp_selection_none(image)
    for i, layer in enumerate(image.layers[:]):
        if copy_layer:
            name = layer.name
            layer = pdb.gimp_layer_copy(layer, True)
            layer.name = "%s-Dark" %name
            image.add_layer(layer, 2 * i)
        pdb.gimp_image_set_active_layer(image, layer)
        pdb.gimp_drawable_invert(layer, linear)
        pdb.gimp_image_select_color(image, 2, layer, (0,0,0))
        if not pdb.gimp_selection_is_empty(image):
            pdb.gimp_drawable_edit_fill(layer, 0)
        pdb.gimp_selection_none(image)

    pdb.gimp_image_undo_group_end(image)
    
    gimp.displays_flush()

def convert_linear(image, drawable):
    convert_layers(image, drawable, True, False)

def convert_linear_copy_layer(image, drawable):
    convert_layers(image, drawable, True, True)

def convert_normal(image, drawable):
    convert_layers(image, drawable, False, False)

def convert_normal_copy_layer(image, drawable):
    convert_layers(image, drawable, False, True)

def combine_hide(image, drawable):
    pdb.gimp_image_undo_group_start(image)

    active_layer = pdb.gimp_image_get_active_layer(image)
    if pdb.gimp_item_get_visible(active_layer):
        pdb.gimp_image_merge_down(image, active_layer, 2)
        active_layer = pdb.gimp_image_get_active_layer(image)
        pdb.gimp_item_set_visible(active_layer, False)
        for i, layer in enumerate(image.layers):
            if layer == active_layer:
                if len(image.layers) > i + 1:
                    pdb.gimp_image_set_active_layer(image, image.layers[i + 1])
                break
    pdb.gimp_selection_none(image)

    pdb.gimp_image_undo_group_end(image)

def show_all(image, drawable):
    pdb.gimp_image_undo_group_start(image)

    for layer in image.layers:
        pdb.gimp_item_set_visible(layer, True)
        
    pdb.gimp_image_undo_group_end(image)
    
def stack_layer(image, drawable):
    pdb.gimp_image_undo_group_start(image)

    pos_y = 0
    height = image.layers[0].height
    for layer in image.layers[1:]:
        layer.set_offsets(0, pos_y - height)
        pos_y -= height
        height = layer.height

    pdb.gimp_image_undo_group_end(image)

    pdb.gimp_image_resize_to_layers(image) 

register(
    "pdf-dark-convert-linear",
    "Convert layers into dark mode",
    "Converte layers into dark mode by using linear revers and adjust the background color to the chosen color",
    "Rivin (https://github.com/RivinHD)",
    "Copyright 2021 Rivin",
    "2021",
    "<Image>/PDF/Convert Dark (Linear)",
    "*",
    [],
    [],
    convert_linear
)

register(
    "pdf-dark-convert-linear-copy",
    "Copy layers and convert into dark mode",
    "Copy layers and convert into dark mode by using linear revers and adjust the background color to the chosen color",
    "Rivin (https://github.com/RivinHD)",
    "Copyright 2021 Rivin",
    "2021",
    "<Image>/PDF/Convert Dark (Linear) - Copy",
    "*",
    [],
    [],
    convert_linear_copy_layer
)

register(
    "pdf-dark-convert",
    "Convert layers into dark mode",
    "Converte layers into dark mode by using revers and adjust the background color to the chosen color",
    "Rivin (https://github.com/RivinHD)",
    "Copyright 2021 Rivin",
    "2021",
    "<Image>/PDF/Convert Dark",
    "*",
    [],
    [],
    convert_normal
)

register(
    "pdf-dark-convert-copy",
    "Copy layers and convert into dark mode",
    "Copy layers and convert into dark mod by using revers and adjust the background color to the chosen color",
    "Rivin (https://github.com/RivinHD)",
    "Copyright 2021 Rivin",
    "2021",
    "<Image>/PDF/Convert Dark - Copy",
    "*",
    [],
    [],
    convert_normal_copy_layer
)

register(
    "pdf-dark-merge-hide",
    "Merge Layer and Hide",
    "Merge the Layer with the next, hide the Layer and select the next Layer if possible",
    "Rivin (https://github.com/RivinHD)",
    "Copyright 2021 Rivin",
    "2021",
    "<Image>/PDF/Merge Hide",
    "*",
    [],
    [],
    combine_hide
)

register(
    "pdf-dark-show-all",
    "Show all Layers",
    "Show all Layers",
    "Rivin (https://github.com/RivinHD)",
    "Copyright 2021 Rivin",
    "2021",
    "<Image>/PDF/Show Layers",
    "*",
    [],
    [],
    show_all
)

register(
    "pdf-dark-stack-layer",
    "Stack all Layers",
    "Stack all Layers",
    "Rivin (https://github.com/RivinHD)",
    "Copyright 2021 Rivin",
    "2021",
    "<Image>/PDF/Stack Layers",
    "*",
    [],
    [],
    stack_layer
)
main()