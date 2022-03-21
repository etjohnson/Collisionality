import sys
import numpy as np
from core.constants import const
import matplotlib.pyplot as plt
from scipy.stats import norm

from features.smooth import smooth

def tr(
    time_,
    np0_,
    tp0_,
    vrp0_,
    na0_,
    theta_,
    wind_radius,
    psp_radius,
    fast = True,
):
    duration = len(time_)

    # Normalisation Constant
    Norm =  2.6*(10**1)

    # Initial proton conidition and decay power.
    np0 = np0_
    nppower = -1.8

    #Initial proton tempreture and decay power.
    tp0 = tp0_
    tppower = -0.74

    # Average velocity and decay power
    vrp0 = vrp0_
    vrppower = -0.2

    #Alpha particle parameters
    ua = 4
    za = 2

    # Inital alpha condition and decay power.
    na0 = na0_
    napower =  -1.8

    n = np.zeros(duration)

    for i in range(duration):
        if np0[i] == 0:
            n[i] = 0
        else:
            n[i] = na0[i]/np0[i]

    #Compute#

    final_aps = np.zeros(duration)

    if fast == True:
        sum_range = 50
        print('Radial prediction computing: Fast mode.')
    else:
        sum_range = duration
        print('Radial prediction computing: Note time for computation may be excessive.')

    for j in range(sum_range):
        constant = (ua**0.5)*(za**2)

        # Define parameters
        L = wind_radius[j] - psp_radius[j]
        l = psp_radius[j]
        # Step size
        h = (1 - l)/(10)
        # Create the numerical grid
        R = np.arange(l, 1, h)

        # Explicit Euler Method
        if theta_[j] > 15:
            s_ = 15
        else:
            s_ = theta_[j]

        for k in range(0,len(R) - 1):
            Tp = (tp0[j])*(R[k]**tppower)
            ndp = (np0[j])*(R[k]**nppower)
            vrp = (vrp0[j])*(R[k]**vrppower)
            nap = (n[j])*(R[k]**(napower-nppower))

            equ_one = Norm*(ndp/(vrp*(Tp**1.5)))*(((constant)/((ua + s_)**1.5)))*(1-s_)*(1+nap*s_)
            equ_two = (9+ np.log(((Tp**1.5)/(ndp**0.5))*((ua + s_)/(za*(1 + ua)))*((1 +((za*za*nap)/(s_)))**(-0.5))))
            s_ = s_ + h*equ_one*equ_two

        final_aps[j] = s_
        print(f"{(j/sum_range)*100:.2f} %", end="\r")

    print(final_aps)

    weights = np.ones_like(final_aps)/float(len(final_aps))

    plt.figure(figsize=(const.x_dim,const.y_dim))
    plt.title('Histogram of α-proton relative temperatures', fontsize=24)
    plt.ylabel('Probability density', fontsize=18)
    plt.xlabel('α-proton relative temperature', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    _,bins,_ = plt.hist(smooth(final_aps,50), 150, density=1, alpha=0.75, histtype='step', linewidth=3, fill=False)
    mu, sigma = norm.fit(final_aps)
    best_fit_line = norm.pdf(bins,mu,sigma)
    #plt.plot(bins, best_fit_line)

    #plt.hist(, density=True, bins=50, range=[0, 15], label='MM data modelled')
    plt.grid()
    plt.show()



    return final_aps

