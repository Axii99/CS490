import math
from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource, FactorRange, LegendItem, Legend
from bokeh.palettes import Spectral6, magma, cividis,turbo
from bokeh.plotting import figure,curdoc
from bokeh.models import CustomJS, Select,Dropdown,Slider
import pandas as pd
import numpy as np


TOOLS = "box_select,lasso_select,help"

data = pd.read_csv("factbook.csv")
length = len(data.index)
plot1 = figure(tools=TOOLS,plot_width=800, plot_height=400)
plot2 = figure(tools=TOOLS,plot_width=800, plot_height=400)
plot3 = figure(tools=TOOLS,plot_width=800, plot_height=400)
plot4 = figure(tools=TOOLS,plot_width=800, plot_height=400)
colors = turbo(11)

data = data.rename(columns=lambda x: x.strip())
GDPperCapita = data['GDP per capita'].str.replace("$", "").str.replace(",", "").str.strip().astype(float)
Life = np.array(data['Life expectancy at birth'].values)
population = data['Population'].str.replace(",", "").astype(float)
population = np.array([float(x - min(population.values))/ float((max(population.values) - min(population.values)))* 29.0 + 5 for x in population.values])
#print(population)
birthrate = np.array(data['Birth rate'])
colorlist = [colors[int((i/max(birthrate)) * 10)] for i in birthrate]
GDPperCapita = np.array(GDPperCapita.values)



dictionary = {'xdata1': GDPperCapita,
              'ydata1': Life,
              'xdata2': GDPperCapita,
              'ydata2': Life,
              'xdata3': GDPperCapita,
              'ydata3': Life,
              'xdata4': GDPperCapita,
              'ydata4': Life,
              'BirthRate': birthrate,
              'size1': population,
              'size2': population,
              'size3': population,
              'size4': population,
              'ColorList1': colorlist,
              'ColorList2': colorlist,
              'ColorList3': colorlist,
              'ColorList4': colorlist}
source = ColumnDataSource(data=dictionary)

for key in data.keys():
    if (key != "Country"):
        print(key)
        dictionary[key] = np.array(pd.to_numeric(data[key].apply(str).str.replace("$", "").str.replace(",", "").str.strip().str.replace("(", "").str.replace(")", "").str.replace(" ", "nan"), errors='coerce'))
    else:
        dictionary['Country'] = data['Country'].astype(str)

source = ColumnDataSource(data=dictionary)



menu = []
for key in data.keys():
    if key != "Country":
        menu.append((key,key))


p1=plot1.circle(x='xdata1', y='ydata1', source= source, size='size1', color='ColorList1', alpha=0.6, line_color="black", line_width = 2)
ds1 = p1.data_source

p2=plot2.circle(x='xdata2', y='ydata2', source= source, size='size2', color='ColorList2', alpha=0.6, line_color="black", line_width = 2)
ds2 = p2.data_source

p3=plot3.circle(x='xdata3', y='ydata3', source= source, size='size3', color='ColorList3', alpha=0.6, line_color="black", line_width = 2)
ds3 = p3.data_source

p4=plot4.circle(x='xdata4', y='ydata4', source= source, size='size4', color='ColorList4', alpha=0.6, line_color="black", line_width = 2)
ds4 = p4.data_source

dropdownX1 = Dropdown(label="X value1", button_type="default", menu=menu)
dropdownX2 = Dropdown(label="X value2", button_type="default", menu=menu)
dropdownX3 = Dropdown(label="X value3", button_type="default", menu=menu)
dropdownX4 = Dropdown(label="X value4", button_type="default", menu=menu)
def dropdownX_handler1(new):
    dictionary['xdata1'] = dictionary[new.item]
    ds1.data = dictionary
    plot1.xaxis.axis_label = new.item

def dropdownX_handler2(new):
    dictionary['xdata2'] = dictionary[new.item]
    ds2.data = dictionary
    plot2.xaxis.axis_label = new.item

def dropdownX_handler3(new):
    dictionary['xdata3'] = dictionary[new.item]
    ds3.data = dictionary
    plot3.xaxis.axis_label = new.item

def dropdownX_handler4(new):
    dictionary['xdata4'] = dictionary[new.item]
    ds4.data = dictionary
    plot4.xaxis.axis_label = new.item

dropdownX1.on_click(dropdownX_handler1)
dropdownX2.on_click(dropdownX_handler2)
dropdownX3.on_click(dropdownX_handler3)
dropdownX4.on_click(dropdownX_handler4)

dropdownY1 = Dropdown(label="Y value1", button_type="default", menu=menu)
dropdownY2 = Dropdown(label="Y value2", button_type="default", menu=menu)
dropdownY3 = Dropdown(label="Y value3", button_type="default", menu=menu)
dropdownY4 = Dropdown(label="Y value4", button_type="default", menu=menu)
def dropdownY_handler1(new):
    dictionary['ydata1'] = dictionary[new.item]
    ds1.data = dictionary
    plot1.yaxis.axis_label = new.item

