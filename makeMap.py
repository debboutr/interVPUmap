# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 08:21:29 2017

@author: Rdebbout
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:05:48 2016

This is a script to walk through json file creation for foium map

@author: Rdebbout
"""

import folium
import geopandas as gpd
from shapely.geometry import LineString
from shapely.geometry import Polygon, MultiPolygon

NHD_dir = r'D:/NHDPlusV21'
bounds = gpd.GeoDataFrame.from_file('%s/NHDPlusGlobalData/BoundaryUnit.shp' % (NHD_dir))


out = r'D:\Projects\interVPUmap'
VPUs = bounds.ix[bounds.UnitType == 'VPU']  # Select out only VPU boundaries
VPUs = VPUs.drop([88,89],axis=0)
VPUs.geometry

keep = gpd.GeoDataFrame()
for idx, row in VPUs.iterrows():
    print idx
    if type(row.geometry) == type(Polygon()):
        g = gpd.GeoSeries(LineString(list(row.geometry.exterior.coords)))
        gdf = gpd.GeoDataFrame({'VPU':[row.UnitID]},geometry=g)
        keep = keep.append(gdf, ignore_index=True)        
    if type(row.geometry) == type(MultiPolygon()):
        polys = [p for p in row.geometry]        
        big = sorted([ps for ps in enumerate(polys)],key=lambda x: len(x[1].exterior.coords), reverse=True)[0][1]
        g = gpd.GeoSeries(LineString(list(big.exterior.coords)))
        gdf = gpd.GeoDataFrame({'VPU':[row.UnitID]},geometry=g)
        keep = keep.append(gdf, ignore_index=True)
keep.crs = VPUs.crs        
keep.to_crs({'init' :'epsg:4326'}).to_file(r"%s\vpu_lines.json" % out, driver="GeoJSON")

needed = ['14','15','06','05','08','10U','10L','07','11']
trim = keep.ix[keep.VPU.isin(needed)]
trim.to_crs({'init' :'epsg:4326'}).to_file(r"%s\vpu_lines_needed.json" % out, driver="GeoJSON")



arr = np.empty([0,2])
for bnds in range(len(poly)):
    arr = np.concatenate([arr,np.array(poly[bnds].exterior.coords)[:,:2]])
    if len(poly[bnds].interiors) > 0:
        arr = np.concatenate([arr,addInteriors(poly[bnds].interiors,arr)])
                
                
VPUs.to_crs({'init' :'epsg:4326'}).to_file(r"%s\boundary.json" % out, driver="GeoJSON")

t = VPUs.centroid
type(t)
t = VPUs.bounds
lat_Center = (t.miny.min() + t.maxy.max())/2
lon_Center = (t.maxx.max() + t.minx.min())/2



f_map=folium.Map(location=[lat_Center , lon_Center],zoom_start=6,tiles="Stamen Terrain")

f_map.add_child(folium.GeoJson(data=open(r"%s\vpu_lines_needed.json" % out),
                name='VPU Boundaries'))

f_map.save(outfile=r'%s\interVPU.html' % out)

## code to get problem sites out of NRSA1314
keep = ['FLS9-0919','FLS9-0921','IAR9-0914','MNSS-1172','OKRF-0005','OKRF-0101','ORRF-0107','PASS-1166','TXRF-0002','WARF-0110']
sites = gpd.read_file(r'L:\Priv\CORFiles\Geospatial_Library\Data\Project\StreamCat\NRSA13_14_SiteData.shp')
sites.columns.tolist()
new = sites.ix[sites.SITE_.isin(keep)]
new.crs
new.to_file(r'D:\Projects\temp\NRSA1314_probsites\sites_10.shp')