#!/usr/bin/python
# Mean_comparison.py 

# This should give a box and wisker plot for the upper Sigma, Lower Sigma, and normal rate pertubation runs.

import os
from bpch import bpch
import numpy as np
import datetime
import matplotlib.pyplot as plt

species1  = 'O3'
species2  = 'H2O2'
species3 = 'NO3'
group1    = 'IJ-AVG-$'
group2   ='IJ-AVG-$'
group3   ='IJ-AVG-$'
debug    = True
month    = '200607' 
Normal_wd   = '/work/home/bn506/Rate_Sensetivity/Batch_runs/HO2_NO_p0/'
#Posative_wd = '/work/home/bn506/Rate_Sensetivity/Batch_runs/HO2_NO_p1/'
Negative_wd = '/work/home/bn506/Rate_Sensetivity/Batch_runs/HO2_NO_n1/'
Output_name = 'Surface_Fractional_difference_Boxplot.png'

def main(species1, species2, species3, debug ):
   
   # Get arguments.
   get_arguments(debug)
   
   normal_species1_data, units, start_time, end_time = get_values( Normal_wd, species1, group1, month, debug=True )
#   posative_data = get_values( Posative_wd, species, group, month )
   negative_species1_data, units, start_time, end_time = get_values( Negative_wd, species1, group1, month )   
   
   normal_species2_data, units, start_time, end_time = get_values( Normal_wd, species2, group2, month, debug=True )
   negative_species2_data, units, start_time, end_time = get_values( Negative_wd, species2, group2, month )   

   normal_species3_data, units, start_time, end_time = get_values( Normal_wd, species3, group3, month, debug=True )
   negative_species3_data, units, start_time, end_time = get_values( Negative_wd, species3, group3, month )   
   

   species1_data = get_fractional_difference( normal_species1_data, negative_species1_data, debug=debug )
   species2_data = get_fractional_difference( normal_species2_data, negative_species2_data, debug=debug )
   species3_data = get_fractional_difference( normal_species3_data, negative_species3_data, debug=debug )
   
#   species_data = [species1_fractional_difference, species1_fractional_difference,species1_fractional_difference]
   

#   absolute_difference  = get_absolute_difference( normal_data, negative_data, debug=debug)
#   relevant_data = strip_relevant_data(normal_data)
   
#   box_plot( normal_data, posative_data, negative_data )
   box_plot(   species1_data, species2_data, species3_data, units, start_time, end_time )   
   

   print 'Units = ' + str(units)
   return;

def get_fractional_difference( data1, data2, debug=False):
   data = 100 * ((data2 - data1) / data1)
   return data;

def get_absolute_difference( data1, data2, debug=False):
   data = data1-data2
   return data;
   

#def box_plot( normal_data, posative_data, negative_data, debug=False ):
def box_plot( species1_data, species2_data, species3_data, units, start_time, end_time, debug=False ):

#   plot_title     = 'Surface ' + species +' average between ' + start_time + ' and '  + end_time   
   Y_axis_title   = 'fractional difference ( % )'
   Y_axis_size    = '30'
   X_axis_size    = '30'
   X_axis_title   = 'Species'
   Tick_Size      =  '25'
   

   # Turn the data into the form needed ( spread, center, flier_high, flier_low)
#   plt.boxplot([np.ravel(relevant_data), np.ravel(posative_data), np.ravel(negative_data)], 0 )
   fig = plt.figure(dpi=120, figsize=(8,16))
#   plt = fig.add_subplot()
   plt.boxplot([np.ravel(species1_data), np.ravel(species2_data), np.ravel(species3_data)])

   plt.ylabel(Y_axis_title, fontsize = Y_axis_size)
   plt.xlabel(X_axis_title, fontsize = X_axis_size)
   plt.xticks([1, 2, 3], [species1, species2, species3])
   plt.grid(axis='y', which='both')
   plt.tick_params(axis='both', which='major', labelsize=Tick_Size)
   fig.tight_layout()
#   plt.title( plot_title, fontsize='15')
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

main(species1, species2, species3, debug)
