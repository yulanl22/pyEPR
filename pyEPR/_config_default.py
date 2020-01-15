"""
 --- DO NOT MODIFY THIS FILE ---

Default configuration file for pyEPR

This file is NOT meant for users to modify.
Rather, a user should update any config settings they want
in a dictionary called CONFIG in a file called config.py

@author: Zlatko Minev and the pyEPR team
@date: Created on Fri Oct 30 14:21:45 2015
"""

from . import Dict

# If we are reloading the package, then config will already be defined, then do not overwrite it.
__config_defined__ = 'config' in locals()


config = Dict(

    # Folder to save result data to.
    root_dir=r'C:\data-pyEPR',

    ansys=Dict(
        # method_calc_P_mj sets the method used to calculate the participation ratio in eigenmode.
        # Valud values:
        # 	'line_voltage' : Uses the line voltage integral
        # 	'J_surf_mag'   : takes the avg. Jsurf over the rect. Make sure you have seeded
        # 					lots of tets here. I recommend starting with 4 across smallest dimension.
        # 					Multi-junction calculation of energy participation ratio matrix based on <I_J>.
        # 					Current is integrated average of J_surf by default: (zkm 3/29/16)
        # 					Will calculate the Pj matrix for the selected modes for the given junctions
        # 					junc_rect array & length of junctions
        method_calc_P_mj='line_voltage',

        # To save or not the mesh statistics from an HFSS run
        save_mesh_stats=True,
    ),

    # Loss properties of various materials and surfaces
    dissipation=Dict(

        ##################################################
        # Bulk dielectric
        # refs: https://arxiv.org/abs/1308.1743
        #       http://arxiv.org/pdf/1509.01854.pdf
        tan_delta_sapp=1e-6,  # tan(delta) for bulk surface
        epsi=10,    # dielectric

        ##################################################
        # Surface dielectric
        # ref: http://arxiv.org/pdf/1509.01854.pdf

        # Surface dielectric (dirt) thickness
        # units: meters
        th=3e-9,

        # Surface dielectric (dirt) constant
        # units: relative permitivity
        eps_r=10,

        # Surface dielectric (dirt) loss tangent
        # units: unitless, since this is tan(delta)
        tan_delta_surf=1e-3,

        ##################################################
        # Thin-film surface loss
        # units:  Ohms
        # ref:    https://arxiv.org/abs/1308.1743
        surface_Rs=250e-9,

        ##################################################
        # Seam current loss
        # units: per Ohm meter; i.e., seam conductance
        # ref:   http://arxiv.org/pdf/1509.01119.pdf
        gseam=1.0e3,
    ),

    plotting=Dict(
        # Default color map for plottng. Better if made into a string name
        # taken from matplotlib.cm
        default_color_map='viridis',  # pylint: disable=no-member
    ),

    # Not to be used by the user. Just internal
    internal=Dict(

        # Are we using ipython
        ipython=None,

        # Error message for loading packages
        error_msg_missing_import="""\n   If you need a part of pyEPR that uses this package,
        then please install it. Then add it to the system path (if needed).
        See online setup instructions at
        github.com/zlatko-minev/pyEPR""",

        # Warn on missing import
        warn_missing_import=False,
    ),

    # Logging
    log=Dict(

        # '%(name)s - %(levelname)s - %(message)s\n   ::%(pathname)s:%(lineno)d: %(funcName)s\n')
        format='%(asctime)s %(levelname)s [%(funcName)s]: %(message)s',

        datefmt='%I:%M%p %Ss',

        level='INFO'
    )

)


def is_using_ipython():
    """Check if we're in IPython.

    Returns:
        bool -- True if ran in IPython
    """
    try:
        __IPYTHON__  # pylint: disable=undefined-variable, pointless-statement
        return True
    except Exception:
        return False


def get_config():
    """Returns the config pointer.

    If the config is not yet loaded, it will load the defualt config and then
    update it with the config_user.config dictionary.

    Else, it will just return the pointer to the above-updated config, which the
    user could have modified. The modificaitons will be kept.

    Returns:
        Dict : the config dictionary
    """
    if __config_defined__:
        print('Config is already defined.')
        return config

    else:
        # Config is only loaded for the first time, set it up.
        print('First time load of config')

        # Update with user config
        from . import config_user
        config.update(config_user.config)

        # Add to config any bootup params
        config.internal.ipython = is_using_ipython()
        return config


__all__ = ['get_config']