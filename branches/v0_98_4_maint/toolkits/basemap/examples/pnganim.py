# make a sequence of png files which may then be displayed
# as an animation using a tool like imagemagick animate, or
# converted to an animate gif (using imagemagick convert).

# reads data over http - needs an active internet connection.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy.ma as ma
import datetime, sys, time, subprocess
from mpl_toolkits.basemap import Basemap, shiftgrid, NetCDFFile, num2date

# times for March 1993 'storm of the century'
YYYYMMDDHH1 = '1993031000'
YYYYMMDDHH2 = '1993031700'

YYYY = YYYYMMDDHH1[0:4]
if YYYY != YYYYMMDDHH2[0:4]:
    raise ValueError,'dates must be in same year'

# set OpenDAP server URL.
URLbase="http://nomad3.ncep.noaa.gov:9090/dods/reanalyses/reanalysis-2/6hr/pgb/"
URL=URLbase+'pres'
URLu=URLbase+'wind'
URLv=URLbase+'wind'
print URL
print URLu
print URLv
try:
    data = NetCDFFile(URL)
    datau = NetCDFFile(URLu)
    datav = NetCDFFile(URLv)
except:
    raise IOError, 'opendap server not providing the requested data'

# read lats,lons,times.
print data.variables.keys()
print datau.variables.keys()
print datav.variables.keys()
latitudes = data.variables['lat'][:]
longitudes = data.variables['lon'][:].tolist()
times = data.variables['time']
# convert numeric time values to datetime objects.
fdates = num2date(times[:],units=times.units,calendar='standard')
# put times in YYYYMMDDHH format.
dates = [fdate.strftime('%Y%m%d%H') for fdate in fdates]
if YYYYMMDDHH1 not in dates or YYYYMMDDHH2 not in dates:
    raise ValueError, 'date1 or date2 not a valid date (must be in form YYYYMMDDHH, where HH is 00,06,12 or 18)'
# find indices bounding desired times.
ntime1 = dates.index(YYYYMMDDHH1)
ntime2 = dates.index(YYYYMMDDHH2)
print 'ntime1,ntime2:',ntime1,ntime2
if ntime1 >= ntime2:
    raise ValueError,'date2 must be greater than date1'
# get sea level pressure and 10-m wind data.
slpdata = data.variables['presmsl']
udata = datau.variables['ugrdprs']
vdata = datau.variables['vgrdprs']
# mult slp by 0.01 to put in units of millibars.
slpin = 0.01*slpdata[ntime1:ntime2+1,:,:]
uin = udata[ntime1:ntime2+1,0,:,:] 
vin = vdata[ntime1:ntime2+1,0,:,:] 
datelabels = dates[ntime1:ntime2+1]
# add cyclic points
slp = np.zeros((slpin.shape[0],slpin.shape[1],slpin.shape[2]+1),np.float64)
slp[:,:,0:-1] = slpin; slp[:,:,-1] = slpin[:,:,0]
u = np.zeros((uin.shape[0],uin.shape[1],uin.shape[2]+1),np.float64)
u[:,:,0:-1] = uin; u[:,:,-1] = uin[:,:,0]
v = np.zeros((vin.shape[0],vin.shape[1],vin.shape[2]+1),np.float64)
v[:,:,0:-1] = vin; v[:,:,-1] = vin[:,:,0]
longitudes.append(360.); longitudes = np.array(longitudes)
# make 2-d grid of lons, lats
lons, lats = np.meshgrid(longitudes,latitudes)
print 'min/max slp,u,v'
print slp.min(), slp.max()
print uin.min(), uin.max()
print vin.min(), vin.max()
print 'dates'
print datelabels
# make orthographic basemaplt.
m = Basemap(resolution='c',projection='ortho',lat_0=60.,lon_0=-60.)
plt.ion() # interactive mode on.
uin = udata[ntime1:ntime2+1,0,:,:] 
vin = vdata[ntime1:ntime2+1,0,:,:] 
datelabels = dates[ntime1:ntime2+1]
# make orthographic basemaplt.
m = Basemap(resolution='c',projection='ortho',lat_0=60.,lon_0=-60.)
plt.ion() # interactive mode on.
# create figure, add axes (leaving room for colorbar on right)
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# set desired contour levels.
clevs = np.arange(960,1061,5)
# compute native x,y coordinates of grid.
x, y = m(lons, lats)
# define parallels and meridians to draw.
parallels = np.arange(-80.,90,20.)
meridians = np.arange(0.,360.,20.)
# number of repeated frames at beginning and end is n1.
nframe = 0; n1 = 10
pos = ax.get_position()
l, b, w, h = pos.bounds
# loop over times, make contour plots, draw coastlines, 
# parallels, meridians and title.
for nt,date in enumerate(datelabels[1:]):
    CS = m.contour(x,y,slp[nt,:,:],clevs,linewidths=0.5,colors='k',animated=True)
    CS = m.contourf(x,y,slp[nt,:,:],clevs,cmap=plt.cm.RdBu_r,animated=True)
    # plot wind vectors on lat/lon grid.
    # rotate wind vectors to map projection coordinates.
    #urot,vrot = m.rotate_vector(u[nt,:,:],v[nt,:,:],lons,lats)
    # plot wind vectors over maplt.
    #Q = m.quiver(x,y,urot,vrot,scale=500) 
    # plot wind vectors on projection grid (looks better).
    # first, shift grid so it goes from -180 to 180 (instead of 0 to 360
    # in longitude).  Otherwise, interpolation is messed uplt.
    ugrid,newlons = shiftgrid(180.,u[nt,:,:],longitudes,start=False)
    vgrid,newlons = shiftgrid(180.,v[nt,:,:],longitudes,start=False)
    # transform vectors to projection grid.
    urot,vrot,xx,yy = m.transform_vector(ugrid,vgrid,newlons,latitudes,51,51,returnxy=True,masked=True)
    # plot wind vectors over maplt.
    Q = m.quiver(xx,yy,urot,vrot,scale=500)
    # make quiver key.
    qk = plt.quiverkey(Q, 0.1, 0.1, 20, '20 m/s', labelpos='W')
    # draw coastlines, parallels, meridians, title.
    m.drawcoastlines(linewidth=1.5)
    m.drawparallels(parallels)
    m.drawmeridians(meridians)
    plt.title('SLP and Wind Vectors '+date)
    if nt == 0: # plot colorbar on a separate axes (only for first frame)
        cax = plt.axes([l+w-0.05, b, 0.03, h]) # setup colorbar axes
        fig.colorbar(CS,drawedges=True, cax=cax) # draw colorbar
        cax.text(0.0,-0.05,'mb')
        plt.axes(ax) # reset current axes
    plt.draw() # draw the plot
    # save first and last frame n1 times 
    # (so gif animation pauses at beginning and end)
    if nframe == 0 or nt == slp.shape[0]-1:
       for n in range(n1):
           plt.savefig('anim%03i'%nframe+'.png')
           nframe = nframe + 1
    else:
       plt.savefig('anim%03i'%nframe+'.png')
       nframe = nframe + 1
    ax.clear() # clear the axes for the next plot.

print """
Now display animation using imagemagick 'animate -delay 10 anim*png'
or, create an animated gif using 'convert -delay 10 anim*png anim.gif'
and display in a web browser (or Powerpoint).

Will try to run imagemagick animate in 5 seconds ..."""
time.sleep(5)
subprocess.call('animate -delay 10 anim*png',shell=True)