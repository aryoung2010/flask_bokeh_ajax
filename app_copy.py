from flask import Flask, render_template, jsonify, request, url_for
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, AjaxDataSource
from bokeh.models import CustomJS, Slider, Select
from bokeh.layouts import widgetbox, column
import json
import math


# Some parts of the code was addopted from https://stackoverflow.com/questions/37083998/flask-bokeh-ajaxdatasource

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

#!/usr/bin/env python
# coding: utf-8

# ## Impact of Chronic Financial Stress on Diabetes
# based on post by Michael Harmon: http://michael-harmon.com/blog/IntroToBokeh.html


## Currently the code is running in python, but unsure about the web part showing up.
## The text shows up in the preview window, but not the images.
## some of the packages listed are residual from previous work(and thus unnecessary), 
## but the "unused package" notification feature is also highlighting packages i 
## definitely used, so I did not delete any. 

# TODO: List of items
# -fix the bug that is only showing text
# -add missing blockgroups with a value of NA 
# -link slider bars to model text


# ### Import Packages


import pandas as pd
import numpy as np
import matplotlib 
matplotlib.use('agg') 
import matplotlib.pyplot as plt

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)


# ### Load Data

models= pd.read_csv('Data_In/BG_17_Model_Data.csv')
models["GEOID"] = models["merge"].astype(str)
len(models) #138

models.columns



models= models[["GEOID","Short_Name",'Evictions','Uninsured_Adult19_64','total__diabetic__rate','actual_diabetic__poor_control_rate']]
models.head()


# ### Importing Shapefiles

# Save the shapefile you are interested on your computer in a place you can access from where you are storing your Jupyter notebook. For instance, I saved mine in the same folder as my code in a subfolder called "Datasets". Then you can access the shapefile using the code below.
# 
# My shapefile is of blockgroups in North Carolina.


import geopandas as gpd
shape=gpd.read_file('Shapefiles/tl_2018_37_bg.shp')
#shape.plot()


# Below is the code that filters the data to just Durham County, which is where the 'COUNTYFP' variable is equal to '063'.


durham = shape[shape['COUNTYFP']=='063']
durham.plot()


# Preview the data to be sure your GEOID variable matches the one you made earlier.


durham["GEOID2"]= durham["GEOID"].astype(str)
durham["GEOID2"]= durham["GEOID"]+".0"
durham.head()
len(durham) #153


# Next, you can merge the data and create a new file that has both the spatial data and ACS data table you pulled down. You merge with the spatial dataset as the first dataset listed, and the datatable within the merge parenthases. Check the data to be sure the merge occured correctly.


durham_models = durham.merge(models, on='GEOID')
durham_models.head()
len(durham_models) #149




durham_models["per_diab"]= durham_models["total__diabetic__rate"]*100
durham_models["per_unin"]= durham_models["Uninsured_Adult19_64"]*100
durham_models.columns


# Now you can see your data! Notice, because we subset the data, it will only show the data we cut the file to (quartiles 4 and 5).



f, ax = plt.subplots(1)
TotalDiabPlot = durham_models.plot('total__diabetic__rate', legend=True,ax=ax, linewidth=0.5)
ax.set_axis_off()
plt.axis('equal')
plt.title("Percent Diabetic")



durham_models.head()



import json
import bokeh
#Read data to json.

#gdf_nc83 = durham_models.to_crs({'init': 'epsg:2264'}\

gdf_nc83 = durham_models
merged_json = json.loads(gdf_nc83.to_json()) #geodata
#Convert to String like object.
json_data = json.dumps(merged_json)



gdf_nc83.crs
#print(durham_models['per_diab'].mean())


