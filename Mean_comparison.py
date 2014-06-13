#!/usr/bin/python
# Mean_comparison.py 

# This should give a box and wisker plot for the upper Sigma, Lower Sigma, and normal rate pertubation runs.

import os
from bpch import bpch
import numpy as np
import datetime
import matplotlib.pyplot as plt

species  = 'SO4'
group    = 'IJ-AVG-$'
debug    = True
month    = '200607' 
Normal_wd   = '/work/home/bn506/Rate_Sensetivity/Batch_runs/HO2_NO_p0/'
#Posative_wd = '/work/home/bn506/Rate_Sensetivity/Batch_runs/HO2_NO_p1/'
Negative_wd = '/work/home/bn506/Rate_Sensetivity/Batch_runs/HO2_NO_n1/'
Output_name = 'Surface_'+ species +'_Boxplot.png'

def main(species, group, debug ):
   
   # Get arguments.
   get_arguments(debug)
   
   normal_data, units, start_time, end_time = get_values( Normal_wd, species, group, month, debug=True )
#   posative_data = get_values( Posative_wd, species, group, month )
   negative_data, units, start_time, end_time = get_values( Negative_wd, species, group, month )   

#   relevant_data = strip_relevant_data(normal_data)
   
#   box_plot( normal_data, posative_data, negative_data )
   box_plot( normal_data, negative_data, units, start_time, end_time )   
   

   print 'Units = ' + str(units)
   return;

#def box_plot( normal_data, posative_data, negative_data, debug=False ):
def box_plot( normal_data, negative_data, units, start_time, end_time, debug=False ):

   plot_title     = 'Surface ' + species +' average between ' + start_time + ' and '  + end_time   
   Y_axis_title   = species +' (' + units + ')'
   Y_axis_size    = 20
   X_axis_size    = 20
   X_axis_title   = 'Rate constant'

   

   # Turn the data into the form needed ( spread, center, flier_high, flier_low)
#   plt.boxplot([np.ravel(relevant_data), np.ravel(posative_data), np.ravel(negative_data)], 0 )
   fig = plt.figure(dpi=120, figsize=(8,16))
#   plt = fig.add_subplot()
   plt.boxplot([np.ravel(normal_data), np.ravel(negative_data)])

   plt.ylabel(Y_axis_title, fontsize = Y_axis_size)
   plt.xlabel(X_axis_title, fontsize = X_axis_size)
   plt.xticks([1,2], ['Normal', '$-\sigma$'])
   plt.grid(axis='y', which='both')
   fig.tight_layout()
   plt.title( plot_title, fontsize='15')
   fig.savefig( Output_name, transparent=True )

def get_values( wd, species, group, month, debug=False ):
   print 'Extracting data from the bpch.'
   bpch_fname  = wd + month +  ".ctm.bpch"
   print str(bpch_fname)
   bpch_data   = bpch(bpch_fname)
   if debug:
      print 'Data groups:'
      print bpch_data.groups
      print 'Group species:'
      print bpch_data.groups[group].variables

   species_data   =  bpch_data.groups[group].variables[species]
   # Extract only the data which is in the troposphere.
# This gives us lots of zeroes, which is bad.
   time_in_trop   =  bpch_data.groups['TIME-TPS'].variables['TIMETROP']
   species_data   =  np.multiply(species_data[:,:38,:,:], time_in_trop)
# Trying surface ozone instead of tropospheric ozone
   species_data   = species_data[0,0,:,:]


   units          =  bpch_data.groups[group].variables[species].units
   start_time     =  bpch_data.groups[group].variables['tau0']
   end_time       =  bpch_data.groups[group].variables['tau1']

   start_time, end_time = extract_month(start_time, end_time)

   return species_data, units, start_time, end_time;
def strip_relevant_data(species_data):

   boxplot = {}
   ### This needs changing to max in the troposphere
   boxplot['max_point'     ]= np.amax(species_data)
   boxplot['min_point'     ]= np.amin(species_data)
   boxplot['mean_point'    ]= np.mean(species_data)
   boxplot['lower_quartile']= np.percentile(species_data,25)
   boxplot['median_point'  ]= np.percentile(species_data,50)
   boxplot['upper_quartile']= np.percentile(species_data,75)

   if debug:
      print 'Max point        = ' + str(boxplot['max_point'])
      print 'Min point        = ' + str(boxplot['min_point'])
      print 'Mean point       = ' + str(boxplot['mean_point'])
      print 'Upper quartile   = ' + str(boxplot['upper_quartile'])
      print 'Median point     = ' + str(boxplot['median_point'])
      print 'Lower quartile   = ' + str(boxplot['lower_quartile'])
   
   return boxplot;


def extract_month( start_time, end_time ):
   # Turn time from hours from the equinox to YYYY-MM-DD
   epoch = datetime.datetime(1985,1,1)
   start_time     = epoch +  datetime.timedelta(hours=start_time[0])
   end_time       = epoch +  datetime.timedelta(hours=end_time[0])
   # Obtain only the date
   start_time  = str(start_time.date())
   end_time    = str(end_time.date())
   
   return start_time, end_time;

def get_arguments(debug=False):

   clear_screen()
   species = 'O3'
   

   
def clear_screen():
   os.system('cls' if os.name == 'nt' else 'clear')
   return

main(species, group, debug)
