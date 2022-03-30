import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
from core.constants import const
import scipy
import numpy as np

from . import theta_radial as the_rad
from . import smooth as smooth

from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib import pyplot


def graph_function(
        solar_data,
        spc_data,
        scalar_temps,
):
    p = 'proton'
    a = 'alpha'

    X = np.linspace(0, 15, 1000)

    arg_ = smooth(scalar_temps['theta_ap'], const.arg_smooth)

    bins = int((max(arg_) - min(arg_)) / const.bin_width)

    hist = np.histogram(arg_, bins=bins)
    hist_dist = scipy.stats.rv_histogram(hist)

    plt.figure(figsize=(const.x_dim, const.y_dim))
    plt.hist(arg_, density=True, bins=bins, alpha=const.transparent)
    plt.plot(X, smooth(hist_dist.pdf(X), const.pdf_smooth), label=r'$\theta_{\alpha p}( 0.1 - 0.2 \, {\rm AU})$',
             color='black', linewidth=3)
    plt.legend(loc='upper right', prop={'size': const.legend_size})
    plt.title(r'Histogram of $\alpha$-proton relative temperatures', fontsize=const.title_size,
              fontname=const.font_family)
    plt.ylabel('Probability density', fontsize=const.label_size, fontname=const.font_family)
    plt.xlabel(r'$\alpha$-proton relative temperature', fontsize=const.label_size, fontname=const.font_family)
    plt.xticks(fontsize=const.tick_size)
    plt.yticks(fontsize=const.tick_size)
    plt.xlim([0, 15])
    plt.grid()
    plt.show()

    #
    time = solar_data[p]['time']
    density_p = solar_data[p]['np1']
    density_ap = scalar_temps['dens_ap']
    temp = scalar_temps['proton_1_k']
    speed = solar_data[p]['v_mag']
    theta = scalar_temps['theta_ap']
    wind_radius = np.full(shape=len(spc_data[const.sc_names[1]]['time']), fill_value=1, dtype=int)
    psp_radius = np.interp(time, spc_data[const.sc_names[0]]['time'], spc_data[const.sc_names[0]]['RADIAL_DISTANCE_AU'])

    final_theta = theta_loop(time, wind_radius, psp_radius, density_p, density_ap, speed, temp, theta)

    arg_v2 = smooth(final_theta, const.arg_smooth)

    bins_v2 = int((max(arg_v2) - min(arg_v2)) / const.bin_width)

    hist_v2 = np.histogram(arg_v2, bins=bins_v2)
    hist_dist_v2 = scipy.stats.rv_histogram(hist_v2)

    plt.figure(figsize=(const.x_dim, const.y_dim))

    plt.plot(X, smooth(hist_dist.pdf(X), const.pdf_smooth), label=r'$\theta_{\alpha p}( 0.1 - 0.2 \, {\rm AU})$',
             color='blue', linewidth=3, linestyle='dashed')
    plt.plot(X, smooth(hist_dist_v2.pdf(X), const.pdf_smooth), label=r'$\theta_{\alpha p}( 1 \, {\rm AU})$',
             color='black', linewidth=3)
    plt.title(r'Histogram of $\alpha$-proton relative temperatures', fontsize=const.title_size,
              fontname=const.font_family)
    plt.ylabel('Probability density', fontsize=const.label_size, fontname=const.font_family)
    plt.xlabel(r'$\alpha$-proton relative temperature', fontsize=const.label_size, fontname=const.font_family)
    plt.xticks(fontsize=const.tick_size)
    plt.yticks(fontsize=const.tick_size)
    plt.legend(loc='upper right', prop={'size': const.legend_size, 'family': const.font_family})
    plt.xlim([0, 7])
    plt.ylim([0, 0.3])
    plt.grid()
    plt.show()

    return


def theta_loop(
        time,
        wind_radius,
        psp_radius,
        density_p,
        density_ap,
        speed,
        temp,
        theta,
):
    final_theta = np.zeros(len(time))
    for i in range(int(len(time))):
        final_theta[i] = the_rad.theta_ap_0(wind_radius[i], psp_radius[i], density_p[i], density_ap[i], speed[i],
                                            temp[i], theta[i])
        print(f"{(i / len(time)) * 100:.2f} %", end="\r")

    return final_theta


def radius_split(
        solar_data,
        spc_data,
):
    time = solar_data['time']
    dp_number = 3

    for i in range(len(time)):
        arg_ = round(spc_data[const.sc_names[0]][i], dp_number)

    return
