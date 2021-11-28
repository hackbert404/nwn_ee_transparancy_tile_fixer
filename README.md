# nwn_ee_transparancy_tile_fixer

Simple python scripts to add a dummy animation to tiles with an animation node. 


# adding dummy animations

Put mdl files in the /in folder.

Run "python add_dummy_animation.py" in the cmd line within the folder.

Or simply double-click on add_dummy_animation.bat.

Files with an animation node but no animations will be copied into the /out folder with the dummy animation added.


# removing dummy animations

Put mdl files in the /in folder.

Run "python remove_dummy_animation.py" in the cmd line within the folder.

Or simply double-click on remove_dummy_animation.bat.

Files with the dummy animation will be copied into the /out folder with the dummy animation removed. 

Note: If the dummy animation was changed in any way, the file will be skipped.
