#-------------------------------------------------------------------------------
# LOAD THE NECESSARY MODULES.
#-------------------------------------------------------------------------------


from math import *
from numpy import *

import scipy.stats
import scipy.optimize

import matplotlib
import matplotlib.pyplot


import sys

sys.path.insert( 0, '/media/omnia/active/research/code/python' )

from bam_dvapmulti import *
from bam_plot import *
from bam_progbar import *



#-------------------------------------------------------------------------------
# DEFINE THE FUNCTION FOR CALCULATING A MAXWELLIAN DISTRIBUTION.
#-------------------------------------------------------------------------------


def maxwell( x, r, m, s ) :

	return ( r / ( s*sqrt(pi) ) ) * exp( - (x-m)**2 / (2*(s**2)) )



#-------------------------------------------------------------------------------
# DEFINE THE FUNCTION FOR CALCULATING $\theta_{\alpha p}(r_1)$.
#-------------------------------------------------------------------------------


def theta_ap_0( r_0, r_1, n_p_1, eta_ap, v_p_1, t_p_1, theta_ap_1,
                show_bar=False, n_step=1000                        ) :


	# Initialize the alpha-proton charge and mass ratios.

	z_a  = 2.
	mu_a = 4.


	# Initialize.

	d_r = ( r_0 - r_1 ) / ( 1. * n_step )

	r        = r_1
	n_p      = n_p_1
	v_p      = v_p_1
	t_p      = t_p_1
	theta_ap = theta_ap_1

	theta_ap_min =   0.01
	theta_ap_max = 100.

	try :
		is_list_like = True
		temp = eta_ap[0]
	except :
		is_list_like = False


	# Loop.

	if ( show_bar ) :
		bar = progbar( 25, n_step )

	for i in range( n_step ) :

		if ( show_bar ) :
			bar.increment()

		r = r_1 + ( (i+1) * d_r )

		n_p = n_p_1 * ( r / r_1 )**-1.8
		v_p = v_p_1 * ( r / r_1 )**-0.2
		t_p = t_p_1 * ( r / r_1 )**-0.77

		lambda_ap = 9 - log( ( n_p**0.5 / t_p**1.5                      )      *
		                     ( z_a * ( mu_a + 1 ) / ( theta_ap + mu_a ) )      *
		                     ( 1 + ( z_a**2 * eta_ap / theta_ap )       )**0.5   )

		d_theta_ap = ( ( -2.60e7                                               ) *
		               ( ( n_p / ( v_p * t_p**1.5 ) )                          ) *
		               ( mu_a**0.5 * z_a**2 / ( eta_ap + 1 )**2.5              ) *
		               ( ( theta_ap - 1. ) * ( eta_ap * theta_ap + 1. )**2.5 /
		                 ( theta_ap + mu_a )**1.5                              ) *
		               ( lambda_ap                                             ) *
		               ( d_r                                                   )   )

		theta_ap = theta_ap + d_theta_ap

		if ( is_list_like ) :
			tk_i = where( theta_ap < theta_ap_min )
			theta_ap[tk_i] = theta_ap_min
		else :
			theta_ap = max( [ theta_ap, theta_ap_min ] )

		if ( is_list_like ) :
			tk_i = where( theta_ap > theta_ap_max )
			theta_ap[tk_i] = theta_ap_max
		else :
			theta_ap = min( [ theta_ap, theta_ap_max ] )

	if ( show_bar ) :
		del bar


	# Return.

	return theta_ap



#-------------------------------------------------------------------------------
# LOAD THE "dvapmulti" DATA.
#-------------------------------------------------------------------------------


# Load the "dvapmulti" data.

dat = load_dvapmulti( )



#-------------------------------------------------------------------------------
# DEFINE THE GENERAL SETTINGS.
#-------------------------------------------------------------------------------


# Define the general histogram and plot settings.

n_bin_x = 100

ret_loc  = True
plot_pdf = True

xlim = [ 0.00, 10.00 ]
ylim = [ 0.00,  0.45 ]

xscale = 'linear'
yscale = 'linear'

linewidth = 0.75

inch_plot_x = 2.40
inch_plot_y = 2.40

