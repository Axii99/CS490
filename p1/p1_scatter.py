import math
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange, LegendItem, Legend
from bokeh.palettes import Spectral6, magma, cividis
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
import pandas as pd
import numpy as np


data = pd.read_csv("old_cars.csv")
years = [*range(70, 83)]

p = figure(plot_width=400, plot_height=400)
colors = cividis(13)

for i, y in enumerate(years):
    subset = data.loc[data['Model'] == y]
    xdata = subset['Horsepower'].values
    ydata = subset['MPG'].values

    p.circle(xdata, ydata, color=colors[i], legend_label='19'+str(y))

show(p)