def dropdownY_handler2(new):
    dictionary['ydata2'] = dictionary[new.item]
    ds2.data = dictionary
    plot2.yaxis.axis_label = new.item

def dropdownY_handler3(new):
    dictionary['ydata3'] = dictionary[new.item]
    ds3.data = dictionary
    plot3.yaxis.axis_label = new.item

def dropdownY_handler4(new):
    dictionary['ydata4'] = dictionary[new.item]
    ds4.data = dictionary
    plot4.yaxis.axis_label = new.item

dropdownY1.on_click(dropdownY_handler1)
dropdownY2.on_click(dropdownY_handler2)
dropdownY3.on_click(dropdownY_handler3)
dropdownY4.on_click(dropdownY_handler4)

slider1 = Slider(start=0.5, end=2, value=1, step=0.1, title="Slider1")
slider2 = Slider(start=0.5, end=2, value=1, step=0.1, title="Slider2")
slider3 = Slider(start=0.5, end=2, value=1, step=0.1, title="Slider3")
slider4 = Slider(start=0.5, end=2, value=1, step=0.1, title="Slider4")
def slider_handler1(attr, old, new):
    ds1.data['size1'] = dictionary['size1'] * slider1.value

def slider_handler2(attr, old, new):
    ds2.data['size2'] = dictionary['size2'] * slider2.value

def slider_handler3(attr, old, new):
    ds3.data['size3'] = dictionary['size3'] * slider3.value

def slider_handler4(attr, old, new):
    ds4.data['size4'] = dictionary['size4'] * slider4.value


slider1.on_change('value', slider_handler1)
slider2.on_change('value', slider_handler2)
slider3.on_change('value', slider_handler3)
slider4.on_change('value', slider_handler4)


dropdownR1 = Dropdown(label="Radius", button_type="default", menu=menu)
dropdownR2 = Dropdown(label="Radius", button_type="default", menu=menu)
dropdownR3 = Dropdown(label="Radius", button_type="default", menu=menu)
dropdownR4 = Dropdown(label="Radius", button_type="default", menu=menu)
def dropdownR_handler1(new):
    temp = dictionary[new.item]
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size1'] = sizelist
    ds1.data = dictionary

def dropdownR_handler2(new):
    temp = dictionary[new.item]
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size2'] = sizelist
    ds2.data = dictionary

def dropdownR_handler3(new):
    temp = dictionary[new.item]
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size3'] = sizelist
    ds3.data = dictionary

def dropdownR_handler4(new):
    temp = dictionary[new.item]
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size4'] = sizelist
    ds4.data = dictionary

dropdownR1.on_click(dropdownR_handler1)
dropdownR2.on_click(dropdownR_handler2)
dropdownR3.on_click(dropdownR_handler3)
dropdownR4.on_click(dropdownR_handler4)


dropdownC1 = Dropdown(label="Colors", button_type="default", menu=menu)
dropdownC2 = Dropdown(label="Colors", button_type="default", menu=menu)
dropdownC3 = Dropdown(label="Colors", button_type="default", menu=menu)
dropdownC4 = Dropdown(label="Colors", button_type="default", menu=menu)
def dropdownC_handler1(new):
    temp = dictionary[new.item]
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList1'] = colorlist
    ds1.data = dictionary

def dropdownC_handler2(new):
    temp = dictionary[new.item]
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList2'] = colorlist
    ds2.data = dictionary

def dropdownC_handler3(new):
    temp = dictionary[new.item]
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList3'] = colorlist
    ds3.data = dictionary

def dropdownC_handler4(new):
    temp = dictionary[new.item]
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList4'] = colorlist
    ds4.data = dictionary

dropdownC1.on_click(dropdownC_handler1)
dropdownC2.on_click(dropdownC_handler2)
dropdownC3.on_click(dropdownC_handler3)
dropdownC4.on_click(dropdownC_handler4)


plot1.xaxis.axis_label = 'GDP per Capita'
plot1.yaxis.axis_label = 'Life Expectancy'
plot2.xaxis.axis_label = 'GDP per Capita'
plot2.yaxis.axis_label = 'Life Expectancy'
plot3.xaxis.axis_label = 'GDP per Capita'
plot3.yaxis.axis_label = 'Life Expectancy'
plot4.xaxis.axis_label = 'GDP per Capita'
plot4.yaxis.axis_label = 'Life Expectancy'
curdoc().add_root(gridplot([[plot1, plot2], [dropdownX1,dropdownX2], [dropdownY1,dropdownY2], [dropdownC1,dropdownC2], [dropdownR1,dropdownR2],[slider1,slider2],[plot3, plot4], [dropdownX3,dropdownX4], [dropdownY3,dropdownY4], [dropdownC3,dropdownC4], [dropdownR3,dropdownR4],[slider3,slider4]]))