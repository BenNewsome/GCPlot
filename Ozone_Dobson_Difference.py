from bpch import bpch
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import ticker
#import temp_map2D
import os
import datetime
import pygchem.diagnostics as gdiag
import numpy as np
import csv
import glob
import datetime as datetime
import sys

species = 'O3'
group='IJ-AVG-$'
debug=True
month = '200607'

def main(species,group,debug):
   
   wd1,wd2, Output_Name = get_arguments()


   data1, units, start_time, end_time = get_species_data_from_bpch(wd1,species,group, month)
   data2, units, start_time, ent_time = get_species_data_from_bpch(wd2,species,group, month)

   data  = get_difference(data1, data2, debug=debug)   

   if debug:
      print 'raw data dimenstion = ' + str(data.dimensions)


   plot_the_data(data, units, start_time, end_time, Output_Name, debug=debug)
   

   return;

def get_difference(data1, data2, debug=False):
   print 'Caluclating the difference'
   data = 100 * ((data2 - data1) / data1)
   if debug:
      print 'data1 shape = ' + str(data1.shape)
      print 'data2 shape = ' + str(data2.shape)
      print 'data shape  = ' + str(data.shape)

   return data

# Ask for arguments
def get_arguments():
   print 'Getting the arguments.'
   try:
      wd1 =  sys.argv[1]
      wd2 =  sys.argv[2]  
      Output_Name=   sys.argv[3]+'.png'
   except:
      sys.exit('Please input arguments of working dir and output png')
   return wd1, wd2, Output_Name;


def plot_the_data(data, units, start_time, end_time, Output_Name, debug=False):
   print 'Plotting the data.'
   #set up plot
#   print data
#   print data.dimensions
   units = 'DU'
   colourbar_tick_size     = 20
   colourbar_title         = species + '(%'+units+')'
   colourbar_title_size    = 25
   colourbar_number_ticks  = 5
   X_axis_title            = 'Longitude'
   X_axis_size             = 25
   Y_axis_title            = 'Latitude'
   Y_axis_size             = 25
   Plot_title              = '$-\sigma$ difference in ' + species + ' average between '+ str(start_time) + ' and ' + str(end_time)


   # Chose the figure size
   fig=plt.figure(figsize=(20,12))

   ax = fig.add_axes([.05, .1, .9, .8])
   fig.patch.set_facecolor('white')

   # Add the basemap
   lat = np.arange(-88,90,4)
   lat = np.insert(lat,0,-90)
   lat = np.append(lat,90)
   lon = np.arange(-182.5,179,5)
   m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
                    llcrnrlon=-182.5,\
                    urcrnrlon=177.5,\
                   resolution='c')

   m.drawcoastlines()
   m.drawmapboundary()
   parallels = np.arange(-90,91,30)
   meridians = np.arange(-180,151,30)

   plt.xticks(meridians)
   plt.yticks(parallels)

   m.drawparallels(parallels)
   m.drawmeridians(meridians)
   x, y = np.meshgrid(*m(lon, lat))

   # #Add the map
   poly = m.pcolor(lon, lat, data)


   plt.xlabel(X_axis_title, fontsize = X_axis_size)
   plt.ylabel(Y_axis_title, fontsize = Y_axis_size)
   # Add colourbar title
   cb = plt.colorbar(poly, shrink=0.7)#,#orientation = 'horizontal')
   tick_locator = ticker.MaxNLocator(nbins=colourbar_number_ticks)
   cb.locator = tick_locator
   cb.ax.tick_params(labelsize=colourbar_tick_size)
   cb.update_ticks()
   plt.text(191,93,colourbar_title,fontsize='25')

   # Add the title
   print species
   print units
   print start_time
   print end_time
   print Plot_title
   plt.title( Plot_title, fontsize='30' )
   fig.savefig( Output_Name, transparent=True )


   return ;

def get_species_data_from_bpch(wd,species,group,month, debug=True):
   print 'Extracting data from the bpch.'
   bpch_fname = wd + month + ".ctm.bpch"
#   print months
#   for month in months:
   bpch_data          = bpch(bpch_fname )
   if debug:
      print 'Data groups:'
      print bpch_data.groups
      print 'Group species:'
      print bpch_data.groups[group].variables
   species_data   = bpch_data.groups[group].variables[species]
   units          = bpch_data.groups[group].variables[species].units
   
   start_time     =  bpch_data.groups[group].variables['tau0']
   end_time       =  bpch_data.groups[group].variables['tau1']

   start_time, end_time = extract_month(start_time, end_time)


