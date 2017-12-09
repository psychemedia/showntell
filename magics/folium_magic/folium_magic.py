from argparse import ArgumentParser
import shlex
from csv import reader
import os.path
from IPython.core.magic import (
    magics_class, line_magic, line_cell_magic, Magics)
from IPython.core.display import Image, HTML


import folium
        
@magics_class
class FoliumMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(FoliumMagic, self).__init__(shell)
        self.cache_display_data = cache_display_data

    @line_magic
    def folium_map(self,line, cell=''):
        ''' Map arguments '''
        parser = ArgumentParser()
        parser.add_argument('-l', '--latlong', default='52.0250,-0.7084')
        parser.add_argument('-m', '--marker', default=None)
        parser.add_argument('-j', '--geojson', default=None)
        #For markers, pass in a list of dicts: [{'lat':x,'lng':y,'latlng''x,y',popup:'txt'}]
        #or a list of lists [ [lat, lng,'popup txt']
        parser.add_argument('-M','--markers',default=None)
        parser.add_argument('-z', '--zoom', default=10 )
        args = parser.parse_args(shlex.split(line))

        latlong = [float(x) for x in args.latlong.split(',')]
        m=folium.Map(location=latlong, zoom_start=args.zoom)
        
        if args.marker is not None:
            #'52.0250,-0.7084,"sds sdsd"'
            marker = [i for i in reader([args.marker])][0]
            if len(marker)==3:
                latlong = [float(x) for x in marker[:2]]
                folium.Marker(latlong,popup=str(marker[2])).add_to(m)
        
        if args.markers is not None:
            markers = self.shell.user_ns[args.markers]
            if isinstance(markers,dict):
                markers = [markers]
            elif isinstance(markers,list):
                if isinstance(markers[0],list) or isinstance(markers[0],dict):
                    pass
                else:
                    markers = [markers]
            else: markers = []
                
            for marker in markers:
                popup = None
                if isinstance(marker,dict):
                    if 'latlng' in marker:
                        latlong = [float(x) for x in marker[latlng].split(',')]
                    elif 'lat' in marker and 'lng' in marker:
                        latlong = [marker['lat'], marker['lng']]
                    else: continue
                    if 'popup' in marker:
                        popup = marker['popup']
                elif isinstance(marker,list) and len(marker)>2:
                    latlong = [float(x) for x in  marker[:2]]
                    if len(marker)>2:
                        popup=str(marker[2])
                else: continue

                folium.Marker(latlong,popup=popup).add_to(m)
                
        if args.geojson is not None:
            if os.path.isfile(args.geojson):
                folium.GeoJson( args.geojson, name='geojson' ).add_to(m)
            
        return m
        
def load_ipython_extension(ipython):
    ipython.register_magics(FoliumMagic)
    
ip = get_ipython()
ip.register_magics(FoliumMagic)