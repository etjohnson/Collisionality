import numpy as np


def gen_uncer(
        error_data,
        scalar_temps,
):
    p = 'proton'
    a = 'alpha'
    t_ = error_data[p]['time']

    out_mean = {}
    out_mean[p] = np.zeros(len(t_))
    out_mean[a] = np.zeros(len(t_))

    for i in range(len(t_)):
        temp_p = np.zeros(i + 1)
        temp_a = np.zeros(i + 1)
        for j in range(i):
            temp_p[j] = scalar_temps['proton_1_k'][j]
            temp_a[j] = scalar_temps['alpha_k'][j]
        sd_p = np.std(temp_p)
        sd_a = np.std(temp_a)
        out_mean[p][i] = sd_p / (i + 1)
        out_mean[a][i] = sd_a / (i + 1)

    out_mean[p][0] = out_mean[p][1]
    out_mean[a][0] = out_mean[a][1]

    return out_mean