inch_mrgn_left   = 0.40
inch_mrgn_right  = 0.10
inch_mrgn_bottom = 0.40
inch_mrgn_top    = 0.10

size_xticks = 'x-small'
size_yticks = 'x-small'
size_xlabel = 'x-small'
size_ylabel = 'x-small'

size_txt = 'x-small'

xlabel = r'$\alpha\textrm{-}\rm{Proton}\ \rm{Relative}\ \rm{Temperature}\ $'
ylabel = r'$\rm{Probability}\ \rm{Density}$'

xtick_val = arange( 11 )
xtick_str = [ '$0$', '', '$2$', '', '$4$', '',
	                 '$6$', '', '$8$', '', '$10$' ]

ytick_val = [ 0.05 * i for i in range( 9 ) ]
ytick_str = [ '$0.0$', '', '$0.1$', '', '$0.2$', '',
	                                '$0.3$', '', '$0.4$' ]



#-------------------------------------------------------------------------------
# GENERATE A HISTOGRAM OF THE $\theta_{\alpha p}$ AND ITS COMPONENTS.
#-------------------------------------------------------------------------------


# Define the plot settings (beyond those defined above).

color_tot = 'k'
color_per = 'r'
color_par = 'b'

linestyle_tot = '-'
linestyle_per = '--'
linestyle_par = ':'


# Calculate and plot the normalized histograms.

ret = plot_histo_1d( dat['tatp'],
                     n_bin_x=n_bin_x,
                     plot_pdf=plot_pdf, ret_loc=ret_loc,
                     xscale=xscale, xlabel=xlabel, xlim=xlim,
                     yscale=yscale, ylabel=ylabel, ylim=ylim,
                     linewidth=linewidth,
                     linestyle=linestyle_tot,
                     color=color_tot,
                     inch_plot_x=inch_plot_x, 
                     inch_plot_y=inch_plot_y,
                     inch_mrgn_left=inch_mrgn_left,
                     inch_mrgn_right=inch_mrgn_right,
                     inch_mrgn_bottom=inch_mrgn_bottom,
                     inch_mrgn_top=inch_mrgn_top,
                     size_xticks=size_xticks,
                     size_yticks=size_yticks,
                     size_xlabel=size_xlabel,
                     size_ylabel=size_ylabel                  )

ret_hst_par = calc_histo_1d( dat['t_par_a']/dat['t_par_p'],
                             ret_pdf=True, ret_loc=True,
                             n_bin_x=n_bin_x,
                             xscale=xscale, xlim=xlim       )

ret_hst_per = calc_histo_1d( dat['t_per_a']/dat['t_per_p'],
                             ret_pdf=True, ret_loc=True,
                             n_bin_x=n_bin_x,
                             xscale=xscale, xlim=xlim       )

ret_plt_per = plot_line( ret_hst_per['loc_x'], ret_hst_per['pdf_x'],
                         linewidth=linewidth, linestyle=linestyle_per,
                         color=color_per, use_plt=ret['plt']           )


ret_plt_par = plot_line( ret_hst_par['loc_x'], ret_hst_par['pdf_x'],
                         linewidth=linewidth, linestyle=linestyle_par,
                         color=color_par, use_plt=ret['plt']           )


# Add in a key.

plot_line( [4.0,5.0], [0.40,0.40],
           linewidth=linewidth, linestyle=linestyle_tot,
           color=color_tot, use_plt=ret['plt']           )
plot_line( [4.0,5.0], [0.36,0.36],
           linewidth=linewidth, linestyle=linestyle_per,
           color=color_per, use_plt=ret['plt']           )
plot_line( [4.0,5.0], [0.32,0.32],
           linewidth=linewidth, linestyle=linestyle_par,
           color=color_par, use_plt=ret['plt']           )

txt_key_par = r'$\theta_{\parallel\alpha p} \equiv T_{\parallel\alpha}\,/\,T_{\parallel p}$'
txt_key_per = r'$\theta_{\perp\alpha p} \equiv T_{\perp\alpha}\,/\,T_{\perp p}$'
txt_key_tot = r'$\theta_{\alpha p} \equiv T_\alpha/T_p$'

ret['plt'].annotate( txt_key_tot, (5.4,0.40),
                     size=size_txt, color=color_tot,
                     horizontalalignment='left',
                     verticalalignment='center'      )
