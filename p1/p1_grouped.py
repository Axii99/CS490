import math
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange, LegendItem, Legend
from bokeh.palettes import Spectral6, magma, cividis
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
import pandas as pd
import numpy as np

#output_file("bars.html")


data = pd.read_csv("old_cars.csv")
origins = ['US','Europe','Japan']
japan = data.loc[data['Origin'] == 'Japan']
maxMPG = max(data['MPG'])
minMPG = min(data['MPG'])

MPGs = [*range(math.floor(minMPG), math.ceil(maxMPG), 2)]
matrix = np.zeros((len(MPGs),3))



for i in  range(len(MPGs)-1):
    for j ,ori in enumerate(origins):
        subset = data.loc[data['Origin'] == ori]
        count = subset.loc[(subset['MPG'] >= MPGs[i]) & (subset['MPG'] < MPGs[i+1])]["MPG"].count()
        matrix[i][j] = count
    #print(count)


temp = [str(m) for m in MPGs]
print(temp)
x = [ (ori,mpg) for mpg in temp for ori in origins]

dictionary = {}
dictionary['Origin'] = origins
for i, t in enumerate(temp):
    dictionary[t] = matrix[i,:].tolist()


print(dictionary)
source = ColumnDataSource(data=dictionary)
p = figure(x_range=FactorRange(*x), y_range=(0,50),plot_height=500, title="MPG",
           toolbar_location=None, tools="")

colors = cividis(20)

#r = p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",fill_color=factor_cmap('x', palette=magma(20), factors=temp, start=1, end=20))

for i in range(len(temp)):
    p.vbar(x=dodge('Origin', -0.6*10+0.6*i, range=p.x_range), top=temp[i], width=0.4, source=source,
           color=colors[i], legend_label=temp[i])




p.xgrid.grid_line_color = None
p.y_range.start = 0
p.y_range.end = 45
p.xaxis.major_label_text_alpha = 0
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "vertical"
p.legend.label_text_font_size = "5pt"
p.legend.padding = 0
p.legend.spacing = 0
show(p)