# #Turn species data from ppbv to moles

   #Convert from ppbv to species_moles
   air_mass    = bpch_data.groups['BXHGHT-$'].variables['AD'] 
   air_moles = (air_mass*1E3)# / ( 0.78*28.0 + 0.22*32.0 )
   species_moles   = air_moles * species_data


# Get tropopause information   
   Fraction_of_time_in_the_troposphere = bpch_data.groups["TIME-TPS"].variables['TIMETROP'] 
   if debug:
      print Fraction_of_time_in_the_troposphere
 
   
# Extract only moles in the troposphere
# by multipling the 4d species concentrations by the fraction of time they were in the troposphere ( 1 = aff trop, 0 = no trop, other = tropopause ).
   species_moles = np.multiply(species_moles[:,:38,:,:] , Fraction_of_time_in_the_troposphere)
   if debug:
      print 'species_moles shape = ' + str(species_moles.shape)

#  get the total column moles.
   total_column   =  species_moles[0,:,:,:].sum( axis=0 )     # total_column[t,lat,lon]
   if debug:
      print' total_column shape =  ' + str(total_column.shape)


# Get the surface area
   print 'Getting the surface area.'
   surface_area = bpch_data.groups['DXYP'].variables['AREA']
   if debug:
      print 'surface_area shape = ' + str(surface_area.shape)
#  surface_area[ lat, long ]


   #Convert from total mols to total Volume
   conversion_factor = 1E-7#1E-12 * 6.02e23 / 2.69e20
   column_volume = np.multiply( total_column, conversion_factor )  
   
   #Convert to Dobson units.
   dobson_data = np.divide( column_volume , surface_area )
   if debug:
      print 'dobson_data shape = ' + str(dobson_data.shape)

   
   return dobson_data, units, start_time, end_time;

def extract_month(start_time, end_time):
   # Turn time from hours from the equinox to YYYY-MM-DD
   epoch = datetime.datetime(1985,1,1)
   start_time     = epoch +  datetime.timedelta(hours=start_time[0])
   end_time       = epoch +  datetime.timedelta(hours=end_time[0])
   # Obtain only the date
   start_time  = start_time.date()
   end_time    = end_time.date()

   return start_time, end_time;
   


   
##lat = f.dimensions['lat']
#
##lat = f.variables['lat']
##lon = f.variables['lon']
#
#lat = np.arange(-88,90,4)
#lat = np.insert(lat,0,-90)
#lat = np.append(lat,90)
#
#lon = np.arange(-182.5,179,5)
#print lon
#tautime = f.variables['tau0']
#tautime_end = f.variables['tau1']
#
#print len(lat)
#print len(lon)
#
#group = f.groups['IJ-AVG-$']
#
#ozone = group.variables[species]
#units = ozone.units
#
#
##d = ozone.variables['tau0']
#print units
#print ozone.dimensions
#
#layer1 = ozone[:,0,:,:]
#layer1 = np.average(layer1,axis=0)	
#
#reference=datetime.datetime(1985, 1, 1)
#
#time =[]
#end_time=[]
#for t in tautime:
#	time.append(reference + datetime.timedelta(hours=t))
#
#for t in tautime_end:
#	end_time.append(reference + datetime.timedelta(hours=t))
#
#m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
#                    llcrnrlon=-182.5,\
#                    urcrnrlon=177.5,\
#                   resolution='c')
#
#m.drawcoastlines()
#m.drawmapboundary()
#parallels = np.arange(-90,91,15)
#meridians = np.arange(-180,151,30)
#
#
#plt.xticks(meridians)
#plt.yticks(parallels)
#
#m.drawparallels(parallels)
#m.drawmeridians(meridians)
#
#x, y = np.meshgrid(*m(lon, lat))
#
#print layer1.shape
#poly = m.pcolor(lon, lat, layer1)
#cb = plt.colorbar(poly, ax = m.ax,shrink=0.8)#,#orientation = 'horizontal')
##cb.set_label('%s (%s)'%(species,units))
#plt.xlabel('Longitude',fontsize = 20)
#plt.ylabel('Latitude',fontsize = 20)
#plt.text(191,93,'%s (%s)'%(species,units),fontsize=20)
#
#plt.title('%s at Surface, %s to %s'%(species,time[0],end_time[-1]),fontsize=20)
#
##plt.tight_layout()
#plt.savefig(Output_Name, transparent=True )
##plt.show()
#
## create 2D map(s) by averaging over a level interval
##for diag in diagnostics:
# #   temp_map2D.map_level_avg(diag, 0, 0)

main(species,group,debug)
