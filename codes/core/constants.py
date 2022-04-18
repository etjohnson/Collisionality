# ---Constants & Input---#
import numpy as np
import pathlib
import os


def const(
        enc,
        valid_enc,
):
    # Min and Max Values#
    density_max = 10 ** 25
    density_min = 10 ** -6

    speed_max = 10 ** 3
    speed_min = 0

    b_field_max = 10 ** 8
    b_field_min = 0

    temp_max = 10 ** 6
    temp_min = 0

    chi_squared_max = 5000
    chi_squared_min = 0

    dr_max = 1
    dr_min = 0

    dv_max = 10
    dv_min = 0

    dT_perp_max = 10
    dT_perp_min = 0

    bmag_max = 9900
    bmag_min = 0

    v_gse_max = 99900
    v_gse_min = 0

    dens_add_max = 990
    dens_add_min = 0

    nanp_max = 9
    nanp_min = 0

    presure_max = 90
    presure_min = 0

    c_max = 10 ** 6
    c_min = 0

    const.error_files = False
    const.output = False
    const.scrub = True

    const.x_dim = 10
    const.y_dim = 10

    # ------------------------------------------------------------------------------#

    directory = os.getcwd()
    path = str(pathlib.Path(directory).parent)

    const.str_dir = str(path + "/data/load/")
    const.str_save = str(path + "/data/save/")

    if enc == 0:
        L = len(valid_enc)
        encounter = np.zeros(L)
        const.encounter = []
        for i in range(L):
            encounter[i] = valid_enc[i]
            const.encounter.append('E' + str(int(encounter[i])))
    else:
        L = 1
        encounter = np.zeros(L)
        encounter[0] = enc
        const.encounter = []
        const.encounter.append('E' + str(int(encounter[0])))
    const.num_of_encs = L
    const.encounter_names = []

    for i in range(L):
        val = (const.encounter[i])
        const.encounter_names.append(val + '_protons.csv')
        const.encounter_names.append(val + '_alphas.csv')

    const.sc_names = []
    const.sc_names.append('PSP.csv')
    const.sc_names.append('Wind_Orbit.csv')
    const.sc_names.append('PSP_Orbit.csv')
    const.sc_names.append('Wind_Outside_Range_Hour.csv')
    const.sc_names.append('Wind_Outside_Range_Min.csv')

    const.num_of_sc = len(const.sc_names)

    # ------------------------------------------------------------------------------#

    const.num_files = len(const.encounter_names) + len(const.sc_names)

    const.data_units = {}

    const.data_units[0] = [0, 1, 1, 2, 2, 2, 3, 3, 3, 2, 4, 4, 4, 4]
    const.data_units[1] = [0, 1, 2, 2, 2, 3, 3, 3, 4, 4]

    const.data_units[2] = [0, 5, 1, 8, 8, 5, 5, 5, 1, 8, 6, 7]
    const.data_units[3] = [0, 5, 1, 8, 8, 5, 5, 5, 1, 8, 6, 7]

    const.sc_units = {}

    const.sc_units[0] = [0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 2, 2, 0, 0, 0, 0]
    const.sc_units[1] = [0, 0, 0, 0, 3, 3, 3, 3, 2, 0, 0, 0, 0]

    const.sc_units[2] = [0, 0, 0, 0, 0, 0]
    const.sc_units[3] = const.sc_units[1]
    const.sc_units[4] = [0, 9, 9, 9, 9, 9, 9, 9, 9, 2, 10, 10, 2, 11, 14, 12, 13, 11, 11,
                         11]

    const.var_max = [(10 ** 30), density_max, speed_max, b_field_max, temp_max,
                     chi_squared_max, dr_max, dv_max, dT_perp_max, bmag_max, v_gse_max,
                     dens_add_max, nanp_max, presure_max, c_max]

    const.var_min = [0, density_min, speed_min, b_field_min, temp_min, chi_squared_min,
                     dr_min, dv_min, dT_perp_min, bmag_min, v_gse_min, dens_add_min,
                     nanp_min, presure_min, c_min]

    # ------------------------------------#

    const.title_size = 30
    const.label_size = 24
    const.tick_size = 22
    const.legend_size = 20
    const.font_family = 'sans-serif'

    const.transparent = 0.0  # 0-1
    const.pdf_smooth = 20
    const.arg_smooth = 20

    const.bin_width = 0.02

    const.dp_number = 1
    const.predict = True
    const.R = 0.2
    const.wind_radius = 1

    # ------------------------------------#

    message = 'Note: Constants imported.'

    if const.R > 0.21:
        raise ValueError(
            f"R must be smaller than the largest radius in the data set"
        )
    if const.wind_radius < 0.19:
        raise ValueError(
            f"Wind must have a distance greater than PSP"
        )

    return message
