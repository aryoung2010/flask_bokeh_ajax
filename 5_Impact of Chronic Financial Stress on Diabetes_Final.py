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

#output_notebook()
output_file("preview.html")

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


# Data[yl] is y

# emit changes for s1
# emit changes for s3


#####################################################################
##### Title and Summary
Header = Div(text="""<h2><font color= "DarkSlateGrey"> Impact of Chronic Stress Exposure on Neighborhood Diabetes</font> </h2>""",width=600, height=10)
          

Summary = Div(text="""<font color= "DarkSlateGrey"><br><br><br>And here i will type a short summary of the relationships.""",width=500, height=200)

##################################################################
### Instructions for map
titleMap= Div(text="""<font size=3, color=DarkSlateGrey><b>Select your neighborhood on the map below to learn about diabetes in your area<br>""", width=650, height= 30)



##################################################################
### Sliders to control model info
titleSlide= Div(text="""<font size=3, color=DarkSlateGrey><b>Move the sliders below to see changes in neighborhood diabetes<br><br>""", width=500, height= 30)

#Instructions= Div(text="""<br>Select your neighborhood on the map below to see how changes in evictions and uninsured rates could influence the rate of diabetes in your community.""",width=500, height=90)

##################################################################
### Interations

#################################################################
### Column Grid Padding
colgap= Div(text="""""",width=10, height=350)

#################################################################
### Row Grid Padding
rowgap = Div(text="""""",width=350, height=60)
srowgap= Div(text="""""",width=350, height=30)


## I started the sliders at 1 so that the model wouldn't predict the value at zero (as opposed to using real values...)
slider = Slider(start=1, end=50, value=1, step=1, title="Decrease Evictions (% change)", width=350)
slider2 = Slider(start=1, end=50, value=1, step=1, title="Decrease Uninsured Rate (% change)", width=350)

####################################################################
### 2017 Calculated Text by Blockgroup/Neighborhood
Select_Text = Div(text="""""", width=400, height=56)

##################################################################
### Model Calculated Text
Model_Text = Div(text="""""", width=400, height=80)

# where map selected, when a change happens, perform this action
# three arguments- s1, s3
## indicies (constant) are the indicies of the selected elements, called inds
## d holds the data for those indicies
## y defaults to 0

# if no selection, end action (default text values)

# for selected index

# y is value of per_diab at index (s3)
callback=CustomJS(args=dict(geosource=geosource, distribution_chart=s3, paragraph=Select_Text, modparagraph=Model_Text), code="""const inds = geosource.selected['1d'].indices; const d = geosource.data; console.log(d); const diabetesRate = d['total__diabetic__rate'][inds[0]].toFixed(2); const poorControl = d['actual_diabetic__poor_control_rate'][inds[0]].toFixed(2); const evictionRate = d['Evictions'][inds[0]].toFixed(1); const uninsuredRate = d['Uninsured_Adult19_64'][inds[0]].toFixed(2); const evicDiff=0; const uninsDiff=0; const diabetesRateMod= (.1+(16*(uninsuredRate*(1-uninsDiff))/100)).toFixed(2); const poorControlMod= (.012+(.11*(evictionRate*(1-evicDiff))/100)).toFixed(2);distribution_chart.data['xl'] = [diabetesRate*100, diabetesRate*100]; const shortName = d['Short_Name'][inds[0]];console.log(shortName);const newParagraphText = '<br><font color= "DarkCyan", size= 4>' + shortName + '<font color="DarkSlateGrey", size = 3><br><br>The <b>total diabetic rate</b> in ' + shortName + ' is '+ diabetesRate*100 + '%<br><br>The <b>poorly managed diabetes rate</b> is ' + poorControl*100 + '%.<br><br>This neighborhood <b>eviction rate</b> is ' + evictionRate + ' per 100 renters.<br><br>The <b>uninsured rate</b> for Adults 16-64 is ' + uninsuredRate*100 + '%.</font>';console.log(newParagraphText); const modelParagraphText = '<font color= "DarkCyan", size= 4>'+ shortName+ '</font><br>A decrease of <b>'+ evicDiff + '% </b> in evictions and <b>' + uninsDiff + '% </b> in the uninsured rate, could mean that for every <b> 1000 residents </b> in this neighborhood, there would be approximately <b>'+ diabetesRateMod*1000 +'</b> residents diagnosed with diabetes rather than <b>' + diabetesRate*1000 +'</b> and <b>' + poorControlMod*1000 + '</b> residents living with poorly managed diabetes, rather than <b>' + poorControl*1000 + '.</font>';console.log(modelParagraphText);paragraph.text = newParagraphText;modparagraph.text = modelParagraphText;geosource.change.emit();distribution_chart.change.emit();paragraph.change.emit();modparagraph.change.emit(); """)
                        
# TODO: DISABLE MULTIPLE SELECT ON TAPTOOL
#p.add_tools(TapTool(callback=callback))

##################################################################
### Detailed Info

Description = Div(text="""<br><h3>Why this matters</h3><br>And here i will type a paragraph about the talking points.""",width=400, height=200)

##################################################################
### Layout
grid = gridplot([[column(Header,Summary)],[column(titleMap,p), column(srowgap,Select_Text,rowgap,rowgap,rowgap,rowgap,p1)],[column(rowgap,titleSlide, srowgap)],[column(srowgap,slider,slider2,rowgap),column(Model_Text)],[Description]])

##################################################################
### Show
show(grid)

