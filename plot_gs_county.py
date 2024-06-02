from urllib.request import urlopen
import pandas as pd
import plotly.express as px
import json

df = pd.read_excel('fbc_data_2024_update2.xlsx', dtype={'county_fips': str, 'Min Grade': int},)
df2 = df.loc[df['Family'] == '1p0c']
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig = px.choropleth(df2, geojson=counties, locations='county_fips', color='Min Grade',
                    color_continuous_scale="Rainbow",
                    range_color=(2, 8),
                    hover_data=['County', 'Min Grade', 'Highest Step'],
                    scope="usa",
                    title='Minimum GS Grade Needed for COL'
                    )
fig.update_traces(marker_line_width=0, marker_opacity=0.8)
fig.update_layout(title_text='Minimum GS Grade Needed for Single Person COL')
fig.update_geos(
showsubunits=True, subunitcolor="black"
)
fig.show()
fig.write_html('single_COL_GS_map.html')

df2 = df.loc[df['Family'] == '2p2c']
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig = px.choropleth(df2, geojson=counties, locations='county_fips', color='Min Grade',
                    color_continuous_scale="Rainbow",
                    range_color=(9, 15),
                    hover_data=['County', 'Min Grade', 'Highest Step'],
                    scope="usa",
                    title='Minimum GS Grade Needed for COL'
                    )
fig.update_traces(marker_line_width=0, marker_opacity=0.8)
fig.update_layout(title_text='Minimum GS Grade Needed for Family of 4 COL')
fig.update_geos(
showsubunits=True, subunitcolor="black"
)
fig.show()
fig.write_html('familyOf4_COL_GS_map.html')