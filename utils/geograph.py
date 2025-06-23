import geopandas as gpd
import folium
from shapely.geometry import Point

def load_region_geojson(filepath):
    return gpd.read_file(filepath)

def prepare_disaster_geodf(df, lon_col='Longitude', lat_col='Latitude', crs="EPSG:4326"):
    df = df.dropna(subset=[lon_col, lat_col])
    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    return gpd.GeoDataFrame(df, geometry=geometry, crs=crs)

def plot_disasters_on_map(disaster_gdf, region_gdf=None, zoom_start=4):
    center = disaster_gdf.geometry.unary_union.centroid.coords[0][::-1]
    fmap = folium.Map(location=center, zoom_start=zoom_start)
    if region_gdf is not None:
        folium.GeoJson(region_gdf).add_to(fmap)
    for _, row in disaster_gdf.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=4,
            popup=f"{row.get('Disaster Type', 'Unknown')}, {row.get('Year', '')}",
            color='red',
            fill=True
        ).add_to(fmap)
    return fmap

def count_disasters_by_region(disaster_gdf, region_gdf, region_key='NAME'):
    disaster_proj = disaster_gdf.to_crs(region_gdf.crs)
    joined = gpd.sjoin(disaster_proj, region_gdf, how='inner', predicate='intersects')
    return joined.groupby(region_key).size().reset_index(name='disaster_count')
