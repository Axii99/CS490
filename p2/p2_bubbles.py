import math
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange, LegendItem, Legend
from bokeh.palettes import Spectral6, magma, cividis
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
import pandas as pd
import numpy as np


data = pd.read_csv("factbook.csv")
length = len(data.index)
p = figure(plot_width=800, plot_height=400)
colors = cividis(25)

data = data.rename(columns=lambda x: x.strip())
GDPperCapita = data['GDP per capita'].str.replace("$", "").str.replace(",", "").str.strip().astype(float)
Life = data['Life expectancy at birth']
population = data['Population'].str.replace(",", "").astype(int)
birthrate = data['Birth rate']
population = population /10000000
#print(birthrate)
colorlist = [colors[int(i/2)] for i in birthrate]
print(colorlist)
xdata = GDPperCapita.values
ydata = Life.values
#print(xdata)
p.circle(xdata, ydata, size= population, color = colorlist)
show(p)