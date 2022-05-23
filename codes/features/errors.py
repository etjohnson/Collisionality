import numpy as np


def gen_uncer(
        solar_data,
        error_data,
        scalar_temps,
):
    p = 'proton'
    a = 'alpha'
    t = 'time'

    L = len(solar_data[p]['time'])
    days = np.zeros(L)
    for i in range(L):
        days[i] = solar_data[p]['time'][i]/3600

    temp_p = scalar_temps['proton_scalar_temp_1']
    temp_a = scalar_temps['alpha_scalar_temp']

    t_min = int(np.floor(min(days)))
    t_max = int(np.ceil(max(days)))
    n_days = t_max - t_min + 1
    t_interval = 10

    n_interval = int((t_max - t_min) / t_interval)



    out_mean = {}
    time = np.tile(0., [n_days, t_interval])
    out_mean_p = np.tile(0., [n_days, t_interval])
    out_mean_a = np.tile(0., [n_days, t_interval])

    for d in range(n_days):
        tk_d = np.where((days >= (d + t_min)) & (days < (d + t_min + 1)))[0]

        if len(tk_d) < 4:
            continue

        tp_s = temp_p[tk_d]
        ta_s = temp_a[tk_d]
        dy_d = days[tk_d] - (d + t_min)

        for i in range(t_interval):
            tk_i = np.where((dy_d >= ((i + 0.) / t_interval)) &
                            (dy_d < ((i + 1.) / t_interval)))[0]
            if len(tk_i) < 4:
                continue

            out_mean_p[d, i] = np.std(tp_s[tk_i]) / np.mean(tp_s[tk_i])
            out_mean_a[d, i] = np.std(ta_s[tk_i]) / np.mean(ta_s[tk_i])
            time[i] = d

    tk = np.where(out_mean_p > 0)

    p_out = np.median(out_mean_p[tk])*100
    a_out = np.median(out_mean_a[tk])*100
    print(f'Proton uncertainty: {p_out:0.2f} %.')
    print(f'Alpha uncertainty: {a_out:0.2f} %.')

    return time, out_mean_p, out_mean_a
