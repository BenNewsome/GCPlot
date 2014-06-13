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

species = 'O3'

#set up plot
fig=plt.figure(figsize=(20,12))
ax = fig.add_axes([.05, .1, .9, .8])
fig.patch.set_facecolor('white')

#bpch_fname = "bpch_files/4x5_GEOS5/ctm.bpch_4x5_GEOS5_2006-2012"
bpch_fname = "/work/home/bn506/Rate_Sensetivity/Batch_runs/HO2_NO_p0/ctm.bpch"

get_times = [1]

f = bpch(bpch_fname)#,timeslice = get_times)

#lat = f.dimensions['lat']

#lat = f.variables['lat']
#lon = f.variables['lon']

lat = np.arange(-88,90,4)
lat = np.insert(lat,0,-90)
lat = np.append(lat,90)

lon = np.arange(-182.5,179,5)
print lon
tautime = f.variables['tau0']
tautime_end = f.variables['tau1']

print len(lat)
print len(lon)

group = f.groups['IJ-AVG-$']

ozone = group.variables[species]
units = ozone.units


d = ozone.variables['tau0']
print units
print ozone.dimensions

layer1 = ozone[:,0,:,:]
layer1 = np.average(layer1,axis=0)	

reference=datetime.datetime(1985, 1, 1)

time =[]
end_time=[]
for t in tautime:
	time.append(reference + datetime.timedelta(hours=t))

for t in tautime_end:
	end_time.append(reference + datetime.timedelta(hours=t))

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

print layer1.shape
poly = m.pcolor(lon, lat, layer1)
cb = plt.colorbar(poly, ax = m.ax,shrink=0.8)#,#orientation = 'horizontal')
#cb.set_label('%s (%s)'%(species,units))
plt.xlabel('Longitude',fontsize = 20)
plt.ylabel('Latitude',fontsize = 20)
plt.text(191,93,'%s (%s)'%(species,units),fontsize=20)

plt.title('%s at Surface, %s to %s'%(species,time[0],end_time[-1]),fontsize=20)

plt.show()

# create 2D map(s) by averaging over a level interval
#for diag in diagnostics:
 #   temp_map2D.map_level_avg(diag, 0, 0)
