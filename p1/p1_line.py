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
origins = ['US','Europe','Japan']
years = [*range(70, 83)]
print(years)

US_line = []
Ja_line = []
Eu_line = []


for y in years:
    for ori in origins:
        subset = data.loc[(data['Origin'] == ori) & (data['Model'] == y)]
        average = sum(subset["MPG"]) / subset["MPG"].count()
        #print(average)
        if (ori == 'US'):
            US_line.append(average)
        elif(ori == "Europe"):
            Eu_line.append(average)
        else:
            Ja_line.append(average)

print(US_line)
print(Eu_line)
print(Ja_line)


source = ColumnDataSource(data=dict(
    x=years,
    y1=US_line,
    y2=Eu_line,
    y3=Ja_line,
))
p = figure(plot_width=400, plot_height=400)

#p.vline_stack(['y1', 'y2', 'y3'], x='x', source=source)

p.line(x='x', y='y1', line_width=2,source = source, color='red', legend_label='US')
p.circle(x='x', y='y1', source = source, color='red',legend_label='US')
p.line(x='x', y='y2', line_width=2,source = source, color='blue', legend_label='Europe')
p.circle(x='x', y='y2', source = source, color='blue', legend_label='Europe')
p.line(x='x', y='y3', line_width=2,source = source, color='yellow', legend_label='Japan')
p.circle(x='x', y='y3', source = source, color='yellow', legend_label='Japan')


show(p)