import sys
import numpy as np
from core.constants import const
import matplotlib.pyplot as plt
from scipy.stats import norm

from features.smooth import smooth

def theta_radial(
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
        
        print('Radial prediction computing: Note time for computation may be excessive.')

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
            n[i] = na0[i]/np0[i]

        #Compute#

        final_aps = np.zeros(duration)
        theta = np.zeros(duration)

        for i in range(duration):
            theta[i] = theta_[i]
            
        if fast == True:
            sum_range =  5000
        else:
            sum_range = duration

        print(sum_range)

        s = {}

        plt.figure(figsize=(const.x_dim, const.y_dim))
        for j in range(sum_range): #duration
            constant = (ua**0.5)*(za**2)

            # Define parameters
            L = wind_radius[j] - psp_radius[j]
            l = psp_radius[j]
            # Step size
            h = (1 - l)/(duration) 
            # Create the numerical grid
            R = np.arange(l, 1, h) 

            #Set up variable functions
            
            s[j] = np.zeros(len(R))
            # Explicit Euler Method
            if theta[j] > 15:
                s[j][0] = 15
                test_s_s = 15
            else:
                s[j][0] = theta[j]
                test_s_s = theta[j]
            
                
            for k in range(0,len(R) - 1):
                Tp = (tp0[j])*(R[k]**tppower)
                ndp = (np0[j])*(R[k]**nppower)
                vrp = (vrp0[j])*(R[k]**vrppower)
                nap = (n[j])*(R[k]**(napower-nppower))
                
                equ_one = Norm*(ndp/(vrp*(Tp**1.5)))*(((constant)/((ua + s[j][k])**1.5)))*(1-s[j][k])*(1+nap*s[j][k])
                #print('Equation 1', equ_one)
                equ_two = (9+ np.log(((Tp**1.5)/(ndp**0.5))*((ua + s[j][k])/(za*(1 + ua)))*((1 +((za*za*nap)/(s[j][k])))**(-0.5))))
                #print('Equation 2', equ_two)
                test_s_s = test_s_s + h*equ_one*equ_two
                #s[j][k + 1] = s[j][k] + h*equ_one*equ_two
                #print('s:', s[i][k+1])

            final_aps[j] = test_s_s#s[j][len(R)-1]
            #plt.plot(R, s[j])

        dumvarstr = str(const.str_dir + '/Predict/Predict' + str(i)+ '.txt')
        np.savetxt(dumvarstr, final_aps, fmt="%s")

        plt.title('Theta against Radius')
        plt.xlabel('r [Au]')
        plt.ylabel('Theta')
        plt.grid()
        #plt.show()
        
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

