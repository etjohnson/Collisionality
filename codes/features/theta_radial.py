import math
import sys
import numpy as np
import scipy as scipy
from core.constants import const
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.stats
import scipy.optimize

from features.smooth import smooth


def maxwell(x, r, m, s):
    return (r / (s * np.sqrt(np.pi))) * np.exp(- (x - m) ** 2 / (2 * (s ** 2)))


def theta_ap_0(r_0, r_1, n_p_1, eta_ap, v_p_1, t_p_1, theta_ap_1,
               n_step=1000):
    # Initialize the alpha-proton charge and mass ratios.

    z_a = 2.
    mu_a = 4.

    # Initialise.

    d_r = (r_0 - r_1) / (1. * n_step)

    r = r_1
    n_p = n_p_1
    v_p = v_p_1
    t_p = t_p_1
    theta_ap = theta_ap_1

    theta_ap_min = 0.01
    theta_ap_max = 100.

    try:
        is_list_like = True
        temp = eta_ap[0]
    except:
        is_list_like = False

    # Loop.

    for i in range(n_step):

        r = r_1 + ((i + 1) * d_r)

        n_p = n_p_1 * (r / r_1) ** -1.8
        v_p = v_p_1 * (r / r_1) ** -0.2
        t_p = t_p_1 * (r / r_1) ** -0.77

        arg_ = ((n_p ** 0.5 / t_p ** 1.5) * (z_a * (mu_a + 1) / (theta_ap + mu_a)) *
                (1 + (z_a ** 2 * eta_ap / theta_ap)) ** 0.5)

        if arg_ == 0:
            arg_ = math.exp(9)
        else:
            pass

        lambda_ap = 9 - np.log(arg_)

        d_theta_ap = ((-2.60e7) * ((n_p / (v_p * t_p ** 1.5))) * (
                mu_a ** 0.5 * z_a ** 2 / (eta_ap + 1) ** 2.5) *
                      ((theta_ap - 1.) * (eta_ap * theta_ap + 1.) ** 2.5 / (
                              theta_ap + mu_a) ** 1.5) * (lambda_ap) *
                      (d_r))
        # print(d_theta_ap)
        theta_ap = theta_ap + d_theta_ap

        if (is_list_like):
            tk_i = np.where(theta_ap < theta_ap_min)
            theta_ap[tk_i] = theta_ap_min
        else:
            theta_ap = max([theta_ap, theta_ap_min])

        if (is_list_like):
            tk_i = np.where(theta_ap > theta_ap_max)
            theta_ap[tk_i] = theta_ap_max
        else:
            theta_ap = min([theta_ap, theta_ap_max])


    return theta_ap
