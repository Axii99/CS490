import math
from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource, FactorRange, LegendItem, Legend, HoverTool, LogColorMapper, ColorBar, \
    LogTicker, Label
from bokeh.palettes import Spectral6, magma, cividis,turbo
from bokeh.plotting import figure,curdoc
from bokeh.models import CustomJS, Select,Dropdown,Slider
import pandas as pd
import numpy as np


TOOLS = "pan,wheel_zoom,reset,box_select,lasso_select,help"



data = pd.read_csv("factbook.csv")

TOOLTIPS = [
    ("index", "$index"),
    ("Country", "@Country"),
    ("GDP per Capita", "@{GDP per capita}"),
    ("Life expectancy at birth", "@{Life expectancy at birth}"),
    ("Population", "@{Population}"),
    ("Birth rate", "@{Birth rate}")
]


length = len(data.index)
plot1 = figure(tools=TOOLS, tooltips=TOOLTIPS,plot_width=800, plot_height=400)
plot2 = figure(tools=TOOLS,tooltips=TOOLTIPS,plot_width=800, plot_height=400)
plot3 = figure(tools=TOOLS,tooltips=TOOLTIPS,plot_width=800, plot_height=400)
plot4 = figure(tools=TOOLS,tooltips=TOOLTIPS,plot_width=800, plot_height=400)
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
              'size1': population,
              'size2': population,
              'size3': population,
              'size4': population,
              'ColorList1': colorlist,
              'ColorList2': colorlist,
              'ColorList3': colorlist,
              'ColorList4': colorlist
              }
source = ColumnDataSource(data=dictionary)

dict = {'x1': 'GDP per capita',
              'y1': 'Life expectancy at birth',
              'x2': 'GDP per capita',
              'y2': 'Life expectancy at birth',
              'x3': 'GDP per capita',
              'y3': 'Life expectancy at birth',
              'x4': 'GDP per capita',
              'y4': 'Life expectancy at birth',
        'r1': 'Population',
        'r2': 'Population',
        'r3': 'Population',
        'r4': 'Population',
        'c1': 'Birth rate',
        'c2': 'Birth rate',
        'c3': 'Birth rate',
        'c4': 'Birth rate',
        }


for key in data.keys():
    if (key != "Country"):
        print(key)
        dictionary[key] = np.array(pd.to_numeric(data[key].apply(str).str.replace("$", "").str.replace(",", "").str.strip().str.replace("(", "").str.replace(")", "").str.replace(" ", "0"), errors='coerce'))
    else:
        dictionary['Country'] = data['Country'].astype(str)

source = ColumnDataSource(data=dictionary)



menu = []
for key in data.keys():
    if key != "Country":
        menu.append((key,key))


color_mapper = LogColorMapper(palette="Turbo256", low=min(dictionary['Birth rate']), high=max(dictionary['Birth rate']))
color_bar1 = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),label_standoff=12, border_line_color=None, location=(0,0))
color_bar2 = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),label_standoff=12, border_line_color=None, location=(0,0))
color_bar3 = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),label_standoff=12, border_line_color=None, location=(0,0))
color_bar4 = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),label_standoff=12, border_line_color=None, location=(0,0))
color_label1 = Label(x=70, y=70, text='Birth rate')
color_label2 = Label(x=70, y=70, text='Birth rate')
color_label3 = Label(x=70, y=70, text='Birth rate')
color_label4 = Label(x=70, y=70, text='Birth rate')

p1=plot1.circle(x='xdata1', y='ydata1', source= source, size='size1', color='ColorList1', alpha=0.6, line_color="black", line_width = 2)
ds1 = p1.data_source
plot1.add_layout(color_bar1, 'right')
plot1.add_layout(color_label1, 'right')

p2=plot2.circle(x='xdata2', y='ydata2', source= source, size='size2', color='ColorList2', alpha=0.6, line_color="black", line_width = 2)
ds2 = p2.data_source
plot2.add_layout(color_bar2, 'right')
plot2.add_layout(color_label2, 'right')

p3=plot3.circle(x='xdata3', y='ydata3', source= source, size='size3', color='ColorList3', alpha=0.6, line_color="black", line_width = 2)
ds3 = p3.data_source
plot3.add_layout(color_bar3, 'right')
plot3.add_layout(color_label3, 'right')

p4=plot4.circle(x='xdata4', y='ydata4', source= source, size='size4', color='ColorList4', alpha=0.6, line_color="black", line_width = 2)
ds4 = p4.data_source
plot4.add_layout(color_bar4, 'right')
plot4.add_layout(color_label4, 'right')

