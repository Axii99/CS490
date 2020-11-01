import math
from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource, FactorRange, LegendItem, Legend
from bokeh.palettes import Spectral6, magma, cividis, turbo
from bokeh.plotting import figure,curdoc
from bokeh.models import CustomJS, Select,Dropdown,Slider
import pandas as pd
import numpy as np


data = pd.read_csv("factbook.csv")
length = len(data.index)
p = figure(plot_width=800, plot_height=400)
colors = turbo(11)

data = data.rename(columns=lambda x: x.strip())
GDPperCapita = data['GDP per capita'].str.replace("$", "").str.replace(",", "").str.strip().astype(float)
Life = np.array(data['Life expectancy at birth'].values)
population = data['Population'].str.replace(",", "").astype(float)
population = np.array([float(x - min(population.values))/ float((max(population.values) - min(population.values)))* 29.0 + 5 for x in population.values])
birthrate = np.array(data['Birth rate'])
colorlist = [colors[int((i/max(birthrate)) * 10)] for i in birthrate]
area = np.array(data['Area'].str.replace("$", "").str.replace(",", "").str.strip().astype(float))
cab = np.array(data['Current account balance'].str.replace("$", "").str.replace(",", "").str.replace("(", "").str.replace(")", "").str.strip().astype(float))


GDPperCapita = np.array(GDPperCapita.values)




dictionary = {'xdata': GDPperCapita,
              'ydata': Life,
              'size': population,
              'ColorList': colorlist}

for key in data.keys():
    if (key != "Country"):
        print(key)
        dictionary[key] = np.array(pd.to_numeric(data[key].apply(str).str.replace("$", "").str.replace(",", "").str.strip().str.replace("(", "").str.replace(")", "").str.replace(" ", "nan"), errors='coerce'))
    else:
        dictionary['Country'] = data['Country'].astype(str)

source = ColumnDataSource(data=dictionary)



menu = []
for key in data.keys():
    menu.append((key,key))



plot=p.circle(x='xdata', y='ydata', source= source, size='size',color='ColorList', alpha=0.6, line_color="black", line_width = 1)
ds = plot.data_source

dropdownX = Dropdown(label="X value", button_type="default", menu=menu)
def dropdownX_handler(new):
    dictionary['xdata'] = dictionary[new.item]
    ds.data = dictionary
    print(dictionary['xdata'])
    print(new.item)
    p.xaxis.axis_label = new.item

dropdownX.on_click(dropdownX_handler)


dropdownY = Dropdown(label="Y value", button_type="default", menu=menu)
def dropdownY_handler(new):
    dictionary['ydata'] = dictionary[new.item]
    ds.data = dictionary
    p.yaxis.axis_label = new.item

dropdownY.on_click(dropdownY_handler)

dropdownR = Dropdown(label="Radius", button_type="default", menu=menu)
def dropdownR_handler(new):
    temp = dictionary[new.item]
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size'] = sizelist
    ds.data = dictionary

dropdownR.on_click(dropdownR_handler)

dropdownC = Dropdown(label="Colors", button_type="default", menu=menu)
def dropdownC_handler(new):
    temp = dictionary[new.item]
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList'] = colorlist
    ds.data = dictionary

dropdownC.on_click(dropdownC_handler)


slider = Slider(start=0.5, end=2, value=1, step=0.1, title="Slider")
def slider_handler(attr, old, new):
        ds.data['size'] = np.array(dictionary['size']) * slider.value

slider.on_change('value', slider_handler)



p.xaxis.axis_label = 'GDP per Capita'
p.yaxis.axis_label = 'Life Expectancy'
curdoc().add_root(gridplot([[p],[dropdownX],[dropdownY],[dropdownC],[dropdownR],[slider]]))