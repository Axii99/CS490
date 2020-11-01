import math
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, FactorRange, LegendItem, Legend
from bokeh.palettes import Spectral6, magma, cividis, Spectral3
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
import pandas as pd
import numpy as np



origins = ['US','Europe','Japan']
data = pd.read_csv("old_cars.csv")
years = [*range(70, 83)]

plot1 = figure(plot_width=400, plot_height=400, title='MPG-Weight')
plot2 = figure(plot_width=400, plot_height=400, title='MPG-Horsepower')
plot3 = figure(plot_width=400, plot_height=400, title='MPG-EngineSize')
plot4 = figure(plot_width=400, plot_height=400, title='Weight-Horsepower')
plot5 = figure(plot_width=400, plot_height=400, title='Weight-Enginesize')
plot6 = figure(plot_width=400, plot_height=400, title='Horsepower-Enginsize')

colors = Spectral3

for i, ori in enumerate(origins):
    subset = data.loc[data['Origin'] == ori]
    xdata = subset['Weight'].values
    ydata = subset['MPG'].values
    plot1.circle(xdata, ydata, color=colors[i], legend_label=ori)


for i, ori in enumerate(origins):
    subset = data.loc[data['Origin'] == ori]
    xdata = subset['Horsepower'].values
    ydata = subset['MPG'].values
    plot2.circle(xdata, ydata, color=colors[i], legend_label=ori)

for i, ori in enumerate(origins):
    subset = data.loc[data['Origin'] == ori]
    xdata = subset['Displacement'].values
    ydata = subset['MPG'].values
    plot3.circle(xdata, ydata, color=colors[i], legend_label=ori)

for i, ori in enumerate(origins):
    subset = data.loc[data['Origin'] == ori]
    xdata = subset['Horsepower'].values
    ydata = subset['Weight'].values
    plot4.circle(xdata, ydata, color=colors[i], legend_label=ori)

for i, ori in enumerate(origins):
    subset = data.loc[data['Origin'] == ori]
    xdata = subset['Displacement'].values
    ydata = subset['Weight'].values
    plot5.circle(xdata, ydata, color=colors[i], legend_label=ori)

for i, ori in enumerate(origins):
    subset = data.loc[data['Origin'] == ori]
    xdata = subset['Displacement'].values
    ydata = subset['Horsepower'].values
    plot6.circle(xdata, ydata, color=colors[i], legend_label=ori)


p = gridplot([[plot1,plot2],[plot3,plot4],[plot5,plot6]])
show(p)