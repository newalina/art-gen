import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import pandas as pd

'''
pip install geopandas
pip install matplotlib
pip install folium
'''
def parse_shp(tracts_shapefile):

    print(tracts_shapefile.head())  

    csv_file_path = 'output_data.csv'
    # gdf['centroid'] = gdf.geometry.centroid
    tracts_shapefile.to_csv(csv_file_path, index=False)
    
    
    # tract_dict[''] = 
    # tracts['centroid'].plot(marker='o', color='red', markersize=5)
    # plt.show()  
    
def merge_file_on_tract(file_path, columns_to_drop=None):
    pm25_df = pd.read_csv(file_path)
    tract_df = pd.read_csv('output_data.csv').drop(columns_to_drop, axis = 1)
    tract_df = tract_df.rename(columns = {'GEOID': 'TRACT'})
    
    merged_df = pd.merge(pm25_df, tract_df, on='TRACT')
    merged_df.to_csv('merged_data.csv', index=False)
    
    
def draw_latitude_longitude(tracts_shapefile):

     #Project to a suitable CRS for the United States
    # EPSG:5070 - USA Contiguous Albers Equal Area Conic
    tracts_projected = tracts_shapefile.to_crs(epsg=5070)
    
    tracts_projected['centroid'] = tracts_projected.geometry.centroid
    tracts_projected['centroid'] = tracts_projected.centroid.to_crs(tracts_shapefile.crs)
    
    tracts_projected['latitude'] = tracts_projected.centroid.y
    tracts_projected['longitude'] = tracts_projected.centroid.x

    tracts_shapefile.centroid.plot(marker='o', color='red', markersize=5)
    plt.show()

    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

    for idx, row in tracts_shapefile.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['GEOID']).add_to(m)

    m
    
    
def main():
    shp_file_path = 'cb_2022_us_tract_500k/cb_2022_us_tract_500k.shp'
    tracts_shapefile = gpd.read_file('cb_2022_us_tract_500k/cb_2022_us_tract_500k.shp')
    pm25_file_path = '../parse_txt/pm2.5.csv'
    columns_to_drop = ['TRACTCE', 'AFFGEOID', 'NAMELSAD', 'STATE_NAME', 'ALAND', 'AWATER', 'LSAD']

    # draw_latitude_longitude(tracts_shapefile)
    merge_file_on_tract(pm25_file_path, columns_to_drop)
    
    
if __name__ == '__main__':
    main()