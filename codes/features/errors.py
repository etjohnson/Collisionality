import os
import numpy as np
from . import smooth as smooth
from core.constants import const
import matplotlib.pyplot as plt
import scipy


def gen_sd(
        solar_data,
        error_data,
        spc_data,
        scalar_temps,
):
    # ---#

    p = 'proton'
    a = 'alpha'
    t_ = len(solar_data[p]['time'])

    dT_proton = error_data[p]['dT1_perp']
    dT_alpha = error_data[a]['dT_perp']

    result = {}

    result[p] = np.zeros(t_)
    result[a] = np.zeros(t_)

    for i in range(t_):
        result[p][i] = dT_proton[i] / scalar_temps['proton_1_k'][i]
        result[a][i] = dT_alpha[i] / scalar_temps['alpha_k'][i]

    return result


def graph_gen(
        data,
):
    p = 'proton'
    a = 'alpha'

    X = np.linspace(0, 15, 1000)

    for i in range(len(data[p])):
        data[p][i] = round(data[p][i], 7)
        data[a][i] = round(data[a][i], 7)

    arg_x, arg_y = np.unique(data[p], return_counts=True)
    arg_x_v2, arg_y_v2 = np.unique(data[a], return_counts=True)

    plt.figure(figsize=(const.x_dim, const.y_dim))

    plt.plot(arg_x, arg_y, label='Proton', color='black', linewidth=2)
    plt.plot(arg_x_v2, arg_y_v2, label=r'$\alpha$', color='blue', linewidth=2)

    plt.legend(loc='upper right', prop={'size': const.legend_size})
    plt.title('Error Graph',
              fontsize=const.title_size,
              fontname=const.font_family)
    plt.ylabel('Number of data', fontsize=const.label_size,
               fontname=const.font_family)
    plt.xlabel(r'$\frac{\sigma}{T}$', fontsize=const.label_size,
               fontname=const.font_family)
    plt.xticks(fontsize=const.tick_size)
    plt.yticks(fontsize=const.tick_size)
    plt.xlim([0, 10 ** -5])
    # plt.ylim([0, const.y_tick])
    plt.grid()
    plt.show()

    return


def gen_uncer(
        error_data,
):
    p = 'proton'
    a = 'alpha'
    t_ = error_data[p]['time']

    max_interval = len(t_)
    interval = np.zeros(max_interval)

    for i in range(max_interval):
        interval[i] = int(i + 1)

    sig_proton = error_data[p]['dT1_perp']
    sig_alpha = error_data[a]['dT_perp']

    sig_tot_p = 0
    sig_tot_a = 0

    for i in range(max_interval):
        sig_tot_a = sig_tot_a + sig_alpha[i]
        sig_tot_p = sig_tot_p + sig_proton[i]

    sp = (sig_tot_p/max_interval)
    sa = (sig_tot_a/max_interval)

    sp = round(sp*100, 2)
    sa = round(sa*10, 2)

    return sp, sa


def graph_percent(
        interval,
        var,
):
    print(interval, var)

    p = 'proton'
    a = 'alpha'

    plt.figure(figsize=(const.x_dim, const.y_dim))

    plt.plot(interval, var[p], label='Proton', color='black', linewidth=2)
    plt.plot(interval, var[a], label=r'$\alpha$', color='blue', linewidth=2)

    plt.legend(loc='upper right', prop={'size': const.legend_size})
    plt.title('Ey',
              fontsize=const.title_size,
              fontname=const.font_family)
    plt.ylabel('y', fontsize=const.label_size,
               fontname=const.font_family)
    plt.xlabel('y', fontsize=const.label_size,
               fontname=const.font_family)
    plt.xticks(fontsize=const.tick_size)
    plt.yticks(fontsize=const.tick_size)
    plt.grid()
    #plt.yscale('log')
    #plt.xlim([7600, 7800])
    plt.ylim([0, len(interval)])
    plt.show()

    return
