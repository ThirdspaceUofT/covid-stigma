import pandas as pd
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
import mapclassify as mc
import os
import plotly.express as px
import csv 

def draw_per_day(date):
    if os.path.exists(date + '.csv') is False:
        return
    print(date)
    df = pd.read_csv(date + '.csv', header=None, names=['id', 'longitude', 'latitude', 'location', 'created_at', 'lang'])
    print(date, df.shape)
    # assign count value
    mydict = dict(df.location.value_counts())

    df['notnan'] = df['location'].notna()
    df['count'] = df.apply(lambda x: mydict[x.location] if x.notnan else 1, axis=1)
    df.drop_duplicates(subset ='location', 
                     keep = 'first', inplace = True) 
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

    scheme = mc.Quantiles(df['count'], k=5)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    ax = gplt.polyplot(
        world, 
        edgecolor='white', 
        facecolor='lightgray',
    )
    gplt.pointplot(
        gdf, ax=ax, hue='count', cmap='Reds', 
        scale='count', scheme=scheme, 
        legend=True, legend_var='hue'
    )
    ax.set_title('Discussion on Twitter, ' + date, fontsize=10)
    plt.savefig(date + '.png', dpi=1000)
    #plt.show()
    
    
def draw_month(month):
    to_full_month = {
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 
        'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July'
    }
    frames = []
    for i in range(1, 32):
        day_str = str(i)
        if i < 10:
            day_str = '0' + str(i)
        if os.path.exists(month + ' ' + day_str + '.csv'):
            df1 = pd.read_csv(month + ' ' + day_str + '.csv', header=None, names=['id', 'longitude', 'latitude', 'location', 'created_at', 'lang'])
            frames.append(df1)
    df = pd.concat(frames)
    print(df.shape)
    mydict = dict(df.location.value_counts())
    df['notnan'] = df['location'].notna()
    df['count'] = df.apply(lambda x: mydict[x.location] if x.notnan else 1, axis=1)
    df.drop_duplicates(subset ='location', 
                     keep = 'first', inplace = True) 
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

    scheme = mc.Quantiles(df['count'], k=5)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    ax = gplt.polyplot(
        world, 
        edgecolor='white', 
        facecolor='lightgray',
    )
    gplt.pointplot(
        gdf, ax=ax, hue='count', cmap='Reds', 
        scale='count', scheme=scheme, 
        legend=True, legend_var='hue'
    )
    ax.set_title('Discussion on Twitter, ' + to_full_month[month], fontsize=10)
    plt.savefig(month + '.png', dpi=1000)


def draw_month_timeline(month):
    to_full_month = {
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 
        'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July'
    }
    frames = []
    for i in range(1, 32):
        day_str = str(i)
        if i < 10:
            day_str = '0' + str(i)
        if os.path.exists(month + ' ' + day_str + '.csv'):
            df1 = pd.read_csv(month + ' ' + day_str + '.csv', header=None, names=['id', 'longitude', 'latitude', 'location', 'created_at', 'lang'])
            frames.append(df1)
    df = pd.concat(frames)
    print(df.shape)
    mydict = dict(df.location.value_counts())
    df['notnan'] = df['location'].notna()
    df['count'] = df.apply(lambda x: mydict[x.location] if x.notnan else 1, axis=1)
    

    df.drop_duplicates(subset ='location', 
                     keep = 'first', inplace = True) 

    df['date'] = df.apply(lambda x: str(x.created_at)[4:10], axis=1)
    fig = px.scatter_geo(df, lat='latitude', lon='longitude',
                     hover_name='location',
                     projection='natural earth',
                     animation_frame='date',
                     hover_data=['date', 'count', 'lang', 'longitude', 'latitude'],
                     color='count',
                     )
    fig.update_layout(
        title = 'Discussion on Twitter, ' + to_full_month[month]
    )

    fig.write_html(month + '.html')
    
def get_country(x):
    location = str(x['location'])
    tokens = location.split(', ')
    return tokens[-1]
    
def get_country_count(month):
    to_full_month = {
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 
        'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July'
    }
    frames = []
    for i in range(1, 32):
        day_str = str(i)
        if i < 10:
            day_str = '0' + str(i)
        if os.path.exists(month + ' ' + day_str + '.csv'):
            df1 = pd.read_csv(month + ' ' + day_str + '.csv', header=None, names=['id', 'longitude', 'latitude', 'location', 'created_at', 'lang'])
            frames.append(df1)
    df = pd.concat(frames)
    
    df['count'] = df.apply(lambda x: get_country(x), axis=1)
    result = dict(df['count'].value_counts())
    
    output = open('count_by_country_jan.csv', 'a', newline='')
    writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    print(to_full_month[month])
    writer.writerow(['country/region', 'count'])
    output.flush()
    for key in sorted(result.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([key[0], key[1]])
        output.flush()
    
    output.close()
    
def main1(month):
    for i in range(1, 32):
        day_str = str(i)
        if i < 10:
            day_str = '0' + str(i)
        draw_per_day(month + ' ' + day_str)
    draw_month(month)
  
if __name__ == '__main__':
    #main1('Jan')
    # main1('Feb')
    #draw_month_timeline('Jan')
    # draw_month_timeline('Feb')
    get_country_count('Jan')