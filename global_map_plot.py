from bpch import bpch
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
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

def main(species,group,debug):
   wd, Output_Name = get_arguments()


   raw_data=get_species_data_from_bpch(wd,species,group)
   print 'raw data dimenstion = ' + str(raw_data.dimensions)

   relevant_data = strip_relevant_data(raw_data,debug)
   print 'relevand data dimensions = ' + str(relevant_data.dimensions   )

   plot_the_data(relevant_data, wd, Output_Name, debug)
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


def plot_the_data(data, wd, Output_Name, debug):
   print 'Plotting the data.'
   #set up plot
#   print data
#   print data.dimensions
   
   fig=plt.figure(figsize=(20,12))
   ax = fig.add_axes([.05, .1, .9, .8])
   fig.patch.set_facecolor('white')
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
   parallels = np.arange(-90,91,15)
   meridians = np.arange(-180,151,30)

   plt.xticks(meridians)
   plt.yticks(parallels)

   m.drawparallels(parallels)
   m.drawmeridians(meridians)
   x, y = np.meshgrid(*m(lon, lat))
   poly = m.pcolor(lon, lat, data)

   cb = plt.colorbar(poly, ax = m.ax,shrink=0.8)#,#orientation = 'horizontal')
   plt.xlabel('Longitude',fontsize = 20)
   plt.ylabel('Latitude',fontsize = 20)
   #plt.text(191,93,'%s (%s)'%(species,units),fontsize=20)

   #plt.title('%s at Surface, %s to %s'%(species,time[0],end_time[-1]),fontsize=20)
   fig.savefig( Output_Name, transparent=True )


   return ;

def get_species_data_from_bpch(wd,species,group, debug=True):
   print 'Extracting data from the bpch.'
   bpch_fname = wd+"ctm.bpch"
#   print months
#   for month in months:
   slice = [2]
   tmp_data          = bpch(bpch_fname,timeslice = [slice] )
   if debug:
      print 'Data groups:'
      print tmp_data.groups
   tmp_data_group    = tmp_data.groups[group]
   if debug:
      print 'Group species:'
      print tmp_data_group.variables
   tmp_data_species  = tmp_data_group.variables[species]
   tmp_data_units    = tmp_data_species.units
   
      

   print tmp_data_species.shape
   data=tmp_data_species
#   print range(6)[timeslice]
   # combine list into single array
   debug =  True
   if debug:
      print 'data length = '  + str(data.dimensions)
#      print data
      print 'data units = '   + tmp_data_units
#   print data

   return data;
   
def strip_relevant_data(data,debug):
   print 'Extracting the surface data.'
   # get surface data
   print ' relevant input data = ' + str(data.dimensions)
   surface_data   =  data[:,0,:,:]
   print 'Surface data dimenstions = ' + str(surface_data.dimensions)
   # Average over year
   surface_data_average =  surface_data[:,:,:].sum( axis=0 )
   print 'Surface data average = ' + str(len(surface_data_average))
   return surface_data_average;

   
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
