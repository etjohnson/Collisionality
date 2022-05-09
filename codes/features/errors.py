import decimal
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

    dR_proton = error_data[p]['dR1']
    dR_alpha = error_data[a]['dR']

    dV_proton = np.zeros(t_)
    dV_alpha = np.zeros(t_)

    dn_proton = error_data[p]['dn1']
    dn_alpha = error_data[a]['dn']

    for i in range(t_):
        dV_proton[i] = np.sqrt(
            error_data[p]['dV1x'][i] ** 2 + error_data[p]['dV1y'][i] ** 2 +
            error_data[p]['dV1z'][i] ** 2)
        dV_alpha[i] = np.sqrt(
            error_data[a]['dVx'][i] ** 2 + error_data[a]['dVy'][i] ** 2 +
            error_data[a]['dVz'][i] ** 2)

    result = {}

    result[p] = {}
    result[p]['temp'] = np.zeros(t_)
    result[p]['R'] = np.zeros(t_)
    result[p]['speed'] = np.zeros(t_)
    result[p]['dens'] = np.zeros(t_)
    result[a] = {}
    result[a]['temp'] = np.zeros(t_)
    result[a]['R'] = np.zeros(t_)
    result[a]['speed'] = np.zeros(t_)
    result[a]['dens'] = np.zeros(t_)

    for i in range(t_):
        result[p]['temp'][i] = dT_proton[i] / scalar_temps['proton_1_k'][i]
        result[a]['temp'][i] = dT_alpha[i] / scalar_temps['alpha_k'][i]
        result[p]['R'][i] = dR_proton[i] / scalar_temps['proton_R'][i]
        result[a]['R'][i] = dR_alpha[i] / scalar_temps['alpha_R'][i]
        result[p]['speed'][i] = dV_proton[i] / solar_data[p]['v_mag'][i]
        result[a]['speed'][i] = dV_alpha[i] / solar_data[a]['v_mag'][i]
        result[p]['dens'][i] = dn_proton[i] / solar_data[p]['np1'][i]
        result[a]['dens'][i] = dn_alpha[i] / solar_data[a]['na'][i]

    return result


def graph_gen(
        data,
):
    p = 'proton'
    a = 'alpha'
    arg_val = 'speed'
    arg_round = 7

    X = np.linspace(0, 15, 1000)

    for i in range(len(data[p][arg_val])):
        data[p][arg_val][i] = round(data[p][arg_val][i], arg_round)
        d = decimal.Decimal(data[a][arg_val][i])
        data[a][arg_val][i] = round(data[a][arg_val][i], arg_round)

    print(data[p][arg_val])

    arg_x, arg_y = np.unique(data[p][arg_val], return_counts=True)
    arg_x_v2, arg_y_v2 = np.unique(data[a][arg_val], return_counts=True)

    print(arg_x, arg_y)

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
    # plt.xlim([0, 10 ** -5])
    # plt.ylim([0, const.y_tick])
    plt.grid()
    plt.show()

    return


def gen_uncer(
        error_data,
        scalar_temps,
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

    sp_av = sum(sig_proton) / len(sig_proton)
    sa_av = sum(sig_alpha) / (len(sig_alpha))

    arg_p = 0
    arg_a = 0
    av_var = {}
    av_var[p] = np.zeros(max_interval)
    av_var[a] = np.zeros(max_interval)
    for i in range(max_interval):
        arg_p = 0
        arg_a = 0
        for j in range(int(interval[i])):
            arg_p = arg_p + sig_proton[j]
            arg_a = arg_a + sig_alpha[j]
        av_var[p][i] = arg_p / interval[i]
        av_var[a][i] = arg_a / interval[i]

    graph_percent(interval, av_var)

    arg_p = sum(av_var[p]) / len(av_var[p])
    arg_a = sum(av_var[a]) / len(av_var[a])

    return round(arg_p, 3), round(arg_a, 3)


def graph_percent(
        interval,
        var,
):
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
    # plt.yscale('log')
    # plt.xlim([7600, 7800])
    # plt.ylim([0, len(interval)])
    plt.show()

    return