ret['plt'].annotate( txt_key_per, (5.4,0.36),
                     size=size_txt, color=color_per,
                     horizontalalignment='left',
                     verticalalignment='center'      )
ret['plt'].annotate( txt_key_par, (5.4,0.32),
                     size=size_txt, color=color_par,
                     horizontalalignment='left',
                     verticalalignment='center'      )


# Adjust frame thickness.

[ i.set_linewidth( 0.5 ) for i in ret['plt'].spines.itervalues( ) ]


# Adjust the tick marks.

ret['plt'].set_xticks( xtick_val )
ret['plt'].set_yticks( ytick_val )

ret['plt'].set_xticklabels( xtick_str )
ret['plt'].set_yticklabels( ytick_str )


# Fit the normalized histogram.

x_p_1 = 0.50
x_p_2 = 1.20

x_q_1 = 3.50
x_q_2 = 5.00

h_p = max( ret['pdf_x'][ where( ( ret['loc_x'] >= x_p_1 ) &
                                ( ret['loc_x'] <= x_p_2 )   ) ] )
h_q = max( ret['pdf_x'][ where( ( ret['loc_x'] >= x_q_1 ) &
                                ( ret['loc_x'] <= x_q_2 )   ) ] )

tk_p = where( ( ret['loc_x'] >= x_p_1 ) &
              ( ret['loc_x'] <= x_p_2 )   )

tk_q = where( ( ret['loc_x'] >= x_q_1 ) &
              ( ret['loc_x'] <= x_q_2 )   )

p0 = [ 0.1, 1.0, 0.2 ]
q0 = [ 0.4, 4.0, 2.0 ]

p_opt, p_cov = \
     scipy.optimize.curve_fit( maxwell, ret['loc_x'][tk_p],
                                        ret['pdf_x'][tk_p], p0=p0 )
q_opt, q_cov = \
     scipy.optimize.curve_fit( maxwell, ret['loc_x'][tk_q],
                                        ret['pdf_x'][tk_q], p0=q0 )


# Annotate the histogram with the fit.

ret['plt'].plot( [ p_opt[1], p_opt[1] ], [ 0.00, h_p+0.030 ],
                 color='k', linewidth=0.5, linestyle='-'      )

ret['plt'].plot( [ q_opt[1], q_opt[1] ], [ 0.00, h_q+0.030 ],
                 color='k', linewidth=0.5, linestyle='-'      )

txt_p = r'$\theta_{\alpha p} = ' + '{:.1f}$'.format( p_opt[1] )
txt_q = r'$\theta_{\alpha p} = ' + '{:.1f}$'.format( q_opt[1] )

ret['plt'].annotate( txt_p, (p_opt[1]-0.4,h_p+0.035),
                     size=size_txt, color='k',
                     horizontalalignment='left',
                     verticalalignment='bottom'    )

ret['plt'].annotate( txt_q, (q_opt[1]-0.4,h_q+0.035),
                     size=size_txt, color='k',
                     horizontalalignment='left',
                     verticalalignment='bottom'    )


# Save the annotated figure.

save_fig( fname='fig_meas_tcomp', ext_eps=True )



#-------------------------------------------------------------------------------
# CALCULATE AND HISTOGRAM THE VALUES OF $\theta_{\alpha p}(r_0)$ FOR SOME DATA.
#-------------------------------------------------------------------------------


# Select only a subset of the dataset (to avoid pathological cases).

tk = where( dat['tatp'] >= 1.05 )[0]

n_tk = len( tk )

print 100. * ( 1. - ( 1. * len( tk ) / len( dat['tatp'] ) ) )


# Calculate $\theta_{\alpha p}(r_0)$ for the selected spectra.

r_0        =  0.10
r_1        =  1.00
n_p_1      =  dat['n_p'][tk]
eta_ap     =  dat['nanp'][tk]
v_p_1      = -dat['v_x_p'][tk]
t_p_1      =  dat['t_p'][tk]
theta_ap_1 =  dat['tatp'][tk]

theta_ap_0 = \
     theta_ap_0( r_0, r_1, n_p_1, eta_ap, v_p_1, t_p_1, theta_ap_1,
                 show_bar=True, n_step=90                           )


