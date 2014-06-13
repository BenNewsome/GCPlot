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
   wd, Output_Name = get_arguments()


   species_data, units, start_time, end_time = get_species_data_from_bpch(wd,species,group, month)
   print 'Species data dimenstion = ' + str(species_data.dimensions)

   relevant_data = strip_relevant_data(species_data,debug)
   print 'relevant data dimensions = ' + str(species_data.dimensions   )

   plot_the_data(relevant_data, units, start_time, end_time, wd, Output_Name, debug)
   return;


# Ask for arguments
def get_arguments():
   print 'Getting the arguments.'
   try:
      wd =  sys.argv[1]
      Output_Name=   sys.argv[2]+'.png'
   except:
      sys.exit('Please input arguments of working dir and output png')
   return wd, Output_Name;


def plot_the_data(data, units, start_time, end_time, wd, Output_Name, debug):
   print 'Plotting the data.'
   #set up plot
#   print data
#   print data.dimensions
   colourbar_tick_size     = 20
   colourbar_title         = species + units
   colourbar_title_size    = 25
   colourbar_number_ticks  = 5
   X_axis_title            = 'Longitude'
   X_axis_size             = 25
   Y_axis_title            = 'Latitude'
   Y_axis_size             = 25
   Plot_title              =  "Surface " + species + ' average between '+ str(start_time) + ' and ' + str(end_time)
   

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
   Colourbar_title = species +' ' +  units
   plt.text(191,93,Colourbar_title,fontsize='25')

   # Add the title
   print species
   print units
   print start_time
   print end_time
   print Plot_title
   plt.title( Plot_title, fontsize='30' )
   fig.savefig( Output_Name, transparent=True )


   return ;

def get_species_data_from_bpch(wd,species,group, debug=True):
   print 'Extracting data from the bpch.'
   bpch_fname = wd + month + ".ctm.bpch"
#   bpch_fname = wd + "ctm.bpch"
   bpch_data          = bpch(bpch_fname)
   if debug:
      print 'Data groups:'
      print bpch_data.groups
      print 'Group species:'
      print bpch_data.groups[group].variables

   species_data   =   bpch_data.groups[group].variables[species]
   units          =   bpch_data.groups[group].variables[species].units
   start_time     =   bpch_data.groups[group].variables['tau0']
   end_time       =   bpch_data.groups[group].variables['tau1']
   
   # Turn time from hours from the equinox to YYYY-MM-DD
   epoch = datetime.datetime(1985,1,1)
   start_time     = epoch +  datetime.timedelta(hours=start_time[0])
   end_time       = epoch +  datetime.timedelta(hours=end_time[0])
   # Obtain only the date
   start_time  = start_time.date()
   end_time    = end_time.date()

   return species_data, units, start_time, end_time;
   
def strip_relevant_data(species_data,debug):
   print 'Extracting the mean surface data.'
   relevant_data   =  species_data[:,0,:,:].mean( axis=0 )
   print 'relevent_data dimenstions = ' + str(relevant_data.dimensions)
   return relevant_data;

   
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