from bokeh.palettes import brewer
from bokeh.io import curdoc, output_notebook, output_file
from bokeh.models import Slider, HoverTool, TapTool
from bokeh.layouts import widgetbox, row, column
from bokeh.events import ButtonClick
from bokeh.models.annotations import ColorBar
from bokeh.models.widgets import RadioButtonGroup
from bokeh.models.widgets import Div
from bokeh.models.mappers import LinearColorMapper
from bokeh.layouts import row, column, gridplot
import pandas as pd
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.models import Button, GeoJSONDataSource
### Source Data


from bokeh.palettes import brewer
from bokeh.io import curdoc, output_notebook, output_file
from bokeh.models import Slider, HoverTool, TapTool
from bokeh.layouts import widgetbox, row, column
from bokeh.events import ButtonClick
from bokeh.models.annotations import ColorBar
from bokeh.models.widgets import RadioButtonGroup
from bokeh.models.mappers import LinearColorMapper
from bokeh.layouts import row, column, gridplot
import pandas as pd
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.models import Button, GeoJSONDataSource
### Source Data

geosource = GeoJSONDataSource(geojson = json.dumps(merged_json))


# map data
# figure of map with choropleth

# data for histogram (default)
# figure of histogram with distribution of diabetes (default)
# (data for text default)

#data for line on graph representing location of selection on histogram (yl)


# where map selected, when a change happens, perform this action
# three arguments- s1, s3
## indicies (constant) are the indicies of the selected elements, called inds
## d holds the data for those indicies
## y defaults to 0

# if no selection, end action (default text values)

# for selected index




#####################################################################
### Colors

#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]
#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40, nan_color = '#d9d9d9')
#Define custom tick labels for color bar.
tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}
#Add hover tool
hover = HoverTool(tooltips = [ ('Blockgroup/Neighborhoods','@Short_Name'),('% Diabetic', '@total__diabetic__rate'), ('Eviction Rate', '@Evictions'), ('Uninsured Rate', "@per_unin")])
#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20, border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

######################################################################
### Figure Plotting

### Map ####

# Specify the selection tools to be made available
all_tools = ['reset', hover]

#Create figure object.
p = figure(title = 'Percent of adults who are diabetic, by block group, 2017', plot_height = 550 , plot_width = 400, tools = all_tools)
s3 = ColumnDataSource(data=dict(xl=[12.93, 12.93], y=[0.12,0])) #bokeh data for line   OK

#p.add_tools(TapTool(callback=callback))
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'per_diab', 'transform' : color_mapper}, line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p.add_layout(color_bar, 'below')

#remove plot axes
p.axis.visible = None


### Histogram ####

hist, edges = np.histogram(durham_models['per_diab'], density=True, bins=30)


p1 = figure(title="Distribution of % Diabetic Rate in Durham, NC Block Groups",tools="save", background_fill_color="#FDFEFE", width=300, height= 200)

p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],fill_color="#D5DBDB", line_color="#D5DBDB")


# y is value of per_diab at index (s3)


p1.line(x='xl', y='y', color="orange", line_width=5, alpha=0.6, source=s3) ## plot line OK

show(p)
show(p1)
#output_notebook()
#output_file("preview.html")

app = Flask(__name__)

# To prevent caching files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    x = [x*0.005 for x in range(0, 200)]
    y = x
    source = ColumnDataSource(data=dict(x=x, y=y))


    plot = figure(plot_width=300, plot_height=250)
    plot.line('x', 'y',  line_width=3, source=source, line_alpha=0.6)

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var f = cb_obj.value
        x = data['x']
        y = data['y']
        for (i = 0; i < x.length; i++) {
            y[i] = Math.pow(x[i], f)
        }
        source.trigger('change');
    """)

    slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
    slider.js_on_change('value', callback)

    layout = column(slider, plot)
    script, div = components(layout, INLINE)
    return render_template('bokeh.html',
                           script=script,
                           div=div,
                           js_resources=INLINE.render_js(),
                           css_resources=INLINE.render_css())


my_data = {'one': [1, 3, 5],
           'two': [2, 7, 5],
           'three': [8, 3, 6]}


if __name__ == "__main__":
    app.run(debug=True)
