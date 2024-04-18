import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import os.path
from matplotlib.colors import ListedColormap
import os, glob, sys
import datetime as dt
from datetime import *
from netCDF4 import Dataset
import matplotlib.cm as mpl_cm
import matplotlib.colors as mpl_col
import cartopy.feature as cfeature
import cartopy

# Read file
DATEIN = str(sys.argv[1])
DATESTART = str(sys.argv[2])
DATEFCST = str(sys.argv[3])
EXP = str(sys.argv[4])
datest = datetime.strptime(DATESTART+'00','%Y%m%d%H%M%S')
datest_file = datest.strftime('%Y-%m-%d_%H.%M.%S')
datefc = datetime.strptime(DATEFCST+'00','%Y%m%d%H%M%S')
print('datefcst=',datefc)
datefc_file = datefc.strftime('%Y-%m-%d_%H.%M.%S')
start_file = '/glade/derecho/scratch/nghido/sio-cw3e_cheyenne/'+EXP+'/ExtendedFC/'+DATEIN+'/mean_convert_0.04d_WestUS/diag.'+datest_file+'.nc'
fcst_file = '/glade/derecho/scratch/nghido/sio-cw3e_cheyenne/'+EXP+'/ExtendedFC/'+DATEIN+'/mean_convert_0.04d_WestUS/diag.'+datefc_file+'.nc'
startnc = Dataset(start_file, "r")
fcstnc = Dataset(fcst_file, "r")
lats = np.array(startnc.variables['latitude'][:])
lons = np.array(startnc.variables['longitude'][:])
preci = np.array( startnc.variables['rainc'][0,:,:] )+np.array( startnc.variables['rainnc'][0,:,:] )
preci = (np.array( fcstnc.variables['rainc'][0,:,:] )+np.array( fcstnc.variables['rainnc'][0,:,:] ))-preci
#z = np.array( startnc.variables['height_925hPa'][0,:,:] ) 
#preci  = np.where(z>0, preci, np.nan)
#Plot
x, y = np.float32(np.meshgrid(lons, lats))
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_xlim([-125, -110])
ax.set_ylim([30, 50])
#gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5, color='black', alpha=0.5, linestyle='dotted')
gl = ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True, ylocs=np.arange(30, 50,4), xlocs=np.arange(-125, -110,4), linestyle='--')
gl.right_labels = False
gl.top_labels = False
gl.xlabel_style = {'size': 19}
gl.ylabel_style = {'size': 19}
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
levels = np.arange(2,50,1)
cpal = 'rainbow'
cmap_cont = mpl_cm.get_cmap(cpal)
cmap_disc = mpl_cm.get_cmap(cpal, len(levels)-1)
badcol   = 'grey'
overcol  = 'magenta'
undercol = 'white'
for cmap in [cmap_cont, cmap_disc]:
      if badcol:   cmap.set_bad(  color=badcol,   alpha=0.5 )
      if overcol:  cmap.set_over( color=overcol,  alpha=0.5 )
      if undercol: cmap.set_under(color=undercol, alpha=0.5 )

cf = ax.contourf(lons, lats, preci,
              cmap=cmap_disc,
              levels=levels,
              extend='both')
colorbar= plt.colorbar(cf, ax=ax, orientation='vertical',pad=0.03, shrink=0.95,label='mm',format='%i')
colorbar.set_label('mm', size=19)
colorbar.ax.tick_params(labelsize=19)
ax.coastlines(resolution='10m', color='black', linestyle='-', alpha=1)
provinces_50m = cfeature.NaturalEarthFeature('cultural',
                                             'admin_1_states_provinces_lines',
                                             '50m',
                                             facecolor='none')
ax.add_feature(provinces_50m)
ax.add_feature(cfeature.BORDERS)
#ax.add_feature(cfeature.OCEAN, facecolor='white', edgecolor='black')
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='black', facecolor='white'))
plt.title('24h accumulated precipitation '+DATEFCST+ ' initiated from '+DATEIN, size=10)
fig.savefig('24h_accumulated_precipitation_'+DATEFCST+'_initiated_from_'+DATEIN+'.png', dpi=300, bbox_inches='tight')