# Define the plot settings (beyond those defined above).

color_01 = 'k'
color_10 = 'g'

linestyle_01 = '-'
linestyle_10 = '-.'


# Plot the histogram of the $\theta_{\alpha p}(0.1\ \rm{AU})$-values.

ret = plot_histo_1d( theta_ap_0,
                     n_bin_x=n_bin_x,
                     plot_pdf=plot_pdf, ret_loc=ret_loc,
                     xscale=xscale, xlabel=xlabel, xlim=xlim,
                     yscale=yscale, ylabel=ylabel, ylim=ylim,
                     linewidth=linewidth,
                     linestyle=linestyle_01,
                     color=color_01,
                     inch_plot_x=inch_plot_x, 
                     inch_plot_y=inch_plot_y,
                     inch_mrgn_left=inch_mrgn_left,
                     inch_mrgn_right=inch_mrgn_right,
                     inch_mrgn_bottom=inch_mrgn_bottom,
                     inch_mrgn_top=inch_mrgn_top,
                     size_xticks=size_xticks,
                     size_yticks=size_yticks,
                     size_xlabel=size_xlabel,
                     size_ylabel=size_ylabel                  )


# Adjust frame thickness.

[ i.set_linewidth( 0.5 ) for i in ret['plt'].spines.itervalues( ) ]


# Adjust the tick marks.

ret['plt'].set_xticks( xtick_val )
ret['plt'].set_yticks( ytick_val )

ret['plt'].set_xticklabels( xtick_str )
ret['plt'].set_yticklabels( ytick_str )


# Also show the distribution of the measured $\theta{\alpha p0}$-values.

ret_hst_org = calc_histo_1d( dat['tatp'],
                             ret_pdf=True, ret_loc=True,
                             n_bin_x=n_bin_x,
                             xscale=xscale, xlim=xlim    )

plot_line( ret_hst_org['loc_x'], ret_hst_org['pdf_x'],
           linewidth=linewidth, linestyle=linestyle_10,
           color=color_10, use_plt=ret['plt']           )


# Add in a key.

plot_line( [5.0,6.0], [0.40,0.40],
           linewidth=linewidth, linestyle=linestyle_01,
           color=color_01, use_plt=ret['plt']           )
plot_line( [5.0,6.0], [0.36,0.36],
           linewidth=linewidth, linestyle=linestyle_10,
           color=color_10, use_plt=ret['plt']           )

txt_key_01 = r'$\theta_{\alpha p}(0.1\ $$\rm{AU}$$)$'
txt_key_10 = r'$\theta_{\alpha p}(1.0\ $$\rm{AU}$$)$'

ret['plt'].annotate( txt_key_01, (6.4,0.40),
                     size=size_txt, color=color_01,
                     horizontalalignment='left',
                     verticalalignment='center'     )
ret['plt'].annotate( txt_key_10, (6.4,0.36),
                     size=size_txt, color=color_10,
                     horizontalalignment='left',
                     verticalalignment='center'     )


# Fit the distribution of $\theta_{\alpha p}(0.1\ \rm{AU})$-values.

h_p = amax( ret['pdf_x'] )

x_h_p = ret['loc_x'][ where( ret['pdf_x'] == h_p )[0][0] ]

tk_p = where( ( ( ret['loc_x'] >= 3.0 ) &
                ( ret['loc_x'] <= 6.0 )   ) )

p0 = [ 0.5, 6.0, 0.5 ]

p_opt, p_cov = scipy.optimize.curve_fit( maxwell, ret['loc_x'][tk_p],
                                                  ret['pdf_x'][tk_p], p0=p0 )


# Annotate the histogram with the fit.

ret['plt'].plot( [ p_opt[1], p_opt[1] ], [ 0.00, h_p+0.030 ],
                 color='k', linewidth=0.5, linestyle='-'      )

txt_p = r'$\theta_{\alpha p} = ' + '{:.1f}$'.format( p_opt[1] )

ret['plt'].annotate( txt_p, (p_opt[1]-0.4,h_p+0.035),
                     size=size_txt, color='k',
                     horizontalalignment='left',
                     verticalalignment='bottom'       )


# Save the figure.

save_fig( fname='fig_comp', ext_eps=True )