def update_tooltip():
    ttx = [(dict['x1'], '@{' + dict['x1'] + '}')]
    tty = [(dict['y1'], '@{' + dict['y1'] + '}')]
    ttr = [(dict['r1'], '@{' + dict['r1'] + '}')]
    ttc = [(dict['c1'], '@{' + dict['c1'] + '}')]
    plot1.tools[6] = HoverTool(tooltips=[("index", "$index"), ("Country", "@Country")] + ttx+tty+ttr+ttc)
    ttx = [(dict['x2'], '@{' + dict['x2'] + '}')]
    tty = [(dict['y2'], '@{' + dict['y2'] + '}')]
    ttr = [(dict['r2'], '@{' + dict['r2'] + '}')]
    ttc = [(dict['c2'], '@{' + dict['c2'] + '}')]
    plot2.tools[6] = HoverTool(tooltips=[("index", "$index"), ("Country", "@Country")] + ttx+tty+ttr+ttc)
    ttx = [(dict['x3'], '@{' + dict['x3'] + '}')]
    tty = [(dict['y3'], '@{' + dict['y3'] + '}')]
    ttr = [(dict['r3'], '@{' + dict['r3'] + '}')]
    ttc = [(dict['c3'], '@{' + dict['c3'] + '}')]
    plot3.tools[6] = HoverTool(tooltips=[("index", "$index"), ("Country", "@Country")] + ttx+tty+ttr+ttc)
    ttx = [(dict['x4'], '@{' + dict['x4'] + '}')]
    tty = [(dict['y4'], '@{' + dict['y4'] + '}')]
    ttr = [(dict['r4'], '@{' + dict['r4'] + '}')]
    ttc = [(dict['c4'], '@{' + dict['c4'] + '}')]
    plot4.tools[6] = HoverTool(tooltips=[("index", "$index"), ("Country", "@Country")] + ttx+tty+ttr+ttc)

dropdownX1 = Dropdown(label="X value1", button_type="default", menu=menu)
dropdownX2 = Dropdown(label="X value2", button_type="default", menu=menu)
dropdownX3 = Dropdown(label="X value3", button_type="default", menu=menu)
dropdownX4 = Dropdown(label="X value4", button_type="default", menu=menu)
def dropdownX_handler1(new):
    dictionary['xdata1'] = dictionary[new.item]
    dict['x1'] = new.item
    ds1.data = dictionary
    plot1.xaxis.axis_label = new.item
    update_tooltip()

def dropdownX_handler2(new):
    dictionary['xdata2'] = dictionary[new.item]
    dict['x2'] = new.item
    ds2.data = dictionary
    plot2.xaxis.axis_label = new.item
    update_tooltip()

def dropdownX_handler3(new):
    dictionary['xdata3'] = dictionary[new.item]
    dict['x3'] = new.item
    ds3.data = dictionary
    plot3.xaxis.axis_label = new.item
    update_tooltip()

def dropdownX_handler4(new):
    dictionary['xdata4'] = dictionary[new.item]
    dict['x4'] = new.item
    ds4.data = dictionary
    plot4.xaxis.axis_label = new.item
    update_tooltip()

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
    dict['y1'] = new.item
    ds1.data = dictionary
    plot1.yaxis.axis_label = new.item
    update_tooltip()

def dropdownY_handler2(new):
    dictionary['ydata2'] = dictionary[new.item]
    dict['y2'] = new.item
    ds2.data = dictionary
    plot2.yaxis.axis_label = new.item
    update_tooltip()

def dropdownY_handler3(new):
    dictionary['ydata3'] = dictionary[new.item]
    dict['y3'] = new.item
    ds3.data = dictionary
    plot3.yaxis.axis_label = new.item
    update_tooltip()

def dropdownY_handler4(new):
    dictionary['ydata4'] = dictionary[new.item]
    dict['y4'] = new.item
    ds4.data = dictionary
    plot4.yaxis.axis_label = new.item
    update_tooltip()

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
    dict['r1'] = new.item
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size1'] = sizelist
    ds1.data = dictionary
    update_tooltip()

def dropdownR_handler2(new):
    temp = dictionary[new.item]
    dict['r2'] = new.item
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size2'] = sizelist
    ds2.data = dictionary
    update_tooltip()

def dropdownR_handler3(new):
    temp = dictionary[new.item]
    dict['r3'] = new.item
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size3'] = sizelist
    ds3.data = dictionary
    update_tooltip()

def dropdownR_handler4(new):
    temp = dictionary[new.item]
    dict['r4'] = new.item
    sizelist = [float(i - min(temp)) / float(max(temp) - min(temp)) * 29 + 5 for i in temp]
    dictionary['size4'] = sizelist
    ds4.data = dictionary
    update_tooltip()

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
    dict['c1'] = new.item
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList1'] = colorlist
    ds1.data = dictionary
    update_tooltip()
    mapper = LogColorMapper(palette="Turbo256", low=min(dictionary[new.item]),
                                  high=max(dictionary[new.item]))
    color_bar1.color_mapper = mapper

def dropdownC_handler2(new):
    temp = dictionary[new.item]
    dict['c2'] = new.item
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList2'] = colorlist
    ds2.data = dictionary
    update_tooltip()
    mapper = LogColorMapper(palette="Turbo256", low=min(dictionary[new.item]),
                            high=max(dictionary[new.item]))
    color_bar2.color_mapper = mapper

def dropdownC_handler3(new):
    temp = dictionary[new.item]
    dict['c3'] = new.item
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList3'] = colorlist
    ds3.data = dictionary
    update_tooltip()
    mapper = LogColorMapper(palette="Turbo256", low=min(dictionary[new.item]),
                            high=max(dictionary[new.item]))
    color_bar3.color_mapper = mapper

def dropdownC_handler4(new):
    temp = dictionary[new.item]
    dict['c4'] = new.item
    colorlist = [colors[int((i/max(temp)) * 10)] for i in temp]
    dictionary['ColorList4'] = colorlist
    ds4.data = dictionary
    update_tooltip()
    mapper = LogColorMapper(palette="Turbo256", low=min(dictionary[new.item]),
                            high=max(dictionary[new.item]))
    color_bar4.color_mapper = mapper

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